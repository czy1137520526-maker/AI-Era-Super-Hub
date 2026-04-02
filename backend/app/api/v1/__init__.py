"""API v1 module exports"""
from fastapi import APIRouter
from app.api.v1 import scripts, characters, render

api_router = APIRouter()

# Include all sub-routers
api_router.include_router(scripts.router, prefix="/scripts", tags=["scripts"])
api_router.include_router(characters.router, prefix="/characters", tags=["characters"])
api_router.include_router(render.router, prefix="/render", tags=["render"])

__all__ = ["api_router"]
