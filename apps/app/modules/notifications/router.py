from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.dependencies import get_current_user
from app.db.models.user import User
from app.modules.notifications.schemas import NotificationResponse
from app.modules.notifications.service import list_events_for_user, mark_event_read

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("", response_model=list[NotificationResponse])
def list_notifications(
    limit: int | None = Query(default=None, ge=1, le=100),
    current_user: User = Depends(get_current_user),
) -> list[NotificationResponse]:
    """Lister les notifications de l'utilisateur."""
    events = list_events_for_user(str(current_user.id), limit=limit)
    return [NotificationResponse.model_validate(event) for event in events]


@router.patch("/{event_id}/read", response_model=NotificationResponse)
def read_notification(
    event_id: str,
    current_user: User = Depends(get_current_user),
) -> NotificationResponse:
    """Marquer une notification comme lue."""
    event = mark_event_read(event_id)
    if event is None or str(event.user_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    return NotificationResponse.model_validate(event)
