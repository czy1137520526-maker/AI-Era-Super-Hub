"""Script generation API routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.script import (
    ScriptGenerationRequest,
    ScriptGenerationResponse,
    ScriptScene
)
from app.schemas.scene import SceneCreate
from app.services.script_service import script_service
from app.models.scene import Scene
from app.models.project import Project


router = APIRouter()


@router.post("/generate", response_model=ScriptGenerationResponse)
async def generate_script(
    request: ScriptGenerationRequest,
    db: Session = Depends(get_db)
):
    """
    Generate script from user input using LLM

    Args:
        request: Script generation request with input text
        db: Database session

    Returns:
        ScriptGenerationResponse with generated scenes
    """
    # Verify project exists and belongs to user (TODO: add auth)
    project = db.query(Project).filter(Project.id == request.project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    # Generate script using LLM service
    generated_scenes = await script_service.generate_script(request)

    # Save scenes to database
    created_scenes = []
    for scene_data in generated_scenes:
        scene = SceneCreate(
            project_id=request.project_id,
            scene_number=scene_data.scene_id,
            description=scene_data.description,
            characters=scene_data.characters,
            emotion=scene_data.emotion,
            camera_angle=scene_data.camera_angle,
            dialogue=scene_data.dialogue,
        )

        db_scene = Scene(**scene.model_dump())
        db.add(db_scene)
        db.commit()
        db.refresh(db_scene)

        created_scenes.append(db_scene)

    return ScriptGenerationResponse(
        project_id=request.project_id,
        scenes=[ScriptScene(
            scene_id=scene.id,
            description=scene.description,
            characters=scene.characters or [],
            emotion=scene.emotion,
            camera_angle=scene.camera_angle,
            dialogue=scene.dialogue or []
        ) for scene in created_scenes],
        total_scenes=len(created_scenes)
    )


@router.get("/project/{project_id}", response_model=List[ScriptScene])
def get_project_scripts(
    project_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all scenes/scripts for a project

    Args:
        project_id: Project ID
        db: Database session

    Returns:
        List of scenes
    """
    # Verify project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    # Get scenes ordered by scene_number
    scenes = db.query(Scene).filter(
        Scene.project_id == project_id
    ).order_by(Scene.scene_number).all()

    return [ScriptScene(
        scene_id=scene.id,
        description=scene.description,
        characters=scene.characters or [],
        emotion=scene.emotion,
        camera_angle=scene.camera_angle,
        dialogue=scene.dialogue or []
    ) for scene in scenes]
