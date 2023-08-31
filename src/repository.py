# file src/repository.py
import io

import boto3

from src.config import settings


class S3Repository:
    def __init__(self):
        self.s3 = boto3.client("s3")

    def upload_original_image(self, file_contents, filename):
        self.s3.upload_fileobj(
            io.BytesIO(file_contents), settings.AWS_BUCKET_NAME, filename
        )

    def upload_compressed_image(self, compressed_image_data, filename):
        self.s3.upload_fileobj(
            io.BytesIO(compressed_image_data), settings.AWS_BUCKET_NAME, filename
        )

    def generate_presigned_url(self, filename: str) -> str:

        presigned_url = self.s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.AWS_BUCKET_NAME, "Key": filename},
            ExpiresIn=3600,  # URL expiration time in seconds
        )
        return presigned_url

# end of file src/repository.py