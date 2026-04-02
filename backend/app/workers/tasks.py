"""Celery async tasks for AI generation workflows"""
from typing import Dict, Any, List, Optional
import logging
from app.workers.celery_app import celery_app
from app.services.comfy_service import comfy_service
from app.services.character_service import character_service
from app.services.script_service import script_service
from app.schemas.render import JobStatus
from app.models.render import RenderJob
from app.db.session import SessionLocal
from fastapi import WebSocket

logger = logging.getLogger(__name__)


def update_job_progress(job_id: int, progress: int, status: Optional[str] = None, message: Optional[str] = None):
    """Update render job progress in database"""
    db = SessionLocal()
    try:
        job = db.query(RenderJob).filter(RenderJob.id == job_id).first()
        if job:
            job.progress = progress
            if status:
                job.status = status
            # TODO: Implement WebSocket notification
            # await notify_progress(job_id, progress, status, message)
            db.commit()
    except Exception as e:
        logger.error(f"Failed to update job progress: {e}")
        db.rollback()
    finally:
        db.close()


@celery_app.task(bind=True, name="generate_image")
def generate_image_task(
    self,
    job_id: int,
    scene_id: int,
    prompt: str,
    lora_path: Optional[str] = None,
    width: int = 1024,
    height: int = 1024,
    steps: int = 30,
    cfg_scale: float = 7.5
):
    """Async task for image generation using ComfyUI"""
    logger.info(f"Starting image generation task for job {job_id}")

    try:
        update_job_progress(job_id, 0, JobStatus.PROCESSING)

        # Build workflow
        workflow = {
            "template": "image_generation",
            "params": {
                "prompt": prompt,
                "negative_prompt": "(worst quality, low quality:1.4), blurry, deformed",
                "width": width,
                "height": height,
                "steps": steps,
                "cfg_scale": cfg_scale,
            }
        }

        if lora_path:
            workflow["params"]["lora_path"] = lora_path
            workflow["params"]["lora_strength"] = 0.8

        # Execute ComfyUI workflow
        result = comfy_service.execute_workflow(workflow)

        # Extract image URLs
        image_urls = []
        for img in result.get("images", []):
            image_urls.append(img["url"])

        update_job_progress(job_id, 100, JobStatus.COMPLETED)

        return {
            "job_id": job_id,
            "status": "completed",
            "images": image_urls
        }

    except Exception as e:
        logger.error(f"Image generation failed: {e}")
        update_job_progress(job_id, 0, JobStatus.FAILED)
        raise


@celery_app.task(bind=True, name="generate_video")
def generate_video_task(
    self,
    job_id: int,
    scene_id: int,
    image_url: str,
    duration: float = 3.0,
    fps: int = 24,
    motion_scale: float = 1.0,
    enable_lipsync: bool = False,
    audio_url: Optional[str] = None
):
    """Async task for video generation"""
    logger.info(f"Starting video generation task for job {job_id}")

    try:
        update_job_progress(job_id, 0, JobStatus.PROCESSING)

        # Build workflow
        workflow = {
            "template": "video_generation",
            "params": {
                "image_url": image_url,
                "duration": duration,
                "fps": fps,
                "motion_scale": motion_scale,
                "enable_lipsync": enable_lipsync,
                "audio_url": audio_url
            }
        }

        # Execute ComfyUI workflow
        result = comfy_service.execute_workflow(workflow)

        # Extract video URLs
        video_urls = []
        for vid in result.get("videos", []):
            video_urls.append(vid["url"])

        update_job_progress(job_id, 100, JobStatus.COMPLETED)

        return {
            "job_id": job_id,
            "status": "completed",
            "videos": video_urls
        }

    except Exception as e:
        logger.error(f"Video generation failed: {e}")
        update_job_progress(job_id, 0, JobStatus.FAILED)
        raise


@celery_app.task(bind=True, name="train_character_lora")
def train_character_lora_task(
    self,
    job_id: int,
    character_id: int,
    reference_images: List[str],
    training_epochs: int = 100,
    learning_rate: float = 0.0001,
    batch_size: int = 1
):
    """Async task for character LoRA training"""
    logger.info(f"Starting LoRA training task for character {character_id}")

    try:
        update_job_progress(job_id, 0, JobStatus.PROCESSING)

        training_config = {
            "training_epochs": training_epochs,
            "learning_rate": learning_rate,
            "batch_size": batch_size
        }

        # Use character service to train LoRA
        result = character_service.train_lora(
            character_id=character_id,
            reference_images=reference_images,
            training_config=training_config
        )

        update_job_progress(job_id, 100, JobStatus.COMPLETED)

        return {
            "job_id": job_id,
            "status": "completed",
            "lora_path": result["lora_model_path"]
        }

    except Exception as e:
        logger.error(f"LoRA training failed: {e}")
        update_job_progress(job_id, 0, JobStatus.FAILED)
        raise


@celery_app.task(bind=True, name="batch_generate_scenes")
def batch_generate_scenes_task(
    self,
    job_id: int,
    project_id: int,
    scene_ids: List[int],
    batch_size: int = 4
):
    """Async task for batch scene image generation"""
    logger.info(f"Starting batch generation for {len(scene_ids)} scenes")

    try:
        update_job_progress(job_id, 0, JobStatus.PROCESSING)

        # Process scenes in batches
        results = []
        total_scenes = len(scene_ids)

        for i, scene_id in enumerate(scene_ids):
            # TODO: Fetch scene data from database
            # scene = get_scene(scene_id)
            # result = generate_image_task.delay(...)
            # results.append(result)

            progress = int((i + 1) / total_scenes * 100)
            update_job_progress(job_id, progress)

        update_job_progress(job_id, 100, JobStatus.COMPLETED)

        return {
            "job_id": job_id,
            "status": "completed",
            "results": results
        }

    except Exception as e:
        logger.error(f"Batch generation failed: {e}")
        update_job_progress(job_id, 0, JobStatus.FAILED)
        raise
