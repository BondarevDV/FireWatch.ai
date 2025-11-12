from fastapi.testclient import TestClient

def test_health_check(client: TestClient):
    """
    Тест для эндпоинта /api/v1/health.
    """
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "version": "v1"
    }