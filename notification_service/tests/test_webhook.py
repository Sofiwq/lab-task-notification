from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_task_created_webhook_success():
    payload = {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "title": "Купить молоко",
        "description": "Не забыть 2.5%",
        "status": "new",
        "created_at": "2026-09-17T09:50:00Z",
    }
    response = client.post("/api/webhooks/task_created", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "received"
    assert body["task_id"] == payload["id"]


def test_task_created_webhook_invalid_payload():
    response = client.post(
        "/api/webhooks/task_created",
        json={"title": "Без id"},
    )
    assert response.status_code == 422


def test_task_created_webhook_invalid_status():
    payload = {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "title": "Купить молоко",
        "description": "",
        "status": "unknown_status",
        "created_at": "2026-09-17T09:50:00Z",
    }
    response = client.post("/api/webhooks/task_created", json=payload)
    assert response.status_code == 422