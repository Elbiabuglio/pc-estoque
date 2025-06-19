# tests/services/test_estoque_service.py

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.estoque_service import EstoqueServices
from app.models.estoque_model import Estoque
from app.common.exceptions.estoque_exceptions import EstoqueBadRequestException


# ---------------- Fixtures reutilizáveis ---------------- #

@pytest.fixture
def mock_repository():
    """Fixture que retorna um repositório mockado para uso nos testes."""
    return AsyncMock()


@pytest.fixture
def service(mock_repository):
    """Fixture que instancia o serviço de EstoqueServices com o repositório mockado."""
    return EstoqueServices(mock_repository)


@pytest.fixture
def estoque_exemplo():
    """Fixture que fornece um exemplo de objeto Estoque para uso nos testes."""
    return Estoque(id=1, seller_id="vendedor1", sku="sku1", quantidade=10)


# ---------------- Testes de get_by_seller_id_and_sku ---------------- #

@pytest.mark.asyncio
async def test_get_by_seller_id_and_sku_retorna_estoque(service, mock_repository):
    """
    Testa se a função get_by_seller_id_and_sku retorna corretamente um estoque existente.

    Cenário:
    - Dado um seller_id e sku válidos
    - Quando a função for chamada
    - Então deve retornar um estoque com os atributos correspondentes
    """
    mock_repository.find_by_seller_id_and_sku.return_value = {
        "id": "1", "seller_id": "vendedor1", "sku": "sku123", "quantidade": 5
    }

    resultado = await service.get_by_seller_id_and_sku("vendedor1", "sku123")

    mock_repository.find_by_seller_id_and_sku.assert_awaited_once_with("vendedor1", "sku123")
    assert resultado.seller_id == "vendedor1"
    assert resultado.sku == "sku123"
    assert resultado.quantidade == 5


# ---------------- Testes de create ---------------- #

@pytest.mark.asyncio
async def test_create_estoque_funciona(service, mock_repository, estoque_exemplo):
    """
    Testa a criação de um novo estoque.

    Cenário:
    - Dado um estoque válido
    - Quando a função create for chamada
    - Então deve validar se o estoque não existe e se a quantidade é positiva,
      criando o registro e retornando o estoque criado
    """
    service._validate_non_existent_estoque = AsyncMock()
    service._validate_positive_estoque = MagicMock()

    mock_repository.create.return_value = estoque_exemplo

    resultado = await service.create(estoque_exemplo)

    service._validate_non_existent_estoque.assert_awaited_once_with("vendedor1", "sku1")
    service._validate_positive_estoque.assert_called_once_with(estoque_exemplo)
    mock_repository.create.assert_awaited_once()

    assert resultado.id == 1
    assert resultado.quantidade == 10


# ---------------- Testes de update ---------------- #

@pytest.mark.asyncio
async def test_update_estoque_funciona(service, mock_repository, estoque_exemplo):
    """
    Testa a atualização de um estoque existente.

    Cenário:
    - Dado um seller_id e sku existentes
    - Quando a função update for chamada com uma nova quantidade
    - Então deve atualizar o estoque e retornar o novo valor
    """
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


# ---------------- Testes de delete ---------------- #

@pytest.mark.asyncio
async def test_delete_estoque_funciona(service, mock_repository):
    """
    Testa a exclusão de um estoque existente.

    Cenário:
    - Dado um estoque encontrado pelo seller_id e sku
    - Quando a função delete for chamada
    - Então deve excluir o registro e confirmar a execução
    """
    mock_repository.find_by_seller_id_and_sku.return_value = {"id": 1, "seller_id": "vendedor1", "sku": "sku1"}
    mock_repository.delete_by_seller_id_and_sku.return_value = True

    await service.delete("vendedor1", "sku1")

    mock_repository.find_by_seller_id_and_sku.assert_awaited_once_with("vendedor1", "sku1")
    mock_repository.delete_by_seller_id_and_sku.assert_awaited_once_with("vendedor1", "sku1")


# ---------------- Testes de list ---------------- #

class FakePaginator:
    def __init__(self, limit, offset):
        self.limit = limit
        self.offset = offset


@pytest.mark.asyncio
async def test_list_estoques_funciona(service, mock_repository):
    """
    Testa a listagem de estoques com paginação e filtros.

    Cenário:
    - Dado um filtro por seller_id e uma paginação configurada
    - Quando a função list for chamada
    - Então deve retornar a lista de estoques correspondente
    """
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


# ---------------- Testes de validação de quantidade ---------------- #

def test_validate_positive_estoque_valido():
    """
    Testa a validação de quantidade positiva.

    Cenário:
    - Dado um estoque com quantidade maior que zero
    - Quando a validação for executada
    - Então não deve lançar exceção
    """
    service = EstoqueServices(None)
    estoque = Estoque(id=1, seller_id="vendedor1", sku="sku1", quantidade=5)
    service._validate_positive_estoque(estoque)


def test_validate_positive_estoque_invalido():
    """
    Testa a validação de quantidade inválida (zero ou negativa).

    Cenário:
    - Dado um estoque com quantidade igual a zero
    - Quando a validação for executada
    - Então deve lançar uma EstoqueBadRequestException com mensagem específica
    """
    service = EstoqueServices(None)
    estoque = Estoque(id=1, seller_id="vendedor1", sku="sku1", quantidade=0)

    with pytest.raises(EstoqueBadRequestException) as exc:
        service._validate_positive_estoque(estoque)

    detalhes = getattr(exc.value, "details", [])
    mensagem = str(detalhes[0].message) if detalhes else str(exc.value)
    assert "quantidade deve ser maior que zero." in mensagem


# ---------------- Testes de validação de estoque existente ---------------- #

@pytest.mark.asyncio
async def test_validate_non_existent_estoque_existente(mock_repository):
    """
    Testa a validação de estoque já existente.

    Cenário:
    - Dado um estoque já cadastrado para o seller_id e sku
    - Quando a validação for executada
    - Então deve lançar uma EstoqueBadRequestException com mensagem de estoque já cadastrado
    """
    mock_repository.find_by_seller_id_and_sku.return_value = Estoque(
        id=1, seller_id="vendedor1", sku="sku1", quantidade=10
    )

    service = EstoqueServices(mock_repository)

    with pytest.raises(EstoqueBadRequestException) as exc:
        await service._validate_non_existent_estoque("vendedor1", "sku1")

    detalhes = getattr(exc.value, "details", [])
    mensagem = str(detalhes[0].message) if detalhes else str(exc.value)
    assert "Estoque para produto já cadastrado." in mensagem