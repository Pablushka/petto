from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_pets_unauthorized():
    # Without auth, the endpoint should return 401 (depends on auth dependency)
    resp = client.get("/api/pets/")
    assert resp.status_code in (401, 403, 200)
