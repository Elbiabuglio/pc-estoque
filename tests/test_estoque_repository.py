import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.models.estoque_model import Estoque
from app.repositories.estoque_repository import EstoqueRepository, EstoqueBase
from app.repositories.base.sqlalchemy_crud_repository import SQLAlchemyCrudRepository
from app.repositories.base.sqlalchemy_entity_base import SellerIdSkuPersistableEntityBase

from tests.fixtures.estoque_repository_fixtures import mock_sql_client, estoque_repository


# ---------------- Testes EstoqueRepository ---------------- #

@pytest.mark.asyncio
async def test_find_by_seller_id_and_sku_retorna_estoque_dict(estoque_repository):
    """
    Testa se a função find_by_seller_id_and_sku retorna o dicionário do estoque encontrado.

    Cenário:
    - Dado um seller_id e sku existentes
    - Quando a função for chamada
    - Então deve retornar o resultado do model_dump do estoque
    """
    seller_id, sku = "abc", "sku-abc"
    mock_estoque = Estoque(seller_id=seller_id, sku=sku, quantidade=10)

    with patch.object(SQLAlchemyCrudRepository, "find_by_seller_id_and_sku", new_callable=AsyncMock) as mock_super:
        mock_super.return_value = mock_estoque

        result = await estoque_repository.find_by_seller_id_and_sku(seller_id, sku)

        assert result == mock_estoque.model_dump()
        mock_super.assert_awaited_once_with(seller_id, sku)

@pytest.mark.asyncio
async def test_find_by_seller_id_and_sku_retorna_none(estoque_repository):
    """
    Testa se a função find_by_seller_id_and_sku retorna None quando não encontra o estoque.

    Cenário:
    - Dado um seller_id e sku inexistentes
    - Quando a função for chamada
    - Então deve retornar None
    """
    with patch.object(SQLAlchemyCrudRepository, "find_by_seller_id_and_sku", new_callable=AsyncMock) as mock_super:
        mock_super.return_value = None

        result = await estoque_repository.find_by_seller_id_and_sku("notfound", "sku-notfound")
        assert result is None

@pytest.mark.asyncio
async def test_find_by_seller_id_and_sku_sem_model_dump(estoque_repository):
    """
    Testa o comportamento da função find_by_seller_id_and_sku quando o retorno não possui model_dump.

    Cenário:
    - Dado um retorno inválido (classe sem model_dump)
    - Quando a função for chamada
    - Então deve lançar AttributeError
    """
    class Dummy: pass

    with patch.object(SQLAlchemyCrudRepository, "find_by_seller_id_and_sku", new_callable=AsyncMock) as mock_super:
        mock_super.return_value = Dummy()

        with pytest.raises(AttributeError):
            await estoque_repository.find_by_seller_id_and_sku("abc", "sku-abc")

@pytest.mark.asyncio
async def test_create_estoque_retorna_model_dump(estoque_repository):
    """
    Testa se a função create retorna corretamente o model_dump do estoque criado.

    Cenário:
    - Dado um estoque válido
    - Quando a função for chamada
    - Então deve retornar o model_dump do estoque criado
    """
    new_estoque = Estoque(seller_id="sellerX", sku="skuX", quantidade=42)

    with patch.object(SQLAlchemyCrudRepository, "create", new_callable=AsyncMock) as mock_super:
        mock_super.return_value = new_estoque.model_dump()

        result = await estoque_repository.create(new_estoque)

        assert result == new_estoque.model_dump()
        mock_super.assert_awaited_once_with(new_estoque)

@pytest.mark.asyncio
async def test_create_estoque_retorna_none(estoque_repository):
    """
    Testa se a função create retorna None ao tentar criar um estoque e falhar.

    Cenário:
    - Dado um estoque válido
    - Quando a função for chamada e o repositório retornar None
    - Então deve retornar None
    """
    new_estoque = Estoque(seller_id="sellerY", sku="skuY", quantidade=0)

    with patch.object(SQLAlchemyCrudRepository, "create", new_callable=AsyncMock) as mock_super:
        mock_super.return_value = None

        result = await estoque_repository.create(new_estoque)
        assert result is None

