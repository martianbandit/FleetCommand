from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.models.user import User
from app.db.models.work_order import WorkOrder, WorkOrderStatus
from app.modules.planning.schemas import PlanningItem
from app.modules.work_orders.service import list_work_orders


def build_planning_item(work_order: WorkOrder) -> PlanningItem:
    planned_date = work_order.created_at
    if work_order.status == WorkOrderStatus.completed and work_order.completed_at:
        planned_date = work_order.completed_at
    if planned_date is None:
        planned_date = datetime.now(timezone.utc)
    return PlanningItem(
        work_order_id=str(work_order.id),
        vehicle_id=str(work_order.vehicle_id),
        description=work_order.description,
        status=work_order.status,
        origin=work_order.origin,
        technician_id=str(work_order.technician_id) if work_order.technician_id else None,
        planned_date=planned_date,
        completed_at=work_order.completed_at,
    )


def list_planning(db: Session, user: User) -> list[PlanningItem]:
    work_orders = list_work_orders(db, user)
    return [build_planning_item(order) for order in work_orders]
