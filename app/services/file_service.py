import os
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile
from fastapi.responses import StreamingResponse, FileResponse

from app.config import settings
from app.models.schemas import FileUploadResponse
from app.utils.file_utils import validate_file_type, get_file_path, get_mime_type
from app.utils.image_utils import resize_image_preview, extract_video_preview


async def upload_file(file: UploadFile) -> FileUploadResponse:
    file_type = validate_file_type(file)

    file_id = str(uuid.uuid4())
    file_extension = Path(file.filename).suffix or (".jpg" if file_type == "image" else ".mp4")
    file_path = os.path.join(settings.MEDIA_DIR, f"{file_id}{file_extension}")

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return FileUploadResponse(file_id=file_id, type=file_type)


async def get_file_content(file_id: str, width: int = None, height: int = None):
    try:
        file_path = get_file_path(file_id)
        mime = get_mime_type(file_path)

        if width or height:
            if mime in settings.SUPPORTED_IMAGE_TYPES:
                img_io = resize_image_preview(file_path, width, height)
            elif mime in settings.SUPPORTED_VIDEO_TYPES:
                img_io = extract_video_preview(file_path, width, height)
            else:
                raise HTTPException(status_code=400, detail="Превью доступно только для изображений и видео")

            return StreamingResponse(
                img_io,
                media_type="image/jpeg",
                headers={"Content-Disposition": f"inline; filename={file_id}_preview.jpg"}
            )

        return FileResponse(file_path, media_type=mime, filename=file_path.name)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")
