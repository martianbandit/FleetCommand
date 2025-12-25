from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.db.models.user import User
from app.modules.vehicles.schemas import VehicleResponse
from app.modules.vehicles.service import list_vehicles

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.get("", response_model=list[VehicleResponse])
def get_vehicles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[VehicleResponse]:
    vehicles = list_vehicles(db, current_user)
    return [VehicleResponse.model_validate(vehicle) for vehicle in vehicles]
