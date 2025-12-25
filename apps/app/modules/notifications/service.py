from __future__ import annotations

import threading
from datetime import datetime, timezone

from app.modules.notifications.events import NotificationEvent


_STORAGE_LOCK = threading.Lock()
_EVENTS: dict[str, NotificationEvent] = {}


def publish_event(event: NotificationEvent) -> None:
    with _STORAGE_LOCK:
        _EVENTS[event.id] = event


def publish_events(events: list[NotificationEvent]) -> None:
    with _STORAGE_LOCK:
        for event in events:
            _EVENTS[event.id] = event


def list_events_for_user(user_id: str, limit: int | None = None) -> list[NotificationEvent]:
    with _STORAGE_LOCK:
        events = [event for event in _EVENTS.values() if event.user_id == user_id]
    events.sort(key=lambda item: item.created_at, reverse=True)
    if limit is not None:
        return events[:limit]
    return events


def mark_event_read(event_id: str) -> NotificationEvent | None:
    with _STORAGE_LOCK:
        event = _EVENTS.get(event_id)
        if event is None:
            return None
        updated = NotificationEvent(
            id=event.id,
            user_id=event.user_id,
            title=event.title,
            message=event.message,
            created_at=event.created_at,
            payload=event.payload,
            read_at=datetime.now(timezone.utc),
        )
        _EVENTS[event_id] = updated
    return updated
