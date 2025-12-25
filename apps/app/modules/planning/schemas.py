from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.db.models.work_order import WorkOrderOrigin, WorkOrderStatus


class PlanningItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    work_order_id: str
    vehicle_id: str
    description: str
    status: WorkOrderStatus
    origin: WorkOrderOrigin
    technician_id: str | None = None
    planned_date: datetime | None = None
    completed_at: datetime | None = None
