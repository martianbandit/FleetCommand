from __future__ import annotations

import os
import shutil
import threading
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from fastapi import UploadFile

STORAGE_DIR = Path(os.getenv("FILE_STORAGE_PATH", "/tmp/fleetcommand_uploads"))


@dataclass(frozen=True)
class FileRecord:
    id: str
    filename: str
    content_type: str | None
    path: Path
    size: int
    uploaded_at: datetime


_STORAGE_LOCK = threading.Lock()
_FILES_INDEX: dict[str, FileRecord] = {}


def _ensure_storage() -> None:
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)


def save_upload(file: UploadFile) -> FileRecord:
    _ensure_storage()
    file_id = str(uuid.uuid4())
    destination = STORAGE_DIR / f"{file_id}_{file.filename}"
    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    size = destination.stat().st_size
    record = FileRecord(
        id=file_id,
        filename=file.filename,
        content_type=file.content_type,
        path=destination,
        size=size,
        uploaded_at=datetime.now(timezone.utc),
    )
    with _STORAGE_LOCK:
        _FILES_INDEX[file_id] = record
    return record


def list_files() -> list[FileRecord]:
    with _STORAGE_LOCK:
        return sorted(_FILES_INDEX.values(), key=lambda item: item.uploaded_at, reverse=True)


def get_file(file_id: str) -> FileRecord | None:
    with _STORAGE_LOCK:
        return _FILES_INDEX.get(file_id)
