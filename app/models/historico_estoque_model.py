from sqlalchemy import Column, Integer, String, DateTime, Enum as SAEnum
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class TipoMovimentacaoEnum(str, enum.Enum):
    CRIACAO = "CRIACAO"
    ATUALIZACAO = "ATUALIZACAO"
    EXCLUSAO = "EXCLUSAO"

class HistoricoEstoque(Base):
    __tablename__ = "pc_estoque_historico"

    id = Column(Integer, primary_key=True, autoincrement=True)  # <-- Adicione esta linha
    seller_id = Column(String, nullable=False)
    sku = Column(String, nullable=False)
    quantidade_anterior = Column(Integer, nullable=False)
    quantidade_nova = Column(Integer, nullable=False)
    movimentado_em = Column(DateTime, nullable=False)
    tipo_movimentacao = Column(SAEnum(TipoMovimentacaoEnum), nullable=False)