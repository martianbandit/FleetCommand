import unittest

from app.core.security import create_access_token, decode_access_token, hash_password, verify_password


class TestAuthSecurity(unittest.TestCase):
    def test_hash_password_roundtrip(self) -> None:
        password = "fleet-command-password"
        password_hash = hash_password(password)

        self.assertNotEqual(password, password_hash)
        self.assertTrue(verify_password(password, password_hash))
        self.assertFalse(verify_password("wrong-password", password_hash))

    def test_access_token_roundtrip(self) -> None:
        token = create_access_token("user-123")
        payload = decode_access_token(token)

        self.assertEqual(payload["sub"], "user-123")
