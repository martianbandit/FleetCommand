import uuid
import enum
from sqlalchemy import Column, Text, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class WorkOrderStatus(str, enum.Enum):
    open = "open"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"

class WorkOrderOrigin(str, enum.Enum):
    driver_request = "driver_request"
    manual = "manual"

class WorkOrder(Base):
    __tablename__ = "work_orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.id"), nullable=False)
    technician_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    repair_request_id = Column(UUID(as_uuid=True), ForeignKey("repair_requests.id"), nullable=True)

    description = Column(Text, nullable=False)
    status = Column(Enum(WorkOrderStatus), default=WorkOrderStatus.open)
    origin = Column(Enum(WorkOrderOrigin), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    vehicle = relationship("Vehicle")
    technician = relationship("User")
    repair_request = relationship("RepairRequest")
