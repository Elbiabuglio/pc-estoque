from app.api.common.schemas import ResponseEntity, SchemaType
from app.models.estoque_model import Estoque


class EstoqueSchema(SchemaType):
    seller_id: str
    sku: str
    quantidade: int


class EstoqueResponse(EstoqueSchema, ResponseEntity):
    """Resposta adicionando"""


class EstoqueCreate(EstoqueSchema):
    """Schema para criação de Estoques"""

    def to_model(self) -> Estoque:
        return Estoque(**self.model_dump())


class EstoqueUpdate(SchemaType):
    """Permite apenas a atualização da quantidade"""
    quantidade: int
