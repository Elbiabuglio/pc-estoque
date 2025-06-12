from uuid import UUID
from app.common.datetime import utcnow
from app.common.exceptions import NotFoundException
from ..models import Estoque
from .base import AsyncMemoryRepository
from sqlalchemy import Column, Integer

from .base.sqlalchemy_crud_repository import SQLAlchemyCrudRepository
from .base.sqlalchemy_entity_base import SellerIdSkuPersistableEntityBase
from app.integrations.database.sqlalchemy_client import SQLAlchemyClient

class EstoqueBase(SellerIdSkuPersistableEntityBase):
    __tablename__ = "pc_estoque"

    quantidade = Column(Integer, nullable=False)

class EstoqueRepository(SQLAlchemyCrudRepository[Estoque, EstoqueBase]):
    
    def __init__(self, sql_client: SQLAlchemyClient):
        """
        Inicializa o repositório de estoque com o cliente SQLAlchemy.
        """
        super().__init__(sql_client=sql_client, model_class=Estoque, entity_base_class=EstoqueBase)

    async def find_by_seller_id_and_sku(self, seller_id: str, sku: str) -> Estoque:
        """
        Busca um estoque pelo seller_id e SKU.
        """
        result = await super().find_by_seller_id_and_sku(seller_id, sku)
        result = result.model_dump() if result else None

    async def create(self, item: Estoque) -> Estoque:
        """
        Cria um novo estoque.
        """
        return await super().create(item)

    async def update(self, seller_id: str, sku: str, quantidade: int) -> Estoque:
        """
        Atualiza um estoque existente.
        """
        estoque = await self.find_by_seller_id_and_sku(seller_id, sku)
        estoque.quantidade = quantidade
        estoque.updated_at = utcnow()
        for index, item in enumerate(self.memory):
            if item.id == estoque.id:
                self.memory[index] = estoque
                return estoque
        raise NotFoundException()

    async def delete(self, item_id: UUID) -> None:
        """
        Deleta um estoque pelo ID.
        """
        for index, item in enumerate(self.memory):
            if item.id == item_id:
                del self.memory[index]
                return
        raise NotFoundException()

    async def list(self) -> list[Estoque]:
        """
        Lista todos os estoques.
        """
        return list(self.memory)  # Retorna cópia para segurança


__all__ = ["EstoqueRepository"]