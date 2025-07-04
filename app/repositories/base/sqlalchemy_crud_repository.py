from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from app.integrations.database.sqlalchemy_client import SQLAlchemyClient

from app.models import PersistableEntity, QueryModel, Estoque

from .async_crud_repository import AsyncCrudRepository
from .sqlalchemy_entity_base import PersistableEntityBase

from app.common.datetime import utcnow

T = TypeVar("T", bound=PersistableEntity)  # Modelo Pydantic
B = TypeVar("B", bound=PersistableEntityBase)  # Entidade base do SQLAlchemy
Q = TypeVar("Q", bound=QueryModel)

from pclogging import LoggingBuilder

LoggingBuilder.init(log_level="DEBUG")

logger = LoggingBuilder.get_logger(__name__)

class SQLAlchemyCrudRepository(AsyncCrudRepository[T], Generic[T, B]):
    """
    Implementação de AsyncCrudRepository com o SQLAlchemy.
    Ponto de atenção: Cada método possui uma transação única.
    """

    def __init__(self, sql_client: SQLAlchemyClient, model_class: T, entity_base_class: B):
        self.sql_client = sql_client
        self.model_class = model_class
        self.entity_base_class = entity_base_class
        self.pk_fields = self.sql_client.get_pk_fields(self.entity_base_class)

    def to_base(self, model: T) -> B:
        model_dict = model.model_dump()
        base = self.entity_base_class()
        for field, value in model_dict.items():
            if hasattr(base, field):
                setattr(base, field, value)
        return base

    def to_model(self, base: B | None) -> T | None:
        base_dict = self.sql_client.to_dict(base)
        if base_dict is None:
            return None
        model = self.model_class.model_validate(base_dict)
        return model

    async def create(self, model: T) -> T:
        base = self.to_base(model)
        async with self.sql_client.make_session() as session:
            async with session.begin():
                session.add(base)
        created_model = self.to_model(base)
        logger.info(f"Entidade criada: {created_model}")
        return created_model

    async def _find_base_by_seller_id_sku_on_session(self, seller_id: str, sku: str, session) -> B | None:
        estoque = self.sql_client.init_select_estoque(self.entity_base_class)
        estoque = estoque.where(self.entity_base_class.seller_id == seller_id).where(self.entity_base_class.sku == sku)
        scalar = await session.execute(estoque)
        base = scalar.scalar_one_or_none()
        return base

    async def find_by_seller_id_and_sku(self, seller_id: str, sku: str) -> T | None:
        async with self.sql_client.make_session() as session:
            base = await self._find_base_by_seller_id_sku_on_session(seller_id, sku, session)
        model = self.to_model(base)
        return model

    def _apply_sort(self, stmt, sort: dict):
        for field, direction in sort.items():
            if hasattr(self.entity_base_class, field):
                column = getattr(self.entity_base_class, field)
                stmt = stmt.order_by(column.desc() if direction == -1 else column.asc())
        return stmt

    async def find(self, filters: Q, limit: int = 20, offset: int = 0, sort: dict | None = None) -> list[T]:
        def apply_operator(stmt, column, op, v):
            if op == "$lt":
                return stmt.where(column < v)
            elif op == "$lte":
                return stmt.where(column <= v)
            elif op == "$gt":
                return stmt.where(column > v)
            elif op == "$gte":
                return stmt.where(column >= v)
            return stmt

        async with self.sql_client.make_session() as session:
            stmt = self.sql_client.init_select_estoque(self.entity_base_class)
            if hasattr(filters, "to_query_dict") and callable(filters.to_query_dict):
                filters_dict = filters.to_query_dict()
            elif hasattr(filters, "dict") and callable(filters.dict):
                filters_dict = filters.dict()
            elif isinstance(filters, dict):
                filters_dict = filters
            else:
                logger.error("O parâmetro filters deve ser conversível para dicionário.")
                raise TypeError("O parâmetro filters deve ser conversível para dicionário.")

            for field, value in filters_dict.items():
                if hasattr(self.entity_base_class, field):
                    stmt = stmt.where(getattr(self.entity_base_class, field) == value)

            stmt = stmt.limit(limit).offset(offset)
            result = await session.execute(stmt)
            bases = result.scalars().all()
            models = [model for base in bases if (model := self.to_model(base)) is not None]
            return models
        
    async def delete_by_seller_id_and_sku(self, seller_id: str, sku: str) -> bool:
        async with self.sql_client.make_session() as session:
            async with session.begin():
                stmt = self.sql_client.init_delete_estoque(self.entity_base_class)
                stmt = stmt.where(self.entity_base_class.seller_id == seller_id).where(
                    self.entity_base_class.sku == sku
                )
                result = await session.execute(stmt)
            deleted = result.rowcount > 0
            if deleted:
                logger.info(f"Entidade deletada: seller_id={seller_id}, sku={sku}")
            return deleted

    async def update_by_seller_id_and_sku(self, seller_id: str, sku: str, model: T) -> T | None:
        async with self.sql_client.make_session() as session:
            async with session.begin():
                base = await self._find_base_by_seller_id_sku_on_session(seller_id, sku, session)
                if can_update := base is not None:
                    base.updated_at = utcnow()
                    for key, value in model.model_dump().items():
                        if key not in self.pk_fields:
                            setattr(base, key, value)
                    base.updated_at = utcnow()
            if can_update:
                await session.commit()
                logger.info(f"Entidade atualizada: seller_id={seller_id}, sku={sku}")
        model = self.to_model(base)
        return model

    async def patch_by_seller_id_and_sku(self, seller_id, sku, patch_entity):
        async with self.sql_client.make_session() as session:
            async with session.begin():
                base = await self._find_base_by_seller_id_sku_on_session(seller_id, sku, session)
                if not base:
                    return None
                for field, value in patch_entity.model_dump().items():
                    if value is not None and hasattr(base, field):
                        setattr(base, field, value)
            updated_model = self.to_model(base)
            logger.info(f"Entidade parcialmente atualizada: seller_id={seller_id}, sku={sku}")
            return updated_model
