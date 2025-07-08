from datetime import datetime

from pydantic import Field

from app.api.common.schemas import ResponseEntity, SchemaType
from app.models.historico_estoque_model import TipoMovimentacaoEnum


class HistoricoEstoqueResponse(ResponseEntity, SchemaType):
    """Schema de resposta para um registro de histórico de estoque."""
    
    seller_id: str = Field(..., description="ID do Vendedor")
    sku: str = Field(..., description="SKU do Produto")
    quantidade_anterior: int = Field(..., description="Quantidade antes da movimentação")
    quantidade_nova: int = Field(..., description="Quantidade após a movimentação")
    tipo_movimentacao: TipoMovimentacaoEnum = Field(..., description="Tipo da movimentação")
    movimentado_em: datetime = Field(..., description="Data e hora da movimentação")

    class Config:
        orm_mode = True