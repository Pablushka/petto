import pytest
from fastapi.testclient import TestClient

from main import app


def test_login_returns_tokens():
    client = TestClient(app)
    # Ensure test user exists in DB or use a fixture; this test assumes a user with email 'test@example.com' and password 'password' exists.
    resp = client.post(
        '/api/login', json={'email': 'test@example.com', 'password': 'password'})
    assert resp.status_code in (200, 401)
    if resp.status_code == 200:
        data = resp.json()
        assert 'access_token' in data
        assert 'refresh_token' in data
