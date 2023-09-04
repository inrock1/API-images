# src/tasks.py
import io

from celery import Celery
from PIL import Image

from src.config import settings
from src.repository import S3Repository
from src.utils import resize_and_compress_image

s3_repository = S3Repository()

celery_app = Celery(
    "tasks",
    broker=settings.RABBITMQ_URL,
    backend="rpc://",
)


@celery_app.task(name="src.tasks.optimize_image")
def optimize_image(filename: str, file_contents: bytes, quality: int):
    image = Image.open(io.BytesIO(file_contents))
    compressed_image_data = resize_and_compress_image(image, quality)
    s3_repository.upload_compressed_image(compressed_image_data, filename)
    print(f"Optimized image {filename} with quality {quality}")

# end of file src/tasks.py