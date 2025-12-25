from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.repair_request import RepairRequest
from app.db.models.user import User, UserRole
from app.db.models.work_order import WorkOrder


def list_work_orders(db: Session, user: User) -> list[WorkOrder]:
    stmt = select(WorkOrder)
    if user.role == UserRole.mechanic:
        stmt = stmt.where(WorkOrder.technician_id == user.id)
    elif user.role == UserRole.driver:
        stmt = (
            stmt.join(RepairRequest, RepairRequest.id == WorkOrder.repair_request_id)
            .where(RepairRequest.driver_id == user.id)
        )
    return list(db.execute(stmt).scalars().all())
