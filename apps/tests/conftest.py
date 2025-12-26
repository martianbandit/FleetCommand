import os
import uuid
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")

from app.core.dependencies import get_db  # noqa: E402
from app.core.security import create_access_token, hash_password  # noqa: E402
from app.db.base import Base  # noqa: E402
from app.db.models.user import User, UserRole  # noqa: E402
from app.main import create_app  # noqa: E402


@pytest.fixture(scope="session")
def engine() -> Generator:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture()
def db_session(engine) -> Generator[Session, None, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection, expire_on_commit=False)()
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture()
def client(db_session: Session) -> TestClient:
    app = create_app()

    def _get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = _get_db
    return TestClient(app)


@pytest.fixture()
def create_user(db_session: Session):
    def _create_user(
        email: str,
        full_name: str = "Test User",
        role: UserRole = UserRole.manager,
        password: str = "password123",
    ) -> User:
        user = User(
            id=uuid.uuid4(),
            email=email,
            full_name=full_name,
            hashed_password=hash_password(password),
            role=role,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

    return _create_user


@pytest.fixture()
def auth_headers():
    def _auth_headers(user: User) -> dict[str, str]:
        token = create_access_token(str(user.id))
        return {"Authorization": f"Bearer {token}"}

    return _auth_headers
