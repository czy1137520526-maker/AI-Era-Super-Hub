"""Character-related schemas"""
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List


class CharacterBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    role: str = "protagonist"  # protagonist, antagonist, supporting, etc.


class CharacterCreate(CharacterBase):
    project_id: int


class CharacterUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    role: Optional[str] = None
    lora_model_path: Optional[str] = None
    is_trained: Optional[bool] = None


class CharacterInDB(CharacterBase):
    id: int
    project_id: int
    lora_model_path: Optional[str] = None
    is_trained: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Character(CharacterInDB):
    pass


class CharacterDetail(Character):
    asset_count: int = 0
    scene_appearances: int = 0


class LoraTrainingJob(BaseModel):
    character_id: int
    reference_images: List[str]
    training_epochs: int = 100
    learning_rate: float = 0.0001
