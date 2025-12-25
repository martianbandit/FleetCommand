from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr

from app.db.models.user import UserRole


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: EmailStr
    full_name: str
    role: UserRole
    created_at: datetime | None = None
