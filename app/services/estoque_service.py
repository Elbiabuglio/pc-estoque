from ..models.estoque_model import Estoque
from ..repositories import estoque_repository
from .base import CrudService


class EstoqueServices(CrudService[Estoque, int]):
    def __init__(self, repository: estoque_repository):
        super().__init__(repository)

    async def find_by_sku(self, sku: str) -> Estoque:
        """
        Busca um estoque pelo SKU.
        """
        return await self.repository.find_by_sku(sku=sku)
    
    async def find_by_seller_id(self, seller_id: str) -> Estoque:
        """
        Busca um estoque pelo seller_id.
        """
        return await self.repository.find_by_seller_id(seller_id=seller_id)  
       
    async def find_by_seller_id_and_sku(self, seller_id: str, sku: str) -> Estoque:
        """
        Busca um estoque pelo seller_id e SKU.
        """
        return await self.repository.find_by_seller_id_and_sku(seller_id=seller_id, sku=sku)
    
    async def create(self, estoque: Estoque) -> Estoque:
        """
        Cria um novo estoque.
        """
        return await self.repository.create(estoque)
    
    async def update(self, seller_id: str, sku: str, estoque: Estoque) -> Estoque:
        """
        Atualiza um estoque existente.
        """
        return await self.repository.update(seller_id=seller_id, sku=sku, estoque=estoque)
    
    async def delete(self, seller_id: str, sku: str) -> Estoque:
        """
        Deleta um estoque existente.
        """
        return await self.repository.delete(seller_id=seller_id, sku=sku)
    
    