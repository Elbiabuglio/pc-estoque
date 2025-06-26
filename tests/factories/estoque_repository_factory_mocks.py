from typing import Dict, Tuple, List
from unittest.mock import AsyncMock, Mock, MagicMock
from datetime import datetime, timezone

from app.models import Estoque
from app.repositories.estoque_repository import EstoqueRepository
from app.integrations.database.sqlalchemy_client import SQLAlchemyClient


class AsyncSessionMock(MagicMock):
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass


class EstoqueRepositoryMockFactory:
    """
    Factory para criar mocks do EstoqueRepository com comportamentos padronizados.
    """

    @staticmethod
    def create_mock_repository(initial_data: Dict[Tuple[str, str], Estoque] = None) -> EstoqueRepository:
        """
        Cria um mock do EstoqueRepository com comportamentos simulados.

        Args:
            initial_data: Dicionário {(seller_id, sku): Estoque}
                Se None, usa dados padrão.

        Returns:
            EstoqueRepository mockado com comportamentos simulados.
        """
        mock_sql_client = Mock(spec=SQLAlchemyClient)

        mock_sql_client.create = AsyncMock()
        mock_sql_client.find_by_seller_and_sku = AsyncMock()
        mock_sql_client.update_by_seller_and_sku = AsyncMock()
        mock_sql_client.delete_by_seller_and_sku = AsyncMock()
        mock_sql_client.make_session = AsyncMock(return_value=AsyncSessionMock())

        repository = EstoqueRepository(sql_client=mock_sql_client)

        if initial_data is None:
            initial_data = {
                ("1", "SKU1"): Estoque(id=1, seller_id="1", sku="SKU1", quantidade=100),
                ("2", "SKU2"): Estoque(id=2, seller_id="2", sku="SKU2", quantidade=200),
            }

        simulated_db = initial_data.copy()

        async def mock_create(estoque: Estoque):
            estoque.created_at = datetime.now(timezone.utc)
            simulated_db[(estoque.seller_id, estoque.sku)] = estoque
            return estoque

        async def mock_find_by_seller_and_sku(seller_id: str, sku: str):
            estoque = simulated_db.get((seller_id, sku))
            if estoque:
                return {
                    "id": estoque.id,
                    "seller_id": estoque.seller_id,
                    "sku": estoque.sku,
                    "quantidade": estoque.quantidade,
                    "created_at": getattr(estoque, 'created_at', None),
                    "updated_at": getattr(estoque, 'updated_at', None),
                    "created_by": getattr(estoque, 'created_by', None),
                    "updated_by": getattr(estoque, 'updated_by', None),
                }
            return None

        async def mock_update_by_seller_and_sku(seller_id: str, sku: str, estoque_update: Estoque):
            if (seller_id, sku) in simulated_db:
                updated_estoque = estoque_update
                updated_estoque.seller_id = seller_id
                updated_estoque.sku = sku
                simulated_db[(seller_id, sku)] = updated_estoque
                return updated_estoque.model_dump()
            raise ValueError("Estoque not found")

        async def mock_delete_by_seller_and_sku(seller_id: str, sku: str):
            if (seller_id, sku) in simulated_db:
                del simulated_db[(seller_id, sku)]
                return True
            return False

        async def mock_find(*args, **kwargs):
            return list(simulated_db.values())

        repository.create = AsyncMock(side_effect=mock_create)
        repository.find_by_seller_and_sku = AsyncMock(side_effect=mock_find_by_seller_and_sku)
        repository.update_by_seller_and_sku = AsyncMock(side_effect=mock_update_by_seller_and_sku)
        repository.delete_by_seller_and_sku = AsyncMock(side_effect=mock_delete_by_seller_and_sku)
        repository.find = AsyncMock(side_effect=mock_find)

        repository._simulated_db = simulated_db

        return repository

    @staticmethod
    def create_empty_mock_repository() -> EstoqueRepository:
        return EstoqueRepositoryMockFactory.create_mock_repository(initial_data={})

    @staticmethod
    def create_mock_repository_with_custom_data(estoques: List[Estoque]) -> EstoqueRepository:
        initial_data = {(e.seller_id, e.sku): e for e in estoques}
        return EstoqueRepositoryMockFactory.create_mock_repository(initial_data)