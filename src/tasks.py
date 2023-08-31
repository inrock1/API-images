# src/tasks.py
from celery import Celery

from src.config import settings
from src.utils import resize_and_compress_image
from src.repository import S3Repository
from PIL import Image
import io

s3_repository = S3Repository()

celery_app = Celery(
    "tasks",
    broker=settings.RABBITMQ_URL,
    backend="rpc://",
)

@celery_app.task(name="src.tasks.optimize_image")
def optimize_image(filename, file_contents: bytes, quality: int):
    image = Image.open(io.BytesIO(file_contents))
    compressed_image_data = resize_and_compress_image(image, quality)
    s3_repository.upload_compressed_image(
        compressed_image_data, f"{filename}_{quality}.jpg"
    )
    print(f"Optimized image {filename} with quality {quality}")

# end of file src/tasks.py
