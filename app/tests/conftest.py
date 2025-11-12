import pytest
from fastapi.testclient import TestClient

# Импортируем наше FastAPI приложение
from main import app

@pytest.fixture(scope="module")
def client():
    """
    Фикстура для создания тестового клиента FastAPI.
    """
    with TestClient(app) as test_client:
        yield test_client