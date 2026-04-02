"""Image/Video generation and render job API routes"""
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.render import (
    ImageGenerationRequest,
    VideoGenerationRequest,
    RenderJobCreate,
    RenderJobUpdate,
    JobProgress,
    JobStatus
)
from app.models.render import RenderJob
from app.models.scene import Scene
from app.models.project import Project
from app.workers.tasks import generate_image_task, generate_video_task


router = APIRouter()


@router.post("/generate/image")
def generate_image(
    request: ImageGenerationRequest,
    db: Session = Depends(get_db)
):
    """
    Generate image for a scene

    Args:
        request: Image generation request
        db: Database session

    Returns:
        Render job ID for tracking progress
    """
    # Verify project exists
    project = db.query(Project).filter(Project.id == request.project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    # Verify scene exists
    scene = db.query(Scene).filter(Scene.id == request.scene_id).first()
    if not scene:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scene not found"
        )

    # Create render job
    job = RenderJob(
        project_id=request.project_id,
        scene_id=request.scene_id,
        job_type="image_generation",
        status=JobStatus.PENDING,
        parameters=request.model_dump()
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    # Start async Celery task
    generate_image_task.delay(
        job_id=job.id,
        scene_id=request.scene_id,
        prompt=request.prompt,
        width=request.width,
        height=request.height,
        steps=request.num_inference_steps,
        cfg_scale=request.guidance_scale
    )

    return {
        "job_id": job.id,
        "status": "pending",
        "message": "Image generation started"
    }


@router.post("/generate/video")
def generate_video(
    request: VideoGenerationRequest,
    db: Session = Depends(get_db)
):
    """
    Generate video from image

    Args:
        request: Video generation request
        db: Database session

    Returns:
        Render job ID for tracking progress
    """
    # Verify project exists
    project = db.query(Project).filter(Project.id == request.project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    # Verify scene exists
    scene = db.query(Scene).filter(Scene.id == request.scene_id).first()
    if not scene:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scene not found"
        )

    # Create render job
    job = RenderJob(
        project_id=request.project_id,
        scene_id=request.scene_id,
        job_type="video_generation",
        status=JobStatus.PENDING,
        parameters=request.model_dump()
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    # Start async Celery task
    generate_video_task.delay(
        job_id=job.id,
        scene_id=request.scene_id,
        image_url=request.image_url,
        duration=request.duration,
        fps=request.fps,
        motion_scale=request.motion_scale,
        enable_lipsync=request.enable_lipsync,
        audio_url=request.audio_url
    )

    return {
        "job_id": job.id,
        status": "pending",
        "message": "Video generation started"
    }


@router.get("/jobs/{job_id}", response_model=JobProgress)
def get_job_status(
    job_id: int,
    db: Session = Depends(get_db)
):
    """Get render job status"""
    job = db.query(RenderJob).filter(RenderJob.id == job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    return JobProgress(
        job_id=job.id,
        status=JobStatus(job.status),
        progress=job.progress,
        message=None,
        result_url=job.result_url
    )


@router.get("/project/{project_id}/jobs", response_model=List[RenderJob])
def get_project_jobs(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Get all render jobs for a project"""
    jobs = db.query(RenderJob).filter(
        RenderJob.project_id == project_id
    ).order_by(RenderJob.created_at.desc()).all()

    return jobs


@router.put("/jobs/{job_id}", response_model=RenderJob)
def update_job(
    job_id: int,
    job_update: RenderJobUpdate,
    db: Session = Depends(get_db)
):
    """Update render job (internal use by workers)"""
    job = db.query(RenderJob).filter(RenderJob.id == job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    update_data = job_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(job, field, value)

    db.commit()
    db.refresh(job)

    return job
