from datetime import datetime
from typing import List
from sqlalchemy import Column, DateTime, Enum, Integer, String, select
from app.integrations.database.sqlalchemy_client import SQLAlchemyClient
from app.models.historico_estoque_model import HistoricoEstoque, TipoMovimentacaoEnum
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
    tipo_movimentacao = Column(Enum(TipoMovimentacaoEnum), nullable=False)
    movimentado_em = Column(DateTime(timezone=True), nullable=False, index=True)

class HistoricoEstoqueRepository:
    def __init__(self, sql_client: SQLAlchemyClient):
        self.sql_client = sql_client
        self.entity_base_class = HistoricoEstoqueBase
        self.model_class = HistoricoEstoque

    def to_model(self, base: HistoricoEstoqueBase | None) -> HistoricoEstoque | None:
        base_dict = self.sql_client.to_dict(base)
        if base_dict is None:
            return None
        return self.model_class.model_validate(base_dict)

    async def create(self, historico: HistoricoEstoque) -> HistoricoEstoque:
        """
        Salva um registro de histórico no banco de dados.
        """
        base = self.entity_base_class(
            seller_id=historico.seller_id,
            sku=historico.sku,
            quantidade_anterior=historico.quantidade_anterior,
            quantidade_nova=historico.quantidade_nova,
            tipo_movimentacao=historico.tipo_movimentacao,
            movimentado_em=historico.movimentado_em,
        )
        async with self.sql_client.make_session() as session:
            async with session.begin():
                session.add(base)
        return self.to_model(base)

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