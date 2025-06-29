#estoque_router
import pytest
from httpx import AsyncClient, ASGITransport
import pytest_asyncio
from dataclasses import dataclass
from app.api_main import app


# ----- Fixtures -----

@pytest_asyncio.fixture
async def async_client():
    """Cliente HTTP assíncrono para testes."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://localhost:8000/seller/v2") as client:
        yield client

@pytest_asyncio.fixture
async def mock_do_auth(monkeypatch):
    """Mock da autenticação."""
    async def fake_do_auth():
        return True

    monkeypatch.setattr("app.api.v2.routers.estoque_router.do_auth", fake_do_auth)

@pytest.fixture
def headers():
    """Cabeçalho padrão de seller."""
    return {"x-seller-id": "1"}

@dataclass
class Estoque:
    seller_id: str
    sku: str
    quantidade: int

@pytest.fixture
def test_estoques():
    """Lista de estoques mockados."""
    return [
        Estoque(seller_id="1", sku="ABC123", quantidade=10),
        Estoque(seller_id="2", sku="DEF456", quantidade=20),
        Estoque(seller_id="3", sku="GHI789", quantidade=30),
    ]


# ----- Testes -----

@pytest.mark.usefixtures("mock_do_auth", "async_client")
class TestEstoqueRouterV2:

    @pytest.mark.asyncio
    async def test_listar_estoques(self, async_client: AsyncClient, headers):
        """Deve retornar lista de estoques com status 200."""
        resposta = await async_client.get("/estoque", headers=headers)
        assert resposta.status_code == 200
        assert "results" in resposta.json()

    @pytest.mark.asyncio
    async def test_buscar_estoque_por_sku(self, async_client: AsyncClient, test_estoques):
        """Deve retornar estoque por SKU com status 200."""
        estoque = test_estoques[0]
        resposta = await async_client.get(
            f"/estoque/{estoque.sku}",
            headers={"x-seller-id": estoque.seller_id}
        )
        assert resposta.status_code == 200
        assert resposta.json()["seller_id"] == estoque.seller_id
        assert resposta.json()["sku"] == estoque.sku

    @pytest.mark.asyncio
    async def test_criar_estoque(self, async_client: AsyncClient):
        """Deve criar um novo estoque com status 201."""
        novo_estoque = {"seller_id": "3", "sku": "C", "quantidade": 100}
        resposta = await async_client.post(
            "/estoque",
            json=novo_estoque,
            headers={"x-seller-id": "3"}
        )
        assert resposta.status_code == 201
        assert resposta.json()["seller_id"] == "3"
        assert resposta.json()["sku"] == "C"

    @pytest.mark.asyncio
    async def test_atualizar_estoque(self, async_client: AsyncClient, test_estoques):
        """Deve atualizar estoque com PUT e retornar status 200."""
        estoque = test_estoques[0]
        update = {"quantidade": 50}
        resposta = await async_client.put(
            f"/estoque/{estoque.sku}",
            json=update,
            headers={"x-seller-id": estoque.seller_id}
        )
        assert resposta.status_code == 200
        assert resposta.json()["quantidade"] == 50

    @pytest.mark.asyncio
    async def test_patch_estoque(self, async_client: AsyncClient, test_estoques):
        """Deve atualizar parcialmente o estoque com PATCH."""
        estoque = test_estoques[0]
        patch = {"quantidade": 75}
        resposta = await async_client.patch(
            f"/estoque/{estoque.sku}",
            json=patch,
            headers={"x-seller-id": estoque.seller_id}
        )
        assert resposta.status_code == 200
        assert resposta.json()["quantidade"] == 75

    @pytest.mark.asyncio
    async def test_deletar_estoque(self, async_client: AsyncClient, test_estoques):
        """Deve deletar o estoque e confirmar exclusão."""
        estoque = test_estoques[0]
        resposta = await async_client.delete(
            f"/estoque/{estoque.sku}",
            headers={"x-seller-id": estoque.seller_id}
        )
        assert resposta.status_code == 204

        # Verificar se o recurso foi realmente excluído
        resposta_get = await async_client.get(
            f"/estoque/{estoque.sku}",
            headers={"x-seller-id": estoque.seller_id}
        )
        assert resposta_get.status_code == 404