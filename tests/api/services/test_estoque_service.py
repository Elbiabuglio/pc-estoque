from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.common.exceptions.estoque_exceptions import EstoqueBadRequestException
from app.models.estoque_model import Estoque
from app.services.estoque_service import EstoqueServices


@pytest.fixture
def mock_repository():
    return AsyncMock()

@pytest.fixture
def mock_redis():
    redis = AsyncMock()
    redis.get_json.return_value = None
    return redis

@pytest.fixture
def mock_historico_repository():
    return AsyncMock()

@pytest.fixture
def service(mock_repository, mock_redis, mock_historico_repository):
    return EstoqueServices(mock_repository, mock_redis, mock_historico_repository)

@pytest.fixture
def estoque_exemplo():
    return Estoque(id=1, seller_id="vendedor1", sku="sku1", quantidade=10)

class FakePaginator:
    def __init__(self, limit, offset):
        self.limit = limit
        self.offset = offset

@pytest.mark.asyncio
async def test_get_by_seller_id_and_sku_cache_hit(service, mock_repository, mock_redis, estoque_exemplo):
    mock_redis.get_json.return_value = estoque_exemplo.model_dump()
    result = await service.get_by_seller_id_and_sku("vendedor1", "sku1")
    assert result.seller_id == "vendedor1"
    assert result.sku == "sku1"
    mock_redis.get_json.assert_awaited_once()

@pytest.mark.asyncio
async def test_get_by_seller_id_and_sku_db_hit(service, mock_repository, mock_redis, estoque_exemplo):
    mock_redis.get_json.return_value = None
    mock_repository.find_by_seller_id_and_sku.return_value = estoque_exemplo.model_dump()
    result = await service.get_by_seller_id_and_sku("vendedor1", "sku1")
    assert result.seller_id == "vendedor1"
    assert result.sku == "sku1"
    mock_repository.find_by_seller_id_and_sku.assert_awaited_once_with("vendedor1", "sku1")
    mock_redis.set_json.assert_awaited_once()

@pytest.mark.asyncio
async def test_create_estoque_funciona(service, mock_repository, mock_historico_repository, estoque_exemplo):
    service._validate_non_existent_estoque = AsyncMock()
    service._validate_positive_estoque = MagicMock()
    mock_repository.create.return_value = estoque_exemplo

    result = await service.create(estoque_exemplo)

    service._validate_non_existent_estoque.assert_awaited_once_with("vendedor1", "sku1")
    service._validate_positive_estoque.assert_called_once_with(estoque_exemplo)
    mock_repository.create.assert_awaited_once()
    mock_historico_repository.create.assert_awaited_once()
    assert result.id == 1
    assert result.quantidade == 10

@pytest.mark.asyncio
async def test_update_estoque_funciona(service, mock_repository, mock_historico_repository, estoque_exemplo):
    mock_repository.find_by_seller_id_and_sku.return_value = estoque_exemplo.model_dump()
    mock_repository.update_by_seller_id_and_sku.return_value = estoque_exemplo
    service._validate_positive_estoque = MagicMock()

    with patch("app.services.estoque_service.utcnow", return_value="2024-01-01T00:00:00Z"):
        result = await service.update("vendedor1", "sku1", 20)

    mock_repository.find_by_seller_id_and_sku.assert_awaited_once_with("vendedor1", "sku1")
    mock_repository.update_by_seller_id_and_sku.assert_awaited_once()
    mock_historico_repository.create.assert_awaited_once()
    assert result.quantidade == 10  # pois mock_repository retorna estoque_exemplo

@pytest.mark.asyncio
async def test_delete_estoque_funciona(service, mock_repository, mock_historico_repository, estoque_exemplo):
    mock_repository.find_by_seller_id_and_sku.return_value = estoque_exemplo.model_dump()
    mock_repository.delete_by_seller_id_and_sku.return_value = True

    result = await service.delete("vendedor1", "sku1")

    mock_repository.find_by_seller_id_and_sku.assert_awaited_once_with("vendedor1", "sku1")
    mock_repository.delete_by_seller_id_and_sku.assert_awaited_once_with("vendedor1", "sku1")
    mock_historico_repository.create.assert_awaited_once()
    assert result is True

@pytest.mark.asyncio
async def test_list_estoques_funciona(service, mock_repository):
    paginator = FakePaginator(limit=10, offset=0)
    filters = {"seller_id": "vendedor1"}
    estoques_mock = [
        Estoque(id=1, seller_id="vendedor1", sku="sku1", quantidade=5),
        Estoque(id=2, seller_id="vendedor1", sku="sku2", quantidade=10)
    ]
    mock_repository.find.return_value = estoques_mock

    result = await service.list(paginator, filters)

    mock_repository.find.assert_awaited_once_with(filters, limit=10, offset=0)
    assert result == estoques_mock

def test_validate_positive_estoque_valido():
    service = EstoqueServices(None, None, None)
    estoque = Estoque(id=1, seller_id="vendedor1", sku="sku1", quantidade=5)
    service._validate_positive_estoque(estoque)

def test_validate_positive_estoque_invalido():
    service = EstoqueServices(None, None, None)
    estoque = Estoque(id=1, seller_id="vendedor1", sku="sku1", quantidade=0)
    with pytest.raises(EstoqueBadRequestException) as exc:
        service._validate_positive_estoque(estoque)
    detalhes = getattr(exc.value, "details", [])
    mensagem = str(detalhes[0].message) if detalhes else str(exc.value)
    assert "quantidade deve ser maior que zero." in mensagem

@pytest.mark.asyncio
async def test_validate_non_existent_estoque_existente(mock_repository):
    mock_repository.find_by_seller_id_and_sku.return_value = Estoque(
        id=1, seller_id="vendedor1", sku="sku1", quantidade=10
    )
    service = EstoqueServices(mock_repository, None, None)
    with pytest.raises(EstoqueBadRequestException) as exc:
        await service._validate_non_existent_estoque("vendedor1", "sku1")
    detalhes = getattr(exc.value, "details", [])
    mensagem = str(detalhes[0].message) if detalhes else str(exc.value)
    assert "Estoque para produto já cadastrado." in mensagem