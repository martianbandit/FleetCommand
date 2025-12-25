from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.repair_request import RepairRequest
from app.db.models.user import User, UserRole
from app.db.models.vehicle import Vehicle


def list_vehicles(db: Session, user: User) -> list[Vehicle]:
    if user.role == UserRole.driver:
        stmt = (
            select(Vehicle)
            .join(RepairRequest, RepairRequest.vehicle_id == Vehicle.id)
            .where(RepairRequest.driver_id == user.id)
            .distinct()
        )
    else:
        stmt = select(Vehicle)
    return list(db.execute(stmt).scalars().all())
