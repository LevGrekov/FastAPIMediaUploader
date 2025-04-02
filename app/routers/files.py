from typing import Optional

from fastapi import APIRouter, UploadFile, File, Query

from app.models.schemas import FileUploadResponse
from app.services.file_service import upload_file, get_file_content

router = APIRouter()


@router.put("/upload", response_model=FileUploadResponse)
async def upload_file_route(file: UploadFile = File(...)):
    return await upload_file(file)


@router.get("/{file_id}")
async def get_file_route(
        file_id: str,
        width: Optional[int] = Query(None, gt=0, le=3840),
        height: Optional[int] = Query(None, gt=0, le=2160)
):
    return await get_file_content(file_id, width, height)
