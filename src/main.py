# file src/main.py
import io

import boto3
from botocore.exceptions import NoCredentialsError
from fastapi import FastAPI, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from PIL import Image

from src.config import settings
from src.utils import resize_and_compress_image

app = FastAPI()

KB = 1024
MB = KB * KB

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file provided")

    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only jpeg and png images allowed")

    file_contents = await file.read()

    # Check file size
    size = len(file_contents)
    print("size: ", size)
    if not 0 < size < 2 * MB:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File size should not exceed 2MB")

    try:
        s3 = boto3.client('s3')

        # Upload the original image to S3
        s3.upload_fileobj(io.BytesIO(file_contents), settings.AWS_BUCKET_NAME, file.filename)

        # Read the contents of the uploaded file into a BytesIO object
        image = Image.open(io.BytesIO(file_contents))

        # Resize and compress the uploaded image
        quality_levels = [75, 50, 25]
        for quality in quality_levels:
            compressed_image_data = resize_and_compress_image(image, quality)
            s3.upload_fileobj(io.BytesIO(compressed_image_data), settings.AWS_BUCKET_NAME,
                              f"{file.filename}_{quality}.jpg")

        return JSONResponse(content={"message": "Image uploaded successfully"})
    except NoCredentialsError:
        return JSONResponse(content={"error": "No AWS credentials found"})


@app.get("/download/{filename}")
async def download_image(filename: str):
    try:
        s3 = boto3.client('s3')
        presigned_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': settings.AWS_BUCKET_NAME, 'Key': filename},
            ExpiresIn=3600  # URL expiration time in seconds
        )

        return JSONResponse(content={"download_url": presigned_url})
    except Exception as e:
        return JSONResponse(content={"error": str(e)})



@app.get("/")
async def root():
    return {"message": "File upload root page 🎬"}

# end of file src/main.py