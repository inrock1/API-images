import io

from botocore.exceptions import NoCredentialsError
from fastapi import HTTPException, UploadFile, status
from PIL import Image

from src.config import settings
from src.repository import S3Repository
from src.utils import resize_and_compress_image


class ImageService:
    def __init__(self, s3_repository: S3Repository):
        self.s3_repository = s3_repository

    def upload_image(self, file: UploadFile):
        if not file:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="No file provided"
            )

        if file.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only jpeg and png images allowed",
            )

        file_contents = file.file.read()

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

            image = Image.open(io.BytesIO(file_contents))

            # Resize and compress the uploaded image
            quality_levels = [75, 50, 25]
            for quality in quality_levels:
                compressed_image_data = resize_and_compress_image(image, quality)
                self.s3_repository.upload_compressed_image(
                    compressed_image_data, f"{file.filename}_{quality}.jpg"
                )

            return {"message": "Image uploaded successfully"}
        except NoCredentialsError:
            return {"error": "No AWS credentials found"}
