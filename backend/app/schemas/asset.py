"""Asset and storage schemas"""
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class AssetType(str, Enum):
    CHARACTER = "character"
    BACKGROUND = "background"
    PROP = "prop"
    REFERENCE = "reference"


class AssetBase(BaseModel):
    asset_type: AssetType
    name: str
    description: Optional[str] = None
    file_path: str
    metadata: Optional[dict] = None


class AssetCreate(AssetBase):
    project_id: int
    character_id: Optional[int] = None


class AssetInDB(AssetBase):
    id: int
    project_id: int
    character_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class Asset(AssetInDB):
    pass


class AssetUploadResponse(BaseModel):
    asset_id: int
    file_url: str
    file_path: str
    uploaded_at: datetime


class PresignedUrlRequest(BaseModel):
    file_name: str
    file_type: str
    asset_type: AssetType


class PresignedUrlResponse(BaseModel):
    upload_url: str
    file_path: str
    expires_in: int
