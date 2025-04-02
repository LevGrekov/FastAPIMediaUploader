from pathlib import Path

import magic
from fastapi import HTTPException, UploadFile

from app.config import settings


def determine_mime_type(content: bytes) -> str:
    try:
        return magic.from_buffer(content, mime=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка определения типа файла: {str(e)}")


def validate_file_type(file: UploadFile) -> str:
    content = file.file.read(2048)
    file.file.seek(0)

    mime = determine_mime_type(content)

    if mime in settings.SUPPORTED_IMAGE_TYPES:
        return "image"
    elif mime in settings.SUPPORTED_VIDEO_TYPES:
        return "video"

    raise HTTPException(
        status_code=400,
        detail=f"Неподдерживаемый тип файла: {mime}. Разрешены только изображения и видео."
    )


def get_mime_type(file_path: str) -> str:
    try:
        with open(file_path, 'rb') as f:
            content = f.read(2048)
        return determine_mime_type(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка определения типа файла: {str(e)}")


def get_file_path(file_id: str):
    media_dir = Path(settings.MEDIA_DIR)
    matched_files = list(media_dir.glob(f"{file_id}.*"))
    if not matched_files:
        raise HTTPException(status_code=404, detail="Файл не найден")
    return matched_files[0]
