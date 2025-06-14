from pydantic import Field
from app.api.common.schemas import ResponseEntity, SchemaType
from app.models.estoque_model import Estoque


class EstoqueSchema(SchemaType): 
    sku: str = Field(..., min_length=1, description="sku não pode ser vazio") 
    quantidade: int = Field(..., ge=0, description="quantidade deve ser maior ou igual a zero")

class EstoqueResponseV2(EstoqueSchema, ResponseEntity):
    """Resposta adicionando"""

class EstoqueCreateV2(EstoqueSchema):
    """Schema para criação de Estoques"""

    def to_model(self) -> Estoque:
        return Estoque(**self.dict(exclude_unset=True))

class EstoqueUpdateV2(SchemaType):
    """Permite apenas a atualização da quantidade"""
    quantidade: int = Field(..., ge=0, description="Quantidade deve ser maior ou igual a zero")