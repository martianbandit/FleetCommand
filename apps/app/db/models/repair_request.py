import enum
import uuid

from sqlalchemy import Column, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base

class RepairRequestStatus(str, enum.Enum):
    submitted = "submitted"
    converted = "converted"
    rejected = "rejected"

class RepairRequest(Base):
    __tablename__ = "repair_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.id"), nullable=False)
    driver_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    description = Column(Text, nullable=False)
    status = Column(Enum(RepairRequestStatus), default=RepairRequestStatus.submitted)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    vehicle = relationship("Vehicle")
    driver = relationship("User")
    work_order = relationship("WorkOrder", back_populates="repair_request", uselist=False)
