from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.user import User, UserRole


def get_user(db: Session, user_id: str) -> User | None:
    return db.get(User, user_id)


def get_user_by_email(db: Session, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    return db.execute(stmt).scalars().first()


def list_users(db: Session, role: UserRole | None = None) -> list[User]:
    stmt = select(User)
    if role is not None:
        stmt = stmt.where(User.role == role)
    return list(db.execute(stmt).scalars().all())
