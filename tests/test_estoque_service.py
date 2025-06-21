import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.estoque_service import EstoqueServices
from app.models.estoque_model import Estoque
from app.common.exceptions.estoque_exceptions import EstoqueBadRequestException

from tests.fixtures.estoque_service_fixtures import (
    mock_repository, service, estoque_exemplo, FakePaginator
)


@pytest.mark.asyncio
async def test_get_by_seller_id_and_sku_retorna_estoque(service, mock_repository):
    """Deve retornar um estoque quando encontrado pelo seller_id e sku."""
    mock_repository.find_by_seller_id_and_sku.return_value = {
        "id": "1", "seller_id": "vendedor1", "sku": "sku123", "quantidade": 5
    }

    resultado = await service.get_by_seller_id_and_sku("vendedor1", "sku123")

    mock_repository.find_by_seller_id_and_sku.assert_awaited_once_with("vendedor1", "sku123")
    assert resultado.seller_id == "vendedor1"
    assert resultado.sku == "sku123"
    assert resultado.quantidade == 5


@pytest.mark.asyncio
async def test_create_estoque_funciona(service, mock_repository, estoque_exemplo):
    """Deve criar um estoque novo após validar inexistência e quantidade positiva."""
    service._validate_non_existent_estoque = AsyncMock()
    service._validate_positive_estoque = MagicMock()

    mock_repository.create.return_value = estoque_exemplo

    resultado = await service.create(estoque_exemplo)

    service._validate_non_existent_estoque.assert_awaited_once_with("vendedor1", "sku1")
    service._validate_positive_estoque.assert_called_once_with(estoque_exemplo)
    mock_repository.create.assert_awaited_once()

    assert resultado.id == 1
    assert resultado.quantidade == 10


@pytest.mark.asyncio
async def test_update_estoque_funciona(service, mock_repository, estoque_exemplo):
    """Deve atualizar a quantidade de um estoque existente."""
    mock_repository.find_by_seller_id_and_sku.return_value = estoque_exemplo

    estoque_atualizado = Estoque(
        id=1, seller_id="vendedor1", sku="sku1", quantidade=20
    )
    mock_repository.update_by_seller_id_and_sku.return_value = estoque_atualizado

    with patch("app.services.estoque_service.utcnow", return_value="2024-01-01T00:00:00Z"):
        resultado = await service.update("vendedor1", "sku1", 20)

    mock_repository.find_by_seller_id_and_sku.assert_awaited_once_with("vendedor1", "sku1")
    mock_repository.update_by_seller_id_and_sku.assert_awaited_once()
    assert resultado.quantidade == 20


@pytest.mark.asyncio
async def test_delete_estoque_funciona(service, mock_repository):
    """Deve excluir um estoque encontrado pelo seller_id e sku."""
    mock_repository.find_by_seller_id_and_sku.return_value = {"id": 1, "seller_id": "vendedor1", "sku": "sku1"}
    mock_repository.delete_by_seller_id_and_sku.return_value = True

    await service.delete("vendedor1", "sku1")

    mock_repository.find_by_seller_id_and_sku.assert_awaited_once_with("vendedor1", "sku1")
    mock_repository.delete_by_seller_id_and_sku.assert_awaited_once_with("vendedor1", "sku1")


@pytest.mark.asyncio
async def test_list_estoques_funciona(service, mock_repository):
    """Deve retornar uma lista de estoques com paginação e filtros."""
    paginator = FakePaginator(limit=10, offset=0)
    filters = {"seller_id": "vendedor1"}
    estoques_mock = [
        Estoque(id=1, seller_id="vendedor1", sku="sku1", quantidade=5),
        Estoque(id=2, seller_id="vendedor1", sku="sku2", quantidade=10)
    ]

    mock_repository.find.return_value = estoques_mock

    resultado = await service.list(paginator, filters)

    mock_repository.find.assert_awaited_once_with(filters, limit=10, offset=0)
    assert resultado == estoques_mock


def test_validate_positive_estoque_valido():
    """Deve validar quando a quantidade for maior que zero, sem exceção."""
    service = EstoqueServices(None)
    estoque = Estoque(id=1, seller_id="vendedor1", sku="sku1", quantidade=5)
    service._validate_positive_estoque(estoque)


def test_validate_positive_estoque_invalido():
    """Deve lançar exceção quando a quantidade for zero ou negativa."""
    service = EstoqueServices(None)
    estoque = Estoque(id=1, seller_id="vendedor1", sku="sku1", quantidade=0)

    with pytest.raises(EstoqueBadRequestException) as exc:
        service._validate_positive_estoque(estoque)

    detalhes = getattr(exc.value, "details", [])
    mensagem = str(detalhes[0].message) if detalhes else str(exc.value)
    assert "quantidade deve ser maior que zero." in mensagem


@pytest.mark.asyncio
async def test_validate_non_existent_estoque_existente(mock_repository):
    """Deve lançar exceção se já existir estoque para seller_id e sku."""
    mock_repository.find_by_seller_id_and_sku.return_value = Estoque(
        id=1, seller_id="vendedor1", sku="sku1", quantidade=10
    )

    service = EstoqueServices(mock_repository)

    with pytest.raises(EstoqueBadRequestException) as exc:
        await service._validate_non_existent_estoque("vendedor1", "sku1")

    detalhes = getattr(exc.value, "details", [])
    mensagem = str(detalhes[0].message) if detalhes else str(exc.value)
    assert "Estoque para produto já cadastrado." in mensagem