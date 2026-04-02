"""Project-related schemas"""
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    style_preset: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[str] = None
    style_preset: Optional[str] = None


class ProjectInDB(ProjectBase):
    id: int
    user_id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Project(ProjectInDB):
    pass


class ProjectDetail(Project):
    characters_count: int = 0
    scenes_count: int = 0
    render_jobs_count: int = 0
