from datetime import datetime

from fastapi import APIRouter, HTTPException, UploadFile, status
from fastapi.responses import FileResponse as FastAPIFileResponse
from pydantic import BaseModel, ConfigDict

from app.modules.files.service import FileRecord, get_file, list_files, save_upload

router = APIRouter(prefix="/files", tags=["files"])


class StoredFileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    filename: str
    content_type: str | None
    size: int
    uploaded_at: datetime


@router.post("", response_model=StoredFileResponse, status_code=status.HTTP_201_CREATED)
def upload_file(file: UploadFile) -> StoredFileResponse:
    record = save_upload(file)
    return StoredFileResponse.model_validate(record)


@router.get("", response_model=list[StoredFileResponse])
def list_uploaded_files() -> list[StoredFileResponse]:
    return [StoredFileResponse.model_validate(record) for record in list_files()]


@router.get("/{file_id}")
def download_file(file_id: str) -> FastAPIFileResponse:
    record = get_file(file_id)
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    return FastAPIFileResponse(path=record.path, filename=record.filename, media_type=record.content_type)
