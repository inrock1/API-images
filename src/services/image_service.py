# file src/service.py
import io
import os

from botocore.exceptions import NoCredentialsError
from fastapi import HTTPException, UploadFile, status

from src.config import settings
from src.repository import S3Repository
from src.tasks import celery_app


class ImageService:
    def __init__(self):
        self.s3_repository = S3Repository
        self.quality_levels = [75, 50, 25]

    async def download_image_url(self, filename: str, quality: int) -> str:
        if quality in self.quality_levels:
            file_name, file_extension = os.path.splitext(filename)
            filename = f"{file_name}_{quality}{file_extension}"
        presigned_url = self.s3_repository.generate_presigned_url(filename)
        return presigned_url

    async def upload_image(self, file: UploadFile) -> dict:
        if not file:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="No file provided"
            )

        if file.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only jpeg and png images allowed",
            )

        file_contents = await file.read()

        # Check file size
        size = len(file_contents)
        print("size: ", size)
        if not 0 < size < 2 * settings.MB:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size should not exceed 2MB",
            )

        try:
            self.s3_repository.upload_original_image(file_contents, file.filename)
            await self.queue_image_optimization(file_contents, file.filename)

            return {"message": "Image uploaded successfully"}
        except NoCredentialsError:
            return {"error": "No AWS credentials found"}

    async def queue_image_optimization(self, file_contents: bytes, filename: str):
        file_name, file_extension = os.path.splitext(filename)

        for quality in self.quality_levels:
            compressed_filename = f"{file_name}_{quality}{file_extension}"

            celery_app.send_task(
                "src.tasks.optimize_image",
                args=[compressed_filename, file_contents, quality],
            )

        return {"message": "Image optimization queued"}


# end of file src/service.py
