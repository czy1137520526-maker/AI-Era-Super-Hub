"""Character ORM model"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from app.db.session import Base


class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    role = Column(String(50), default="protagonist")
    lora_model_path = Column(String, nullable=True)
    lora_config = Column(JSON, nullable=True)
    is_trained = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="characters")
    assets = relationship("Asset", back_populates="character", cascade="all, delete-orphan")
    render_jobs = relationship("RenderJob", back_populates="character")
