from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.db.models.repair_request import RepairRequestStatus


class RepairRequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    vehicle_id: str
    driver_id: str
    description: str
    status: RepairRequestStatus
    created_at: datetime | None = None
