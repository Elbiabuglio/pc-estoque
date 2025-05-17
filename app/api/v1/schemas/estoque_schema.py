from app.api.common.schemas import ResponseEntity, SchemaType


class EstoqueSchema(SchemaType):
    seller_id: str
    sku: str
    quantidade: int


class EstoqueResponse(EstoqueSchema, ResponseEntity):
    """Resposta adicionando"""


class EstoqueCreate(EstoqueSchema):
    """Schema para criação de Estoques"""


class EstoqueUpdate(SchemaType):
    """Permite apenas a atualização da quantidade"""
    quantidade: int

