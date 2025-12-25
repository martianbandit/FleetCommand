import uuid
import enum
from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, synonym
from sqlalchemy.sql import func
from app.db.base import Base

class RepairRequestPriority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class RepairRequestStatus(str, enum.Enum):
    submitted = "submitted"
    converted = "converted"
    rejected = "rejected"

class RepairRequest(Base):
    __tablename__ = "repair_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.id"), nullable=False)
    reported_by_id = Column("driver_id", UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    description = Column(Text, nullable=False)
    priority = Column(Enum(RepairRequestPriority), nullable=False)
    status = Column(Enum(RepairRequestStatus), default=RepairRequestStatus.submitted)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    vehicle = relationship("Vehicle")
    reported_by = relationship("User")
    work_orders = relationship("WorkOrder", back_populates="repair_request")

    driver_id = synonym("reported_by_id")
