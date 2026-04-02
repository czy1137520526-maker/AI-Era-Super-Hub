"""RenderJob ORM model"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, Integer as SQLInteger
from sqlalchemy.orm import relationship
from app.db.session import Base


class RenderJob(Base):
    __tablename__ = "render_jobs"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    scene_id = Column(Integer, ForeignKey("scenes.id"), nullable=True)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=True)
    job_type = Column(String(50), nullable=False)  # image_generation, video_generation, lora_training, etc.
    status = Column(String(50), default="pending")  # pending, processing, completed, failed, cancelled
    progress = Column(SQLInteger, default=0)
    parameters = Column(JSON, nullable=True)
    result_url = Column(String, nullable=True)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="render_jobs")
    scene = relationship("Scene", back_populates="render_jobs")
    character = relationship("Character", back_populates="render_jobs")
