import enum
import uuid

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base

class WorkOrderStatus(str, enum.Enum):
    open = "open"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"

class WorkOrder(Base):
    __tablename__ = "work_orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    repair_request_id = Column(UUID(as_uuid=True), ForeignKey("repair_requests.id"), nullable=True)
    assigned_to_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    summary = Column(Text, nullable=False)
    status = Column(Enum(WorkOrderStatus), default=WorkOrderStatus.open)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    repair_request = relationship("RepairRequest", back_populates="work_order")
    assigned_to = relationship("User", back_populates="assigned_work_orders")
    status_history = relationship("WorkOrderStatusHistory", back_populates="work_order")
