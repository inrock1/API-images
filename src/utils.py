import io

from PIL import Image


def resize_and_compress_image(image: Image.Image, quality: int) -> bytes:
    resized_image = image.copy()
    resized_image.thumbnail((resized_image.width * quality // 100, resized_image.height * quality // 100))

    compressed_image = io.BytesIO()
    resized_image.save(compressed_image, format="JPEG", quality=quality)
    compressed_image.seek(0)

    return compressed_image.read()