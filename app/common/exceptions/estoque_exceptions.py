from typing import TYPE_CHECKING

from app.common.exceptions import BadRequestException, NotFoundException

if TYPE_CHECKING:
    from app.api.common.schemas.response import ErrorDetail


class EstoqueNotFoundException(NotFoundException):
    def __init__(self, seller_id: str, sku: str, details: list["ErrorDetail"] | None = None):
        if details is None:
            from app.api.common.schemas.response import ErrorDetail

            details = [
                ErrorDetail(
                    message="Estoque para produto não encontrado.",
                    location= "body",
                    slug="estoque_nao_encontrado",
                    field="sku",
                    ctx={"seller_id": seller_id, "sku": sku},
                )
            ]
        super().__init__(details=details)


class EstoqueBadRequestException(BadRequestException):
    def __init__(self, message: str, field: str = None, value=None, details: list["ErrorDetail"] | None = None):
        if details is None:
            from app.api.common.schemas.response import ErrorDetail

            details = [
                ErrorDetail(
                    message=message,
                    location= "body",
                    slug="estoque_invalido",
                    field=field,
                    ctx={"value": value} if value is not None else {},
                )
            ]
        super().__init__(details=details)