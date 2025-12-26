from datetime import datetime, timezone

from app.db.models.user import UserRole
from app.modules.notifications.events import NotificationEvent
from app.modules.notifications.service import publish_event


def test_notifications_flow(client, create_user, auth_headers) -> None:
    user = create_user("notify@example.com", role=UserRole.manager)
    event = NotificationEvent(
        id="evt-1",
        user_id=str(user.id),
        title="Test",
        message="Hello",
        created_at=datetime.now(timezone.utc),
        payload={"foo": "bar"},
        read_at=None,
    )
    publish_event(event)

    response = client.get("/notifications", headers=auth_headers(user))
    assert response.status_code == 200
    payload = response.json()
    assert payload
    assert payload[0]["id"] == event.id

    read_response = client.patch(f"/notifications/{event.id}/read", headers=auth_headers(user))
    assert read_response.status_code == 200
    assert read_response.json()["read_at"] is not None
