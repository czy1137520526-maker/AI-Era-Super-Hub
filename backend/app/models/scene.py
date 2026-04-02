"""Scene ORM model"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, Integer as SQLInteger
from sqlalchemy.orm import relationship
from app.db.session import Base


class Scene(Base):
    __tablename__ = "scenes"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    scene_number = Column(SQLInteger, nullable=False)
    description = Column(Text, nullable=False)
    characters = Column(JSON, nullable=True)  # List of character names
    emotion = Column(String(50), nullable=True)
    camera_angle = Column(String(50), nullable=True)
    dialogue = Column(JSON, nullable=True)  # List of dialogue objects
    duration_seconds = Column(SQLInteger, default=3)
    generated_image_url = Column(String, nullable=True)
    generated_video_url = Column(String, nullable=True)
    generation_config = Column(JSON, nullable=True)  # Generation parameters
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="scenes")
    render_jobs = relationship("RenderJob", back_populates="scene", cascade="all, delete-orphan")
