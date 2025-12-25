from __future__ import annotations

from dataclasses import dataclass
from math import ceil
from typing import Generic, Sequence, TypeVar

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.core.constants import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

T = TypeVar("T")


@dataclass(frozen=True)
class Page(Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
    pages: int
    has_next: bool
    has_previous: bool


def _normalize_pagination(page: int, size: int) -> tuple[int, int]:
    page = max(page, 1)
    size = max(1, min(size, MAX_PAGE_SIZE))
    return page, size


def paginate_list(items: Sequence[T], page: int = 1, size: int = DEFAULT_PAGE_SIZE) -> Page[T]:
    page, size = _normalize_pagination(page, size)
    total = len(items)
    pages = max(ceil(total / size), 1)
    offset = (page - 1) * size
    return Page(
        items=list(items[offset : offset + size]),
        total=total,
        page=page,
        size=size,
        pages=pages,
        has_next=page < pages,
        has_previous=page > 1,
    )


def paginate_query(
    db: Session,
    stmt: Select,
    page: int = 1,
    size: int = DEFAULT_PAGE_SIZE,
) -> Page[T]:
    page, size = _normalize_pagination(page, size)
    total_stmt = select(func.count()).select_from(stmt.subquery())
    total = db.execute(total_stmt).scalar_one()
    offset = (page - 1) * size
    items = list(db.execute(stmt.limit(size).offset(offset)).scalars().all())
    pages = max(ceil(total / size), 1)
    return Page(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=pages,
        has_next=page < pages,
        has_previous=page > 1,
    )
