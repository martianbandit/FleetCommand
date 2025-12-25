from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.models.work_order import WorkOrder, WorkOrderStatus
from app.db.models.work_order_status_history import WorkOrderStatusHistory

ALLOWED_TRANSITIONS: dict[WorkOrderStatus, set[WorkOrderStatus]] = {
    WorkOrderStatus.open: {WorkOrderStatus.in_progress, WorkOrderStatus.cancelled},
    WorkOrderStatus.in_progress: {WorkOrderStatus.completed, WorkOrderStatus.cancelled},
    WorkOrderStatus.completed: set(),
    WorkOrderStatus.cancelled: set(),
}


def is_transition_allowed(current: WorkOrderStatus, new_status: WorkOrderStatus) -> bool:
    if current == new_status:
        return True
    return new_status in ALLOWED_TRANSITIONS.get(current, set())


def require_valid_transition(current: WorkOrderStatus, new_status: WorkOrderStatus) -> None:
    if not is_transition_allowed(current, new_status):
        raise ValueError(f"Transition from {current.value} to {new_status.value} is not allowed")


def apply_status_transition(
    db: Session,
    work_order: WorkOrder,
    new_status: WorkOrderStatus,
    changed_by: str,
) -> WorkOrder:
    require_valid_transition(work_order.status, new_status)

    if work_order.status == new_status:
        return work_order

    history = WorkOrderStatusHistory(
        work_order_id=work_order.id,
        changed_by=changed_by,
        old_status=work_order.status,
        new_status=new_status,
    )
    work_order.status = new_status
    if new_status == WorkOrderStatus.completed:
        work_order.completed_at = datetime.now(timezone.utc)

    db.add(history)
    db.add(work_order)
    db.commit()
    db.refresh(work_order)
    return work_order
