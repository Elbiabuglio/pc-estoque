import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.models.estoque_model import Estoque
from app.repositories.estoque_repository import EstoqueRepository, EstoqueBase
from app.repositories.base.sqlalchemy_crud_repository import SQLAlchemyCrudRepository
from app.repositories.base.sqlalchemy_entity_base import SellerIdSkuPersistableEntityBase

# ---------------- Fixtures ---------------- #

@pytest.fixture
def mock_sql_client():
    mock_client = MagicMock()
    mock_client.session = AsyncMock()
    return mock_client

@pytest.fixture
def estoque_repository(mock_sql_client):
    return EstoqueRepository(sql_client=mock_sql_client)

# ---------------- Testes EstoqueRepository ---------------- #

@pytest.mark.asyncio
async def test_find_by_seller_id_and_sku_retorna_estoque_dict(estoque_repository):
    seller_id, sku = "abc", "sku-abc"
    mock_estoque = Estoque(seller_id=seller_id, sku=sku, quantidade=10)

    with patch.object(SQLAlchemyCrudRepository, "find_by_seller_id_and_sku", new_callable=AsyncMock) as mock_super:
        mock_super.return_value = mock_estoque

        result = await estoque_repository.find_by_seller_id_and_sku(seller_id, sku)

        assert result == mock_estoque.model_dump()
        mock_super.assert_awaited_once_with(seller_id, sku)

@pytest.mark.asyncio
async def test_find_by_seller_id_and_sku_retorna_none(estoque_repository):
    with patch.object(SQLAlchemyCrudRepository, "find_by_seller_id_and_sku", new_callable=AsyncMock) as mock_super:
        mock_super.return_value = None

        result = await estoque_repository.find_by_seller_id_and_sku("notfound", "sku-notfound")
        assert result is None

@pytest.mark.asyncio
async def test_find_by_seller_id_and_sku_sem_model_dump(estoque_repository):
    class Dummy: pass

    with patch.object(SQLAlchemyCrudRepository, "find_by_seller_id_and_sku", new_callable=AsyncMock) as mock_super:
        mock_super.return_value = Dummy()

        with pytest.raises(AttributeError):
            await estoque_repository.find_by_seller_id_and_sku("abc", "sku-abc")

@pytest.mark.asyncio
async def test_create_estoque_retorna_model_dump(estoque_repository):
    new_estoque = Estoque(seller_id="sellerX", sku="skuX", quantidade=42)

    with patch.object(SQLAlchemyCrudRepository, "create", new_callable=AsyncMock) as mock_super:
        mock_super.return_value = new_estoque.model_dump()

        result = await estoque_repository.create(new_estoque)

        assert result == new_estoque.model_dump()
        mock_super.assert_awaited_once_with(new_estoque)

@pytest.mark.asyncio
async def test_create_estoque_retorna_none(estoque_repository):
    new_estoque = Estoque(seller_id="sellerY", sku="skuY", quantidade=0)

    with patch.object(SQLAlchemyCrudRepository, "create", new_callable=AsyncMock) as mock_super:
        mock_super.return_value = None

        result = await estoque_repository.create(new_estoque)
        assert result is None

@pytest.mark.asyncio
async def test_update_by_seller_id_and_sku_sucesso(estoque_repository):
    seller_id, sku = "seller", "sku"
    estoque_update = Estoque(seller_id=seller_id, sku=sku, quantidade=99)

    with patch.object(SQLAlchemyCrudRepository, "update_by_seller_id_and_sku", new_callable=AsyncMock) as mock_super:
        mock_super.return_value = estoque_update.model_dump()

        result = await estoque_repository.update_by_seller_id_and_sku(seller_id, sku, estoque_update)

        assert result == estoque_update.model_dump()
        mock_super.assert_awaited_once_with(seller_id, sku, estoque_update)

@pytest.mark.asyncio
async def test_update_by_seller_id_and_sku_sem_retorno(estoque_repository):
    seller_id, sku = "none", "sku-none"
    estoque_update = Estoque(seller_id=seller_id, sku=sku, quantidade=1)

    with patch.object(SQLAlchemyCrudRepository, "update_by_seller_id_and_sku", new_callable=AsyncMock) as mock_super:
        mock_super.return_value = None

        result = await estoque_repository.update_by_seller_id_and_sku(seller_id, sku, estoque_update)
        assert result is None

@pytest.mark.asyncio
async def test_delete_by_seller_id_and_sku_none(estoque_repository):
    seller_id, sku = "seller", "sku"

    with patch.object(SQLAlchemyCrudRepository, "delete_by_seller_id_and_sku", new_callable=AsyncMock) as mock_super:
        mock_super.return_value = None

        result = await estoque_repository.delete_by_seller_id_and_sku(seller_id, sku)
        assert result is None

@pytest.mark.asyncio
async def test_delete_by_seller_id_and_sku_com_retorno(estoque_repository):
    seller_id, sku = "seller", "sku"

    with patch.object(SQLAlchemyCrudRepository, "delete_by_seller_id_and_sku", new_callable=AsyncMock) as mock_super:
        mock_super.return_value = "removed"

        result = await estoque_repository.delete_by_seller_id_and_sku(seller_id, sku)
        assert result == "removed"

# ---------------- Testes EstoqueBase ---------------- #

def test_estoque_repository_herda_de_sqlalchemy_crud():
    repo = EstoqueRepository(sql_client=MagicMock())
    assert isinstance(repo, SQLAlchemyCrudRepository)

def test_estoque_base_herda_de_entity_base():
    assert issubclass(EstoqueBase, SellerIdSkuPersistableEntityBase)

def test_estoque_base_coluna_quantidade_configuracao():
    col = EstoqueBase.__dict__["quantidade"]
    assert col.nullable is False
    assert hasattr(col.type, "python_type")
    assert col.type.python_type is int

def test_estoque_base_tablename():
    assert EstoqueBase.__tablename__ == "pc_estoque"