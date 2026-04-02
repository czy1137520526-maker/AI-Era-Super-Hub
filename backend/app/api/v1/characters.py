"""Character management API routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.character import (
    CharacterCreate,
    CharacterUpdate,
    CharacterDetail,
    LoraTrainingJob
)
from app.schemas.render import RenderJobCreate, JobStatus
from app.models.character import Character
from app.models.project import Project
from app.models.render import RenderJob
from app.workers.tasks import train_character_lora_task


router = APIRouter()


@router.post("/", response_model=CharacterDetail)
def create_character(
    character: CharacterCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new character

    Args:
        character: Character creation data
        db: Database session

    Returns:
        Created character
    """
    # Verify project exists
    project = db.query(Project).filter(Project.id == character.project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    # Create character
    db_character = Character(**character.model_dump())
    db.add(db_character)
    db.commit()
    db.refresh(db_character)

    return db_character


@router.get("/{character_id}", response_model=CharacterDetail)
def get_character(
    character_id: int,
    db: Session = Depends(get_db)
):
    """Get character by ID"""
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Character not found"
        )

    return character


@router.put("/{character_id}", response_model=CharacterDetail)
def update_character(
    character_id: int,
    character_update: CharacterUpdate,
    db: Session = Depends(get_db)
):
    """Update character"""
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Character not found"
        )

    # Update fields
    update_data = character_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(character, field, value)

    db.commit()
    db.refresh(character)

    return character


@router.delete("/{character_id}")
def delete_character(
    character_id: int,
    db: Session = Depends(get_db)
):
    """Delete character"""
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Character not found"
        )

    db.delete(character)
    db.commit()

    return {"message": "Character deleted successfully"}


@router.post("/{character_id}/train-lora")
def train_character_lora(
    character_id: int,
    training_job: LoraTrainingJob,
    db: Session = Depends(get_db)
):
    """
    Start LoRA training for character

    Args:
        character_id: Character ID
        training_job: Training configuration
        db: Database session

    Returns:
        Render job ID for tracking training progress
    """
    # Verify character exists
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Character not found"
        )

    # Create render job
    job = RenderJob(
        project_id=character.project_id,
        character_id=character_id,
        job_type="lora_training",
        status=JobStatus.PENDING,
        parameters={
            "reference_images": training_job.reference_images,
            "training_epochs": training_job.training_epochs,
            "learning_rate": training_job.learning_rate
        }
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    # Start async Celery task
    train_character_lora_task.delay(
        job_id=job.id,
        character_id=character_id,
        reference_images=training_job.reference_images,
        training_epochs=training_job.training_epochs,
        learning_rate=training_job.learning_rate
    )

    return {
        "job_id": job.id,
        "status": "pending",
        "message": "LoRA training started"
    }


@router.get("/project/{project_id}", response_model=List[CharacterDetail])
def get_project_characters(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Get all characters for a project"""
    # Verify project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    characters = db.query(Character).filter(
        Character.project_id == project_id
    ).all()

    return characters
