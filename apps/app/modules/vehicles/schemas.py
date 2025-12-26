from datetime import datetime
from pydantic import BaseModel, ConfigDict


class VehicleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    vin: str
    license_plate: str
    make: str
    model: str
    year: int
    status: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
