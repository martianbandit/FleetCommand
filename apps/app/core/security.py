import base64
import hashlib
import hmac
import json
import os
from datetime import datetime, timedelta, timezone
from typing import Any

from app.core.config import settings


def _base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


def _base64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120_000)
    return f"pbkdf2_sha256${_base64url_encode(salt)}${_base64url_encode(digest)}"


def verify_password(password: str, password_hash: str) -> bool:
    try:
        algorithm, salt_b64, digest_b64 = password_hash.split("$", 2)
    except ValueError:
        return False
    if algorithm != "pbkdf2_sha256":
        return False
    salt = _base64url_decode(salt_b64)
    expected = _base64url_decode(digest_b64)
    candidate = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120_000)
    return hmac.compare_digest(expected, candidate)


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(hours=6)
    expiry = datetime.now(timezone.utc) + expires_delta
    payload = {"sub": subject, "exp": int(expiry.timestamp())}
    payload_bytes = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    payload_b64 = _base64url_encode(payload_bytes)
    signature = hmac.new(settings.JWT_SECRET.encode("utf-8"), payload_b64.encode("utf-8"), hashlib.sha256).digest()
    signature_b64 = _base64url_encode(signature)
    return f"{payload_b64}.{signature_b64}"


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        payload_b64, signature_b64 = token.split(".")
    except ValueError as exc:
        raise ValueError("Invalid token format") from exc
    expected_signature = hmac.new(
        settings.JWT_SECRET.encode("utf-8"), payload_b64.encode("utf-8"), hashlib.sha256
    ).digest()
    if not hmac.compare_digest(_base64url_encode(expected_signature), signature_b64):
        raise ValueError("Invalid token signature")
    payload = json.loads(_base64url_decode(payload_b64))
    if int(payload.get("exp", 0)) < int(datetime.now(timezone.utc).timestamp()):
        raise ValueError("Token expired")
    return payload
