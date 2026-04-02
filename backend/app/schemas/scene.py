"""Scene-related schemas"""
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class Dialogue(BaseModel):
    speaker: str
    text: str
    emotion: Optional[str] = None


class SceneBase(BaseModel):
    scene_number: int
    description: str
    characters: List[str] = []
    emotion: Optional[str] = None
    camera_angle: Optional[str] = None
    dialogue: Optional[List[Dialogue]] = None
    duration_seconds: Optional[int] = 3


class SceneCreate(SceneBase):
    project_id: int


class SceneUpdate(BaseModel):
    scene_number: Optional[int] = None
    description: Optional[str] = None
    characters: Optional[List[str]] = None
    emotion: Optional[str] = None
    camera_angle: Optional[str] = None
    dialogue: Optional[List[Dialogue]] = None
    duration_seconds: Optional[int] = None
    generated_image_url: Optional[str] = None
    generated_video_url: Optional[str] = None


class SceneInDB(SceneBase):
    id: int
    project_id: int
    generated_image_url: Optional[str] = None
    generated_video_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Scene(SceneInDB):
    pass


class SceneReorder(BaseModel):
    scene_ids: List[int]


class SceneBatchGenerate(BaseModel):
    scene_ids: List[int]
    batch_size: int = 4
