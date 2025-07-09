from typing import Any, Dict, Optional, TypeVar

from app.integrations.database.sqlalchemy_client import SQLAlchemyClient
from app.models.estoque_model import Estoque

from .base.sqlalchemy_crud_repository import SQLAlchemyCrudRepository
from .base.sqlalchemy_entity_base import SellerIdSkuPersistableEntityBase

T = TypeVar("T", bound=Estoque)
B = TypeVar("B", bound=SellerIdSkuPersistableEntityBase)

from sqlalchemy import Column, Integer, select


class EstoqueBase(SellerIdSkuPersistableEntityBase):
    __tablename__ = "pc_estoque"
    quantidade = Column(Integer, nullable=False)

class EstoqueRepository(SQLAlchemyCrudRepository[Estoque, EstoqueBase]):

    def __init__(self, sql_client: SQLAlchemyClient):
        """
        Inicializa o repositório de preços com o cliente SQLAlchemy.
        :param sql_client: Instância do cliente SQLAlchemy.
        """
        super().__init__(sql_client=sql_client, model_class=Estoque, entity_base_class=EstoqueBase)


    async def find_by_seller_id_and_sku(self, seller_id: str, sku: str) -> Optional[Dict[str, Any]]:
        """
        Busca um estoque pela junção de seller_id + sku

        :param seller_id: ID do vendedor.
        :param sku: Código do produto.
        :return: Dicionário do estoque encontrado.
        """

        result = await super().find_by_seller_id_and_sku(seller_id, sku)
        result = result.model_dump() if result else None

        return result
    
    async def find_all_below_threshold(self, threshold: int) -> list[Estoque]:
        """
        Encontra todos os registros de estoque que estão abaixo ou no limite especificado.
        """
        async with self.sql_client.make_session() as session:
            stmt = select(self.entity_base_class).where(
                self.entity_base_class.quantidade <= threshold
            )
            result = await session.execute(stmt)
            entities = result.scalars().all()
            return [Estoque.model_validate(entity) for entity in entities]

    async def update_by_seller_id_and_sku(self, seller_id: str, sku: str, estoque_update: Estoque) -> Dict[str, Any]:
        """
        Atualiza um estoque na memória pela junção de seller_id + sku.

        :param seller_id: ID do vendedor.
        :param sku: Código do produto.
        :param estoque_update: Dicionário com os dados a serem atualizados.
        :return: True se encontrado, False caso contrário.
        """
        result = await super().update_by_seller_id_and_sku(seller_id, sku, estoque_update)
        return result

    async def delete_by_seller_id_and_sku(self, seller_id: str, sku: str) -> None:
        """
        Remove um estoque da memória com base no ID.

        :param seller_id: ID do vendedor.
        :param sku: Código do produto.
        :return: None
        """
        deleted = await super().delete_by_seller_id_and_sku(seller_id, sku)
        return deleted


__all__ = ["EstoqueRepository"]