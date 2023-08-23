
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse

import boto3
from botocore.exceptions import NoCredentialsError

from src.config import settings

app = FastAPI()

KB = 1024
MB = KB * KB

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file provided")

    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only jpeg and png images allowed")

    content = await file.read()
    size = len(content)
    print("size: ", size)
    file.file.seek(0)

    if not 0 < size < 2 * MB:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File size should not exceed 2MB")

    try:
        s3 = boto3.client('s3')
        s3.upload_fileobj(file.file, settings.AWS_BUCKET_NAME, file.filename)

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


