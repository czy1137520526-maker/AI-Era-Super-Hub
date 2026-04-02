"""Script generation schemas"""
from pydantic import BaseModel, Field
from typing import Optional, List


class ScriptGenerationRequest(BaseModel):
    project_id: int
    input_text: str = Field(..., min_length=10)
    style: Optional[str] = "comic"
    num_scenes: Optional[int] = Field(default=10, ge=1, le=50)
    tone: Optional[str] = "dramatic"


class ScriptScene(BaseModel):
    scene_id: int
    description: str
    characters: List[str]
    emotion: str
    camera_angle: str
    dialogue: List[dict]


class ScriptGenerationResponse(BaseModel):
    project_id: int
    scenes: List[ScriptScene]
    total_scenes: int


class ScriptFromLLM(BaseModel):
    """Schema for LLM output"""
    scenes: List[dict]
    metadata: Optional[dict] = None
