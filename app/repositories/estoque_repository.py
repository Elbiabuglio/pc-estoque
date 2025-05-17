from uuid import UUID

from app.common.exceptions import NotFoundException

from ..models import Estoque
from .base import AsyncMemoryRepository


class EstoqueRepository(AsyncMemoryRepository[Estoque, UUID]):

    async def find_by_sku(self, sku: str) -> Estoque:
        """
        Busca um estoque pelo SKU.
        """
        result = next((s for s in self.memory if s["sku"] == sku), None)
        if result:
            return result
        raise NotFoundException()
    
    async def find_by_seller_id(self, seller_id: str) -> Estoque:
        """
        Busca um estoque pelo seller_id.
        """
        result = next((s for s in self.memory if s["seller_id"] == seller_id), None)
        if result:
            return result
        raise NotFoundException()
    
    async def find_by_seller_id_and_sku(self, seller_id: str, sku: str) -> Estoque:
        """
        Busca um estoque pelo seller_id e SKU.
        """
        result = next((s for s in self.memory if s["seller_id"] == seller_id and s["sku"] == sku), None)
        if result:
            return result
        raise NotFoundException()
    

__all__ = ["EstoqueRepository"]