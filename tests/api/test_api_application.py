from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.api.api_application import create_app
from tests.fixtures.api_application_fixtures import mock_router, mock_settings


@patch("app.api.api_application.configure_middlewares")
@patch("app.api.api_application.add_error_handlers")
@patch("app.api.api_application.add_health_check_router")
def test_create_app_with_mocks(mock_health, mock_errors, mock_middlewares, mock_settings, mock_router):
    """Testa se a aplicação FastAPI é criada corretamente com os middlewares, rotas e handlers simulados."""
    app = create_app(mock_settings, mock_router)
    client = TestClient(app)

    # Verifica rota registrada
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}

    # Verifica chamada das funções mockadas
    mock_middlewares.assert_called_once_with(app, mock_settings)
    mock_errors.assert_called_once_with(app)
    mock_health.assert_called_once_with(app, prefix=mock_settings.health_check_base_path)

    # Verifica se a documentação está disponível
    response = client.get("/api/docs")
    assert response.status_code == 200
