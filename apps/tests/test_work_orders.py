import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.models.repair_request import RepairRequest, RepairRequestStatus
from app.db.models.user import UserRole
from app.db.models.vehicle import Vehicle
from app.db.models.work_order import WorkOrder, WorkOrderOrigin, WorkOrderStatus


def _create_vehicle(db_session: Session, vin: str) -> Vehicle:
    vehicle = Vehicle(
        id=uuid.uuid4(),
        vin=vin,
        license_plate=f"PLATE-{vin[-3:]}",
        make="Peugeot",
        model="Partner",
        year=2021,
        status="active",
        created_at=datetime.now(timezone.utc),
    )
    db_session.add(vehicle)
    db_session.commit()
    db_session.refresh(vehicle)
    return vehicle


def test_list_work_orders_by_role(client, db_session: Session, create_user, auth_headers) -> None:
    driver = create_user("driver2@example.com", role=UserRole.driver)
    mechanic = create_user("mechanic@example.com", role=UserRole.mechanic)
    manager = create_user("manager2@example.com", role=UserRole.manager)

    vehicle = _create_vehicle(db_session, "VIN999")
    repair_request = RepairRequest(
        id=uuid.uuid4(),
        vehicle_id=vehicle.id,
        driver_id=driver.id,
        description="Engine noise",
        status=RepairRequestStatus.submitted,
    )
    db_session.add(repair_request)
    db_session.flush()

    work_order_driver = WorkOrder(
        id=uuid.uuid4(),
        vehicle_id=vehicle.id,
        technician_id=mechanic.id,
        repair_request_id=repair_request.id,
        description="Inspect engine",
        status=WorkOrderStatus.open,
        origin=WorkOrderOrigin.driver_request,
        created_at=datetime.now(timezone.utc),
    )
    work_order_manager = WorkOrder(
        id=uuid.uuid4(),
        vehicle_id=vehicle.id,
        technician_id=None,
        repair_request_id=None,
        description="Scheduled maintenance",
        status=WorkOrderStatus.in_progress,
        origin=WorkOrderOrigin.manual,
        created_at=datetime.now(timezone.utc),
    )
    db_session.add_all([work_order_driver, work_order_manager])
    db_session.commit()

    response_driver = client.get("/work-orders", headers=auth_headers(driver))
    assert response_driver.status_code == 200
    assert len(response_driver.json()) == 1

    response_mechanic = client.get("/work-orders", headers=auth_headers(mechanic))
    assert response_mechanic.status_code == 200
    assert len(response_mechanic.json()) == 1

    response_manager = client.get("/work-orders", headers=auth_headers(manager))
    assert response_manager.status_code == 200
    assert len(response_manager.json()) == 2


def test_planning_endpoint(client, db_session: Session, create_user, auth_headers) -> None:
    manager = create_user("planner@example.com", role=UserRole.manager)
    vehicle = _create_vehicle(db_session, "VIN321")

    work_order = WorkOrder(
        id=uuid.uuid4(),
        vehicle_id=vehicle.id,
        technician_id=None,
        repair_request_id=None,
        description="Check tires",
        status=WorkOrderStatus.open,
        origin=WorkOrderOrigin.manual,
        created_at=datetime.now(timezone.utc),
    )
    db_session.add(work_order)
    db_session.commit()

    response = client.get("/planning", headers=auth_headers(manager))
    assert response.status_code == 200
    payload = response.json()
    assert payload
    assert payload[0]["work_order_id"] == str(work_order.id)
