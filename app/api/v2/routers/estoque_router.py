from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Header, status

from app.api.common.schemas import ListResponse, Paginator, get_request_pagination
from app.api.v1.schemas.estoque_schema import EstoqueCreate, EstoqueResponse, EstoqueUpdate
from app.services.estoque_service import EstoqueServices
from app.container import Container


router = APIRouter(prefix="/seller/v2/estoque", tags=["Estoque V2"])

@router.get(
    "",
    response_model=ListResponse[EstoqueResponse],
    status_code=status.HTTP_200_OK,
)
@inject
async def list_estoque_v2(
    x_seller_id: str = Header(..., alias="x-seller-id"),
    paginator: Paginator = Depends(get_request_pagination),
    estoque_service: EstoqueServices = Depends(Provide[Container.estoque_service]),
):
    result = await estoque_service.list(paginator=paginator, filters={"seller_id": x_seller_id})
    return paginator.paginate(results=result)

@router.get(
    "/{sku}",
    response_model=EstoqueResponse,
    status_code=status.HTTP_200_OK,
)
@inject
async def list_estoque_by_seller_and_sku_v2(
    sku: str,
    x_seller_id: str = Header(..., alias="x-seller-id"),
    estoque_service: EstoqueServices = Depends(Provide[Container.estoque_service]),
):
    return await estoque_service.find_by_seller_id_and_sku(x_seller_id, sku)

@router.post(
    "",
    response_model=EstoqueResponse,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_estoque_v2(
    estoque: EstoqueCreate,
    x_seller_id: str = Header(..., alias="x-seller-id"),
    estoque_service: EstoqueServices = Depends(Provide[Container.estoque_service]),
):
    estoque_model = estoque.to_model()
    estoque_model.seller_id = x_seller_id  # sobrescreve com valor do cabeçalho
    return await estoque_service.create(estoque_model)

@router.patch(
    "/{sku}",
    response_model=EstoqueResponse,
    status_code=status.HTTP_200_OK,
)
@inject 
async def update_estoque_by_seller_and_sku_v2(
    sku: str,
    estoque_update: EstoqueUpdate,
    x_seller_id: str = Header(..., alias="x-seller-id"),
    estoque_service: EstoqueServices = Depends(Provide[Container.estoque_service]),
):
    return await estoque_service.update(x_seller_id, sku, estoque_update)

@router.delete(
    "/{sku}",
    status_code=status.HTTP_200_OK,
)
@inject
async def delete_estoque_by_seller_and_sku_v2(
    sku: str,
    x_seller_id: str = Header(..., alias="x-seller-id"),
    estoque_service: EstoqueServices = Depends(Provide[Container.estoque_service]),
):
    return await estoque_service.delete(x_seller_id, sku)
