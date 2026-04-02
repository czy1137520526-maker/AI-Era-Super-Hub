"""
MinIO object storage client.
"""
from minio import Minio
from minio.error import S3Error
from app.core.config import settings
from io import BytesIO
from typing import Optional
import uuid


class MinIOClient:
    """MinIO client wrapper."""

    def __init__(self):
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE,
        )
        self.bucket = settings.MINIO_BUCKET
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        """Ensure the bucket exists."""
        try:
            if not self.client.bucket_exists(self.bucket):
                self.client.make_bucket(self.bucket)
        except S3Error as e:
            console.error(f"MinIO bucket error: {e}")

    def upload_file(
        self,
        file_data: bytes,
        filename: Optional[str] = None,
        content_type: str = "application/octet-stream",
    ) -> str:
        """Upload file to MinIO."""
        if not filename:
            filename = f"{uuid.uuid4()}.bin"

        file_path = f"{filename}"
        self.client.put_object(
            self.bucket,
            file_path,
            BytesIO(file_data),
            length=len(file_data),
            content_type=content_type,
        )
        return file_path

    def get_file_url(self, file_path: str) -> str:
        """Get public URL for file."""
        return f"http://{settings.MINIO_ENDPOINT}/{self.bucket}/{file_path}"

    def delete_file(self, file_path: str) -> bool:
        """Delete file from MinIO."""
        try:
            self.client.remove_object(self.bucket, file_path)
            return True
        except S3Error:
            return False


minio_client = MinIOClient()
