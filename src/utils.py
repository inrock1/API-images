# src/utils.py
import io

from PIL import Image
from fastapi import Depends

from src.repository import S3Repository
from src.services.image_service import ImageService


def resize_and_compress_image(image: Image.Image, quality: int) -> bytes:
    resized_image = image.copy()
    resized_image.thumbnail(
        (resized_image.width * quality // 100, resized_image.height * quality // 100)
    )

    compressed_image = io.BytesIO()
    resized_image.save(compressed_image, format="JPEG", quality=quality)
    compressed_image.seek(0)

    return compressed_image.read()


def get_image_service(s3_repository: S3Repository = Depends()) -> ImageService:
    service = ImageService(s3_repository)
    return service

# end of file src/utils.py
