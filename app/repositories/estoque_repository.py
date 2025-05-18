from uuid import UUID
from app.common.datetime import utcnow
from app.common.exceptions import NotFoundException
from ..models import Estoque
from .base import AsyncMemoryRepository


class EstoqueRepository(AsyncMemoryRepository[Estoque, UUID]):
    
    async def find_by_seller_id_and_sku(self, seller_id: str, sku: str) -> Estoque:
        """
        Busca um estoque pelo seller_id e SKU.
        """
        result = next(
            (s for s in self.memory if s.seller_id == seller_id and s.sku == sku),
            None
        )
        if result:
            return result
        raise NotFoundException()

    async def create(self, item: Estoque) -> Estoque:
        """
        Cria um novo estoque.
        """
        self.memory.append(item)
        return item

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