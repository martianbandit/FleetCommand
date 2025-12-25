import uuid
from sqlalchemy import Column, Enum, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.base import Base
from app.db.models.work_order import WorkOrderStatus

class WorkOrderStatusHistory(Base):
    __tablename__ = "work_order_status_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    work_order_id = Column(UUID(as_uuid=True), ForeignKey("work_orders.id"), nullable=False)
    changed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    old_status = Column(Enum(WorkOrderStatus), nullable=False)
    new_status = Column(Enum(WorkOrderStatus), nullable=False)

    changed_at = Column(DateTime(timezone=True), server_default=func.now())
