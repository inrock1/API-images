from src.repository import S3Repository
from src.services.image_service import ImageService


def get_image_service() -> ImageService:
    s3_repository = S3Repository()
    service = ImageService(s3_repository)
    return service
