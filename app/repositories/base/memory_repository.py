from typing import Any, Generic, List, Optional, TypeVar
from uuid import UUID
from pydantic import BaseModel
from app.common.datetime import utcnow
from app.common.exceptions import NotFoundException
from .async_crud_repository import AsyncCrudRepository

T = TypeVar("T", bound=BaseModel)
ID = TypeVar("ID", bound=int | str | UUID)


class AsyncMemoryRepository(AsyncCrudRepository[T, ID], Generic[T, ID]):

    def __init__(self):
        super().__init__()
        self.memory: List[T] = []

    async def create(self, entity: T) -> T:
        entity = entity.copy(update={"created_at": utcnow()})
        self.memory.append(entity)
        return entity

    async def find_by_id(self, entity_id: ID) -> T:
        result = next((r for r in self.memory if getattr(r, "id", None) == entity_id), None)
        if result:
            return result
        raise NotFoundException()

    async def find(
        self,
        filters: dict,
        limit: int = 10,
        offset: int = 0,
        sort: Optional[dict] = None
    ) -> List[T]:
        # Filtro básico
        filtered_list = [
            item for item in self.memory
            if all(getattr(item, key, None) == value for key, value in filters.items())
        ]

        # TODO: Implementar ordenação se necessário (usando `sort`)
        return filtered_list[offset:offset + limit]

    async def update(self, entity_id: ID, entity: T) -> T:
        index = next((i for i, item in enumerate(self.memory) if getattr(item, "id", None) == entity_id), None)
        if index is None:
            raise NotFoundException()

        entity = entity.copy(update={"updated_at": utcnow()})
        self.memory[index] = entity
        return entity

    async def delete_by_id(self, entity_id: ID) -> None:
        index = next((i for i, item in enumerate(self.memory) if getattr(item, "id", None) == entity_id), None)
        if index is None:
            raise NotFoundException()
        del self.memory[index]
