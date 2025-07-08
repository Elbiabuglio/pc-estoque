import pytest
from fastapi import APIRouter
from httpx import AsyncClient

from app.api.api_application import create_app
from app.settings import ApiSettings


@pytest.fixture
def mock_settings():
    """Fixture que retorna uma configuração simulada para a aplicação FastAPI."""
    return ApiSettings(
        app_name="Teste API",
        openapi_path="/openapi.json",
        version="1.0.0",
        health_check_base_path="/health"
    )


@pytest.fixture
def mock_router():
    """Fixture que retorna um roteador FastAPI vazio com rota /ping para inclusão na aplicação."""
    router = APIRouter()

    @router.get("/ping")
    async def ping():
        return {"message": "pong"}

    return router


@pytest.fixture
def app(mock_settings, mock_router):
    """Fixture que cria e retorna a instância FastAPI usando as configurações e rotas simuladas."""
    return create_app(mock_settings, mock_router)


@pytest.fixture
async def async_client(app):
    """Fixture que retorna um cliente HTTP assíncrono para realizar requisições na aplicação FastAPI."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client