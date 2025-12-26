from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    title: str
    message: str
    created_at: datetime
    payload: dict[str, Any]
    read_at: datetime | None = None
