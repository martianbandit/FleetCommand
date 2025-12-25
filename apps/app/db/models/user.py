import enum
import uuid

from sqlalchemy import Column, DateTime, Enum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base

class UserRole(str, enum.Enum):
    driver = "driver"
    mechanic = "mechanic"
    manager = "manager"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    assigned_work_orders = relationship("WorkOrder", back_populates="assigned_to")
