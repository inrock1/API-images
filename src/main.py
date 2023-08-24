# file src/main.py
import boto3
from fastapi import Depends, FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

from src.config import settings
from src.service import ImageService

app = FastAPI()

KB = 1024
MB = KB * KB


@app.post("/upload/", response_model=dict)
async def upload_image(
    file: UploadFile = File(...), image_service: ImageService = Depends()
):
    response = await image_service.upload_image(file)
    return response


@app.get("/download/{filename}")
async def download_image(filename: str):
    try:
        s3 = boto3.client("s3")
        presigned_url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.AWS_BUCKET_NAME, "Key": filename},
            ExpiresIn=3600,  # URL expiration time in seconds
        )

        return JSONResponse(content={"download_url": presigned_url})
    except Exception as e:
        return JSONResponse(content={"error": str(e)})


@app.get("/")
async def root():
    return {"message": "File upload root page 🎬"}


# end of file src/main.py
