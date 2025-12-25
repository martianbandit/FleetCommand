from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.db.models.user import User
from app.modules.auth.schemas import LoginRequest, RegisterRequest


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.execute(select(User).where(User.email == email)).scalars().first()


def register_user(db: Session, payload: RegisterRequest) -> User:
    existing = get_user_by_email(db, payload.email)
    if existing:
        raise ValueError("Email already registered")
    user = User(
        email=payload.email,
        full_name=payload.full_name,
        password_hash=hash_password(payload.password),
        role=payload.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, payload: LoginRequest) -> str:
    user = get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.password_hash):
        raise ValueError("Invalid credentials")
    return create_access_token(str(user.id))
