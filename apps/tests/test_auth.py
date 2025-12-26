from sqlalchemy.orm import Session

from app.modules.auth.service import authenticate_user, register_user
from app.modules.auth.schemas import LoginRequest, RegisterRequest
from app.db.models.user import UserRole


def test_register_user_hashes_password(db_session: Session) -> None:
    payload = RegisterRequest(
        email="unit@example.com",
        full_name="Unit Tester",
        password="supersecret",
        role=UserRole.manager,
    )
    user = register_user(db_session, payload)

    assert user.email == payload.email
    assert user.hashed_password != payload.password


def test_authenticate_user_rejects_invalid_password(db_session: Session) -> None:
    payload = RegisterRequest(
        email="login@example.com",
        full_name="Login Tester",
        password="validpassword",
        role=UserRole.driver,
    )
    register_user(db_session, payload)

    invalid_login = LoginRequest(email=payload.email, password="wrongpassword")
    try:
        authenticate_user(db_session, invalid_login)
    except ValueError as exc:
        assert "Invalid credentials" in str(exc)
    else:
        raise AssertionError("Expected invalid credentials error")


def test_register_and_login_flow(client) -> None:
    register_payload = {
        "email": "api@example.com",
        "full_name": "API User",
        "password": "strongpassword",
        "role": "manager",
    }
    response = client.post("/auth/register", json=register_payload)
    assert response.status_code == 201

    token_response = client.post(
        "/auth/token", json={"email": register_payload["email"], "password": register_payload["password"]}
    )
    assert token_response.status_code == 200
    assert token_response.json()["access_token"]
