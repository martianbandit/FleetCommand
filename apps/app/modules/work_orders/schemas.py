from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.db.models.work_order import WorkOrderOrigin, WorkOrderStatus


class WorkOrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    vehicle_id: str
    technician_id: str | None = None
    repair_request_id: str | None = None
    description: str
    status: WorkOrderStatus
    origin: WorkOrderOrigin
    created_at: datetime | None = None
    completed_at: datetime | None = None
