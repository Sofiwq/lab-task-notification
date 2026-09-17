from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_task():
    r = client.post("/api/tasks", json={"title": "Test", "description": "desc"})
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == "Test"
    assert data["status"] == "new"
    assert "id" in data and "created_at" in data