from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from app.db.models.repair_request import RepairRequest
from app.db.models.user import User
from app.db.models.work_order import WorkOrder, WorkOrderStatus


@dataclass(frozen=True)
class NotificationEvent:
    id: str
    user_id: str
    title: str
    message: str
    created_at: datetime
    payload: dict[str, Any]
    read_at: datetime | None = None


def _base_payload(work_order: WorkOrder) -> dict[str, Any]:
    return {
        "work_order_id": str(work_order.id),
        "vehicle_id": str(work_order.vehicle_id),
        "status": work_order.status.value,
        "origin": work_order.origin.value,
    }


def _make_event(user_id: str, title: str, message: str, payload: dict[str, Any]) -> NotificationEvent:
    return NotificationEvent(
        id=str(uuid.uuid4()),
        user_id=user_id,
        title=title,
        message=message,
        created_at=datetime.now(timezone.utc),
        payload=payload,
    )


def build_work_order_status_events(
    work_order: WorkOrder,
    changed_by: User,
    previous_status: WorkOrderStatus | None = None,
) -> list[NotificationEvent]:
    title = "Work order update"
    status_segment = work_order.status.value
    if previous_status is not None:
        message = f"Le statut de l'ordre {work_order.id} est passé de {previous_status.value} à {status_segment}."
    else:
        message = f"Le statut de l'ordre {work_order.id} est maintenant {status_segment}."

    payload = _base_payload(work_order)
    events: list[NotificationEvent] = []

    if work_order.technician_id and str(work_order.technician_id) != str(changed_by.id):
        events.append(_make_event(str(work_order.technician_id), title, message, payload))

    if work_order.repair_request and work_order.repair_request.driver_id:
        driver_id = str(work_order.repair_request.driver_id)
        if driver_id != str(changed_by.id):
            events.append(_make_event(driver_id, title, message, payload))

    return events


def build_repair_request_created_event(repair_request: RepairRequest, manager: User) -> NotificationEvent:
    payload = {
        "repair_request_id": str(repair_request.id),
        "vehicle_id": str(repair_request.vehicle_id),
        "driver_id": str(repair_request.driver_id),
        "status": repair_request.status.value,
    }
    message = f"Une nouvelle demande de réparation a été soumise pour le véhicule {repair_request.vehicle_id}."
    return _make_event(str(manager.id), "Repair request", message, payload)
