# file src/main.py
from fastapi import Depends, FastAPI, File, Path, Query, UploadFile
from fastapi.responses import JSONResponse

from src.services.get_service import get_image_service
from src.services.image_service import ImageService

app = FastAPI()


@app.post("/upload/")
async def upload_image(
    file: UploadFile = File(...),
    image_service: ImageService = Depends(get_image_service),
):
    response = await image_service.upload_image(file)

    return response


@app.get("/download/{filename}")
async def download_image(
    filename: str = Path(
        ...,
        description="Filename of the image with extension",
        regex=".+\.(jpg|jpeg|png)$",
    ),
    quality: int = Query(
        default=100, description="Image quality level (25, 50, 75, or 100 %)"
    ),
    image_service: ImageService = Depends(get_image_service),
):
    if quality not in [25, 50, 75, 100]:
        return JSONResponse(
            content={"error": "Invalid quality level. Choose from 25, 50, 75, or 100."},
            status_code=400,
        )

    try:
        presigned_url = await image_service.download_image_url(filename, quality)
        return JSONResponse(content={"download_url": presigned_url})
    except Exception as e:
        return JSONResponse(content={"error": str(e)})


@app.get("/")
async def root():
    return {"message": "File upload root page 🎬"}


# end of file src/main.py
