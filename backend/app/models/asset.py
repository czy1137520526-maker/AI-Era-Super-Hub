"""Asset ORM model"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.db.session import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=True)
    asset_type = Column(String(50), nullable=False)  # character, background, prop, reference
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    file_path = Column(String, nullable=False)
    file_url = Column(String, nullable=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="assets")
    character = relationship("Character", back_populates="assets")
