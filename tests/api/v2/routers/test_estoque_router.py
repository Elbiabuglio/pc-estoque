#estoque_router
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from app.api.v2.routers import estoque_router
from app.container import Container

@pytest.fixture
def mock_estoque_service():
    """
    Fixture que retorna um AsyncMock para o serviço de estoque.
    """
    return AsyncMock()

@pytest.fixture
def app(mock_estoque_service):
    """
    Fixture que cria uma instância FastAPI com o container configurado e o router de estoque incluído.
    """
    container = Container()
    container.estoque_service.override(mock_estoque_service)

    app = FastAPI()
    app.container = container
    app.include_router(estoque_router.router)

    container.wire(modules=[estoque_router])

    return app

@pytest.fixture
def client(app):
    """
    Fixture que cria um TestClient para realizar requisições HTTP à aplicação FastAPI.
    """
    return TestClient(app)

def test_get_estoque(client, mock_estoque_service):
    """
    Testa a rota GET /estoque para listar itens em estoque filtrados pelo seller_id.
    """
    mock_estoque_service.list.return_value = [
        {"sku": "ABC123", "quantidade": 5}
    ]

    headers = {"x-seller-id": "12345"}
    response = client.get("/estoque", headers=headers)

    assert response.status_code == 200
    json_data = response.json()

    assert "results" in json_data
    assert isinstance(json_data["results"], list)

    result_item = json_data["results"][0]
    assert result_item["sku"] == "ABC123"
    assert result_item["quantidade"] == 5

    mock_estoque_service.list.assert_awaited_once()

    called_args = mock_estoque_service.list.call_args.kwargs
    assert called_args["filters"]["seller_id"] == "12345"

def test_get_estoque_by_sku(client, mock_estoque_service):
    """
    Testa a rota GET /estoque/{sku} para buscar um item específico pelo SKU e seller_id.
    """
    mock_estoque_service.get_by_seller_id_and_sku.return_value = {
        "sku": "ABC123",
        "quantidade": 5
    }

    headers = {"x-seller-id": "12345"}
    response = client.get("/estoque/ABC123", headers=headers)

    assert response.status_code == 200
    json_data = response.json()

    assert json_data["sku"] == "ABC123"
    assert json_data["quantidade"] == 5

    mock_estoque_service.get_by_seller_id_and_sku.assert_awaited_once_with("12345", "ABC123")

def test_create_estoque(client, mock_estoque_service):
    """
    Testa a rota POST /estoque para criar um novo item de estoque com dados enviados.
    """
    mock_estoque_service.create.return_value = {
        "sku": "ABC123",
        "quantidade": 10
    }

    headers = {"x-seller-id": "12345"}
    payload = {
        "sku": "ABC123",
        "quantidade": 10
    }

    response = client.post("/estoque", json=payload, headers=headers)

    assert response.status_code == 201
    json_data = response.json()

    assert json_data["sku"] == "ABC123"
    assert json_data["quantidade"] == 10

    called_args = mock_estoque_service.create.call_args.args[0]
    # Verifica se o argumento é um objeto com atributos ou um dict
    if hasattr(called_args, "sku"):
        assert called_args.sku == "ABC123"
        assert called_args.quantidade == 10
        assert getattr(called_args, "seller_id", None) == "12345"
    else:
        assert called_args["sku"] == "ABC123"
        assert called_args["quantidade"] == 10
        assert called_args["seller_id"] == "12345"

def test_update_estoque_by_sku(client, mock_estoque_service):
    """
    Testa a rota PATCH /estoque/{sku} para atualizar a quantidade de um item específico.
    """
    mock_estoque_service.update.return_value = {
        "sku": "ABC123",
        "quantidade": 20
    }

    headers = {"x-seller-id": "12345"}
    payload = {
        "quantidade": 20
    }

    response = client.patch("/estoque/ABC123", json=payload, headers=headers)

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["sku"] == "ABC123"
    assert json_data["quantidade"] == 20

    mock_estoque_service.update.assert_awaited_once_with("12345", "ABC123", 20)

def test_delete_estoque_by_sku(client, mock_estoque_service):
    """
    Testa a rota DELETE /estoque/{sku} para remover um item específico do estoque.
    """
    mock_estoque_service.delete.return_value = None  # DELETE normalmente não retorna conteúdo

    headers = {"x-seller-id": "12345"}

    response = client.delete("/estoque/ABC123", headers=headers)

    assert response.status_code == 204
    mock_estoque_service.delete.assert_awaited_once_with("12345", "ABC123")