@pytest.mark.asyncio
async def test_update_by_seller_id_and_sku_sucesso(estoque_repository):
    """
    Testa a atualização de um estoque por seller_id e sku com sucesso.

    Cenário:
    - Dado um seller_id e sku existentes
    - Quando a função update_by_seller_id_and_sku for chamada
    - Então deve retornar o model_dump atualizado do estoque
    """
    seller_id, sku = "seller", "sku"
    estoque_update = Estoque(seller_id=seller_id, sku=sku, quantidade=99)

    with patch.object(SQLAlchemyCrudRepository, "update_by_seller_id_and_sku", new_callable=AsyncMock) as mock_super:
        mock_super.return_value = estoque_update.model_dump()

        result = await estoque_repository.update_by_seller_id_and_sku(seller_id, sku, estoque_update)

        assert result == estoque_update.model_dump()
        mock_super.assert_awaited_once_with(seller_id, sku, estoque_update)

@pytest.mark.asyncio
async def test_update_by_seller_id_and_sku_sem_retorno(estoque_repository):
    """
    Testa a atualização de um estoque quando o repositório não retorna valor.

    Cenário:
    - Dado um estoque válido
    - Quando a função update_by_seller_id_and_sku for chamada
    - Então deve retornar None se não houver retorno do repositório
    """
    seller_id, sku = "none", "sku-none"
    estoque_update = Estoque(seller_id=seller_id, sku=sku, quantidade=1)

    with patch.object(SQLAlchemyCrudRepository, "update_by_seller_id_and_sku", new_callable=AsyncMock) as mock_super:
        mock_super.return_value = None

        result = await estoque_repository.update_by_seller_id_and_sku(seller_id, sku, estoque_update)
        assert result is None

@pytest.mark.asyncio
async def test_delete_by_seller_id_and_sku_none(estoque_repository):
    """
    Testa a exclusão de um estoque quando o repositório não retorna valor.

    Cenário:
    - Dado um seller_id e sku válidos
    - Quando a função delete_by_seller_id_and_sku for chamada
    - Então deve retornar None se não houver retorno
    """
    seller_id, sku = "seller", "sku"

    with patch.object(SQLAlchemyCrudRepository, "delete_by_seller_id_and_sku", new_callable=AsyncMock) as mock_super:
        mock_super.return_value = None

        result = await estoque_repository.delete_by_seller_id_and_sku(seller_id, sku)
        assert result is None

@pytest.mark.asyncio
async def test_delete_by_seller_id_and_sku_com_retorno(estoque_repository):
    """
    Testa a exclusão de um estoque com retorno de confirmação.

    Cenário:
    - Dado um seller_id e sku válidos
    - Quando a função delete_by_seller_id_and_sku for chamada
    - Então deve retornar a confirmação do repositório
    """
    seller_id, sku = "seller", "sku"

    with patch.object(SQLAlchemyCrudRepository, "delete_by_seller_id_and_sku", new_callable=AsyncMock) as mock_super:
        mock_super.return_value = "removed"

        result = await estoque_repository.delete_by_seller_id_and_sku(seller_id, sku)
        assert result == "removed"

# ---------------- Testes EstoqueBase ---------------- #

def test_estoque_repository_herda_de_sqlalchemy_crud():
    """
    Verifica se EstoqueRepository herda corretamente de SQLAlchemyCrudRepository.
    """
    repo = EstoqueRepository(sql_client=MagicMock())
    assert isinstance(repo, SQLAlchemyCrudRepository)

def test_estoque_base_herda_de_entity_base():
    """
    Verifica se EstoqueBase herda de SellerIdSkuPersistableEntityBase.
    """
    assert issubclass(EstoqueBase, SellerIdSkuPersistableEntityBase)

def test_estoque_base_coluna_quantidade_configuracao():
    """
    Verifica a configuração da coluna 'quantidade' em EstoqueBase.

    Cenário:
    - A coluna deve ser não nula
    - O tipo python associado deve ser int
    """
    col = EstoqueBase.__dict__["quantidade"]
    assert col.nullable is False
    assert hasattr(col.type, "python_type")
    assert col.type.python_type is int

def test_estoque_base_tablename():
    """
    Verifica se o nome da tabela em EstoqueBase está configurado corretamente.
    """
    assert EstoqueBase.__tablename__ == "pc_estoque"