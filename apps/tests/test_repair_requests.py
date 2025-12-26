import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.models.repair_request import RepairRequest, RepairRequestStatus
from app.db.models.user import UserRole
from app.db.models.vehicle import Vehicle


def _create_vehicle(db_session: Session, vin: str, license_plate: str) -> Vehicle:
    vehicle = Vehicle(
        id=uuid.uuid4(),
        vin=vin,
        license_plate=license_plate,
        make="Renault",
        model="Kangoo",
        year=2022,
        status="active",
        created_at=datetime.now(timezone.utc),
    )
    db_session.add(vehicle)
    db_session.commit()
    db_session.refresh(vehicle)
    return vehicle


def test_list_repair_requests_filters_for_driver(client, db_session: Session, create_user, auth_headers) -> None:
    driver = create_user("driver@example.com", role=UserRole.driver)
    manager = create_user("manager@example.com", role=UserRole.manager)

    vehicle = _create_vehicle(db_session, "VIN123", "ABC-123")
    request = RepairRequest(
        id=uuid.uuid4(),
        vehicle_id=vehicle.id,
        driver_id=driver.id,
        description="Brake issue",
        status=RepairRequestStatus.submitted,
    )
    db_session.add(request)
    db_session.commit()

    response_driver = client.get("/repair-requests", headers=auth_headers(driver))
    assert response_driver.status_code == 200
    assert len(response_driver.json()) == 1

    response_manager = client.get("/repair-requests", headers=auth_headers(manager))
    assert response_manager.status_code == 200
    assert len(response_manager.json()) == 1
