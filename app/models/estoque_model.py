from app.models.base import PersistableEntity


class Estoque(PersistableEntity):
    seller_id: str
    sku: str
    quantidade: int
    