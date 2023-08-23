import json
from unittest.mock import patch

import boto3
from fastapi.testclient import TestClient
from moto import mock_s3, mock_sqs

from src.main import app
from src.config import settings

client = TestClient(app)


# @patch("src.config.settings", AWS_ACCESS_KEY='testing', AWS_SECRET_KEY='testing', AWS_BUCKET_NAME='test-bucket34')
def test_upload_image():
    response = client.post("/upload/", files={"file": ("test_image.jpg", open("test_image.jpg", "rb"))})
    assert response.status_code == 200
    assert response.json() == {"message": "Image uploaded successfully"}


def test_download_image():
    response = client.get("/download/1.jpg")
    assert response.status_code == 200
    assert "download_url" in response.json()

@mock_s3
def test_upload_image2():
    # Create a mock S3 bucket
    mock_bucket_name = "mock-bucket"
    s3 = boto3.client("s3")
    s3.create_bucket(Bucket=mock_bucket_name)

    # Perform the upload_image request
    response = client.post("/upload/", files={"file": ("test_image.jpg", open("tests/test_image.jpg", "rb"))})
    assert response.status_code == 200
    assert response.json() == {"message": "Image uploaded successfully"}
