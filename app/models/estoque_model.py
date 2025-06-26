from app.models.base import SellerSkuIntPersistableEntity


class Estoque(SellerSkuIntPersistableEntity):
    quantidade: int
    