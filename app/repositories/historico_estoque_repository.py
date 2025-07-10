from datetime import datetime
from typing import List

from sqlalchemy import Column, DateTime, Integer, String, select

from app.integrations.database.sqlalchemy_client import SQLAlchemyClient
from app.models.historico_estoque_model import HistoricoEstoque
from app.repositories.base.sqlalchemy_crud_repository import SQLAlchemyCrudRepository
from app.repositories.base.sqlalchemy_entity_base import PersistableEntityBase


class HistoricoEstoqueBase(PersistableEntityBase):
    """
    Entidade SQLAlchemy para a tabela pc_estoque_historico.
    """
    __tablename__ = "pc_estoque_historico"

    seller_id = Column(String, nullable=False, index=True)
    sku = Column(String, nullable=False, index=True)
    quantidade_anterior = Column(Integer, nullable=False)
    quantidade_nova = Column(Integer, nullable=False)
    tipo_movimentacao = Column(String(20), nullable=False)
    movimentado_em = Column(DateTime(timezone=True), nullable=False, index=True)


class HistoricoEstoqueRepository(SQLAlchemyCrudRepository[HistoricoEstoque, HistoricoEstoqueBase]):
    """
    Repositório para operações na tabela de histórico de estoque.
    """
    def __init__(self, sql_client: SQLAlchemyClient):
        super().__init__(
            sql_client=sql_client,
            model_class=HistoricoEstoque(),
            entity_base_class=HistoricoEstoqueBase 
        )

    async def create(self, model: HistoricoEstoque) -> HistoricoEstoque:
        """
        Override do método create para contornar problemas de versão do Pydantic.
        Converte o modelo Pydantic para a entidade SQLAlchemy manualmente.
        """
        base = self.entity_base_class(
            id=model.id,  
            seller_id=model.seller_id,
            sku=model.sku,
            quantidade_anterior=model.quantidade_anterior,
            quantidade_nova=model.quantidade_nova,
            tipo_movimentacao=model.tipo_movimentacao.value,
            movimentado_em=model.movimentado_em,
        )

        async with self.sql_client.make_session() as session:
            async with session.begin():
                session.add(base)
        return self.to_model(base)

    def to_model(self, base: HistoricoEstoqueBase | None) -> HistoricoEstoque | None:
        """
        Override do método to_model para contornar problemas de versão do Pydantic.
        Converte a entidade do banco para o modelo Pydantic manualmente.
        """
        if base is None:
            return None

        return HistoricoEstoque(
            id=base.id,
            seller_id=base.seller_id,
            sku=base.sku,
            quantidade_anterior=base.quantidade_anterior,
            quantidade_nova=base.quantidade_nova,
            tipo_movimentacao=base.tipo_movimentacao,
            movimentado_em=base.movimentado_em,
        )

    async def find_by_period(
        self,
        start_date: datetime,
        end_date: datetime,
        seller_id: str | None = None
    ) -> List[HistoricoEstoque]:
        """
        Busca registros de histórico por período e, opcionalmente, por seller_id.
        """
        async with self.sql_client.make_session() as session:
            stmt = select(self.entity_base_class).where(
                self.entity_base_class.movimentado_em.between(start_date, end_date)
            )

            if seller_id:
                stmt = stmt.where(self.entity_base_class.seller_id == seller_id)

            stmt = stmt.order_by(self.entity_base_class.movimentado_em.desc())

            result = await session.execute(stmt)
            bases = result.scalars().all()

            return [self.to_model(base) for base in bases]