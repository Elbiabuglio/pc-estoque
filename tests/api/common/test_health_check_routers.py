# tests/test_health_check_routers.py

from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI

from app.api.common.routers import health_check_routers


@pytest.fixture
def mock_settings():
    """
    Mock para simular AppSettings ou configurações injetadas.
    """
    return MagicMock()

@pytest.fixture
def app_with_health_check(mock_settings):
    """
    Instancia o FastAPI e registra o health check router.
    """
    app = FastAPI()
    # Futuro: app.dependency_overrides[get_settings] = lambda: mock_settings
    health_check_routers.add_health_check_router(app)
    return app

@pytest.fixture
def client(app_with_health_check):
    """
    Cria um TestClient para realizar requisições HTTP ao app.
    """
    from fastapi.testclient import TestClient
    return TestClient(app_with_health_check)


def test_health_check_ping_get(client):
    """GET /api/ping deve retornar 204 e corpo vazio."""
    response = client.get("/api/ping")
    assert response.status_code == 204
    assert response.content == b""


def test_health_check_ping_head(client):
    """HEAD /api/ping deve retornar 204 e corpo vazio."""
    response = client.head("/api/ping")
    assert response.status_code == 204
    assert response.content == b""  # HEAD normalmente não retorna body


def test_health_check_ping_post_not_allowed(client):
    """POST /api/ping deve retornar 405 Method Not Allowed."""
    response = client.post("/api/ping")
    assert response.status_code == 405


def test_health_check_ping_response_headers(client):
    """Verifica se resposta 204 está coerente mesmo sem Content-Length."""
    response = client.get("/api/ping")
    assert response.status_code == 204
    assert response.content == b""
    # Header opcional para 204, apenas valida se existir
    if "Content-Length" in response.headers:
        assert response.headers["Content-Length"] == "0"


def test_nonexistent_route(client):
    """Requisição para rota inexistente deve retornar 404."""
    response = client.get("/api/rota-inexistente")
    assert response.status_code == 404


@pytest.mark.parametrize("method", ["get", "head"])
def test_ping_valid_methods_parametrized(client, method):
    """Valida múltiplos métodos permitidos usando parametrização."""
    response = getattr(client, method)("/api/ping")
    assert response.status_code == 204


def test_health_check_router_registration(app_with_health_check):
    """Garante que o /api/ping foi registrado na aplicação."""
    paths = [route.path for route in app_with_health_check.router.routes]
    assert "/api/ping" in paths
    

