"""
Core configuration settings for ManjuFlow AI backend.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""

    # Application
    APP_NAME: str = "ManjuFlow AI"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "your-secret-key-change-in-production"

    # Server
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://manju:manju123@localhost:5432/manjuflow"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # MinIO
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "manjuflow-assets"
    MINIO_SECURE: bool = False

    # ComfyUI
    COMFYUI_URL: str = "http://localhost:8188"
    COMFYUI_CLIENT_ID: str = "manjuflow-client"
    COMFYUI_WORKFLOWS_DIR: str = "./comfyui/workflows"
    COMFYUI_CUSTOM_NODES_DIR: str = "./comfyui/custom_nodes"
    COMFYUI_OUTPUT_DIR: str = "./comfyui/output"

    # LLM Configuration
    LLM_PROVIDER: str = "qwen"  # qwen, deepseek, openai
    QWEN_API_KEY: Optional[str] = None
    QWEN_BASE_URL: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    DEEPSEEK_API_KEY: Optional[str] = None
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com/v1"
    OPENAI_API_KEY: Optional[str] = None

    # LoRA Training
    LORA_OUTPUT_DIR: str = "./lora_models"
    LORA_TRAINING_DATASET_DIR: str = "./training_datasets"

    # Vector Database
    PINECONE_API_KEY: Optional[str] = None
    PINECONE_ENVIRONMENT: str = "us-west1-gcp"
    PINECONE_INDEX: str = "manjuflow-assets"

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
    ]

    # File Upload
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_IMAGE_FORMATS: list[str] = ["jpg", "jpeg", "png", "webp"]
    ALLOWED_VIDEO_FORMATS: list[str] = ["mp4", "mov", "webm"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
