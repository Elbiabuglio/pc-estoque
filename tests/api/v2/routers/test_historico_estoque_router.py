from unittest import mock
import pytest
from httpx import ASGITransport, AsyncClient
from fastapi import status

from app.api.common.auth_handler import do_auth
from app.api_main import app
from app.container import Container


@pytest.fixture
def mock_estoque_service():
    """Fixture para mockar o serviço de estoque."""
    yield mock
    Container.estoque_service.reset_override()

@pytest.fixture
def app_fixture():
    """Fixture que retorna a instância da aplicação FastAPI."""
    return app

@pytest.fixture
def mock_do_auth(app_fixture):
    """Fixture para desativar a autenticação durante os testes."""
    app_fixture.dependency_overrides[do_auth] = lambda: None
    yield
    app_fixture.dependency_overrides.pop(do_auth, None)

@pytest.fixture
async def async_client(app_fixture):
    """Fixture para criar um cliente HTTP assíncrono para os testes."""
    transport = ASGITransport(app=app_fixture)
    async with AsyncClient(transport=transport, base_url="http://localhost:8000/seller/v2") as client:
        yield client

@pytest.fixture
def auth_headers():
    """Fixture que retorna os headers necessários para as requisições."""
    return {"x-seller-id": "seller1", "Authorization": "Bearer fake-token"}


@pytest.mark.asyncio
async def test_list_historico_estoque_semana_v2_200(async_client, mock_do_auth, monkeypatch, auth_headers):
    """Testa o status 200 OK para o relatório semanal."""
    async def fake_get_relatorio_semanal(self, seller_id):
        return [{"seller_id": seller_id, "sku": "sku1", "quantidade_anterior": 1, "quantidade_nova": 2, "tipo_movimentacao": "CRIACAO", "movimentado_em": "2024-07-08T00:00:00"}]
    monkeypatch.setattr("app.services.historico_estoque_service.HistoricoEstoqueService.get_relatorio_semanal", fake_get_relatorio_semanal)
    
    response = await async_client.get("/historico_estoque/semana", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2

@pytest.mark.asyncio
async def test_list_historico_estoque_semana_v2_404(async_client, mock_do_auth, monkeypatch, auth_headers):
    """Testa o status 404 Not Found para o relatório semanal."""
    async def fake_get_relatorio_semanal(self, seller_id):
        return []
    monkeypatch.setattr("app.services.historico_estoque_service.HistoricoEstoqueService.get_relatorio_semanal", fake_get_relatorio_semanal)
    
    response = await async_client.get("/historico_estoque/semana", headers=auth_headers)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_list_historico_estoque_dia_v2_200(async_client, mock_do_auth, monkeypatch, auth_headers):
    """Testa o status 200 OK para o relatório diário."""
    async def fake_get_relatorio_diario(self, seller_id):
        return [{"seller_id": seller_id, "sku": "sku1", "quantidade_anterior": 1, "quantidade_nova": 2, "tipo_movimentacao": "CRIACAO", "movimentado_em": "2024-07-08T00:00:00"}]
    monkeypatch.setattr("app.services.historico_estoque_service.HistoricoEstoqueService.get_relatorio_diario", fake_get_relatorio_diario)
    
    response = await async_client.get("/historico_estoque/dia", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2

@pytest.mark.asyncio
async def test_list_historico_estoque_dia_v2_404(async_client, mock_do_auth, monkeypatch, auth_headers):
    """Testa o status 404 Not Found para o relatório diário."""
    async def fake_get_relatorio_diario(self, seller_id):
        return []
    monkeypatch.setattr("app.services.historico_estoque_service.HistoricoEstoqueService.get_relatorio_diario", fake_get_relatorio_diario)
    
    response = await async_client.get("/historico_estoque/dia", headers=auth_headers)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND