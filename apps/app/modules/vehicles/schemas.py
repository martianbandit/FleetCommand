from datetime import date, datetime
from pydantic import BaseModel, ConfigDict


class VehicleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    unit_number: str
    vin: str | None = None
    brand: str
    model: str
    year: int
    mileage: int | None = None
    in_service_date: date | None = None
    created_at: datetime | None = None
