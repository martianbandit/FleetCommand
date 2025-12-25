from __future__ import annotations

import uuid


def generate_uuid() -> str:
    return str(uuid.uuid4())


def is_valid_uuid(value: str, *, version: int | None = None) -> bool:
    try:
        candidate = uuid.UUID(value)
    except (TypeError, ValueError):
        return False
    if version is not None and candidate.version != version:
        return False
    return True


def normalize_uuid(value: str) -> str:
    try:
        return str(uuid.UUID(value))
    except (TypeError, ValueError) as exc:
        raise ValueError("Invalid UUID value") from exc


def coerce_uuid(value: str | uuid.UUID) -> uuid.UUID:
    if isinstance(value, uuid.UUID):
        return value
    try:
        return uuid.UUID(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("Invalid UUID value") from exc
