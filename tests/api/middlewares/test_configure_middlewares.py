# tests/test_configure_middlewares.py

import pytest
from unittest.mock import patch

from app.api.middlewares import configure_middlewares

#configure_middlewares
import pytest
from unittest.mock import MagicMock
from fastapi import FastAPI

@pytest.fixture
def mock_settings():
    """Retorna configurações mockadas com CORS liberado."""
    class Settings:
        cors_origins = ["*"]
    return Settings()

@pytest.fixture
def app():
    """Retorna uma instância mockada de FastAPI."""
    return MagicMock(spec=FastAPI)

def test_configure_middlewares_adds_middlewares(app, mock_settings):
    """
    Testa se a função configure_middlewares adiciona os middlewares esperados
    e se o CorrelationIdMiddleware usa corretamente o get_trace_id como generator.
    """
    with patch("app.api.middlewares.configure_middlewares.get_trace_id", return_value="traceid") as mock_trace_id:
        configure_middlewares.configure_middlewares(app, mock_settings)

        calls = [call[0][0] for call in app.add_middleware.call_args_list]

        assert any("CORSMiddleware" in str(c) for c in calls), "CORSMiddleware não adicionado"
        assert any("CorrelationIdMiddleware" in str(c) for c in calls), "CorrelationIdMiddleware não adicionado"
        assert any("GZipMiddleware" in str(c) for c in calls), "GZipMiddleware não adicionado"

        correlation_call = [
            call for call in app.add_middleware.call_args_list
            if "CorrelationIdMiddleware" in str(call[0][0])
        ][0]

        assert correlation_call[1]["generator"]() == "traceid"
        assert mock_trace_id.called, "get_trace_id não foi chamado"