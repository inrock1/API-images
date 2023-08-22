from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import os
import boto3
from botocore.exceptions import NoCredentialsError

from src.config import settings

app = FastAPI()


@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    try:
        s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
        s3.upload_fileobj(file.file, settings.AWS_BUCKET_NAME, file.filename)
        return JSONResponse(content={"message": "Image uploaded successfully"})
    except NoCredentialsError:
        return JSONResponse(content={"error": "No AWS credentials found"})



@app.get("/")
async def root():
    return {"message": "File upload root page 🎬"}


