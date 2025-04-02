import io

from PIL import Image
from fastapi import HTTPException
from moviepy import VideoFileClip


def resize_image(img, width=None, height=None):
    try:
        if width and not height:
            ratio = width / float(img.size[0])
            height = int(float(img.size[1]) * float(ratio))
        elif height and not width:
            ratio = height / float(img.size[1])
            width = int(float(img.size[0]) * float(ratio))

        img = img.resize((width, height), Image.LANCZOS)

        img_io = io.BytesIO()
        img.save(img_io, format='JPEG', quality=85)
        img_io.seek(0)
        return img_io
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации превью: {str(e)}")


def extract_video_preview(file_path, width, height):
    try:
        video = VideoFileClip(str(file_path))
        img = video.get_frame(0)
        img = Image.fromarray(img)
        return resize_image(img, width, height)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации превью: {str(e)}")


def resize_image_preview(file_path, width, height):
    try:
        img = Image.open(file_path)
        return resize_image(img, width, height)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации превью: {str(e)}")
