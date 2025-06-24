# tests/test_router.py
import pytest
import importlib
from fastapi import APIRouter

@pytest.fixture
def mock_router_estoque_v2():
    """Fixture que cria um router fictício para mock."""
    router = APIRouter()

    @router.get("/fake")
    def fake_route():
        return {"msg": "ok"}

    return router


def test_router_include_router(monkeypatch, mock_router_estoque_v2):
    """
    Testa se o routes.include_router incluiu corretamente o router mockado.
    
    Usa monkeypatch para substituir o router original por um mock, recarrega o módulo
    para aplicar a substituição, e verifica se a rota fake está presente.
    """
    # Substitui o router_estoque_v2 pelo mock antes da importação
    monkeypatch.setattr("app.api.v2.router_estoque_v2", mock_router_estoque_v2)

    # Reimporta o módulo router para aplicar o patch
    import app.api.router
    importlib.reload(app.api.router)

    # Obtém o router do módulo já com o mock aplicado
    routes = app.api.router.routes

    # Lista as rotas adicionadas
    route_paths = [route.path for route in routes.routes]

    # Verifica se a rota fictícia foi adicionada
    assert "/fake" in route_paths