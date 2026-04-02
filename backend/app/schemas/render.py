"""Render job and generation schemas"""
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum


class JobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class RenderJobBase(BaseModel):
    job_type: str  # image_generation, video_generation, lora_training, etc.
    project_id: int
    scene_id: Optional[int] = None
    character_id: Optional[int] = None


class RenderJobCreate(RenderJobBase):
    parameters: Optional[Dict[str, Any]] = None


class RenderJobUpdate(BaseModel):
    status: Optional[JobStatus] = None
    progress: Optional[int] = Field(None, ge=0, le=100)
    result_url: Optional[str] = None
    error_message: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None


class RenderJobInDB(RenderJobBase):
    id: int
    status: JobStatus
    progress: int = 0
    result_url: Optional[str] = None
    error_message: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class RenderJob(RenderJobInDB):
    pass


class ImageGenerationRequest(BaseModel):
    project_id: int
    scene_id: int
    prompt: str
    negative_prompt: Optional[str] = ""
    width: Optional[int] = 1024
    height: Optional[int] = 1024
    num_inference_steps: Optional[int] = 30
    guidance_scale: Optional[float] = 7.5
    seed: Optional[int] = -1


class VideoGenerationRequest(BaseModel):
    project_id: int
    scene_id: int
    image_url: str
    duration: Optional[float] = 3.0
    fps: Optional[int] = 24
    motion_scale: Optional[float] = 1.0
    enable_lipsync: Optional[bool] = False
    audio_url: Optional[str] = None


class JobProgress(BaseModel):
    job_id: int
    status: JobStatus
    progress: int
    message: Optional[str] = None
    result_url: Optional[str] = None
