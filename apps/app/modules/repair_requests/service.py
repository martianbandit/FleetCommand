from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.repair_request import RepairRequest
from app.db.models.user import User, UserRole


def list_repair_requests(db: Session, user: User) -> list[RepairRequest]:
    stmt = select(RepairRequest)
    if user.role == UserRole.driver:
        stmt = stmt.where(RepairRequest.driver_id == user.id)
    return list(db.execute(stmt).scalars().all())
