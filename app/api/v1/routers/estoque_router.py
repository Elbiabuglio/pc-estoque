from typing import TYPE_CHECKING

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.api.common.schemas import ListResponse, Paginator, UuidType, get_request_pagination
from app.api.v1.routers import ESTOQUE_PREFIX
from app.container import Container

from app.api.v1.schemas.estoque_schema import EstoqueCreate, EstoqueResponse, EstoqueUpdate
from app.services.estoque_service import EstoqueServices


router = APIRouter(prefix="", tags=["Algumas Coisas"])

# Listar todo estoque

@router.get(
    "/",
    response_model=ListResponse[EstoqueResponse],
    status_code=status.HTTP_200_OK,
)
@inject
async def list_estoque(
    paginator: Paginator = Depends(get_request_pagination),
    estoque_service: EstoqueServices = Depends(Provide[Container.estoque_service]),
) -> ListResponse[EstoqueResponse]:
    """
    Listar todos os estoques
    """
    result = await estoque_service.find(paginator)
    return result
# Listar estoque por seller_id e sku

@router.get(
    "/seller/{seller_id}",
    response_model=ListResponse[EstoqueResponse],
    status_code=status.HTTP_200_OK,
)
@inject
async def list_estoque_by_seller(
    seller_id: str,
    paginator: Paginator = Depends(get_request_pagination),
    estoque_service: EstoqueServices = Depends(Provide[Container.estoque_service]),
) -> ListResponse[EstoqueResponse]:
    """
    Listar estoques por seller_id
    """
    result = await estoque_service.find_by_seller_id(seller_id, paginator)
    return result

# Listar estoque por seller_id

@router.get(
    "/{seller_id}/{sku}",
    response_model=EstoqueResponse,
    status_code=status.HTTP_200_OK,
)
@inject
async def list_estoque_by_seller_and_sku(
    seller_id: str,
    sku: str,
    estoque_service: EstoqueServices = Depends(Provide[Container.estoque_service]),
) -> EstoqueResponse:
    """
    Listar estoque por seller_id e sku
    """
    result = await estoque_service.find_by_seller_id_and_sku(seller_id, sku)
    return result

# Criar estoque
@router.post(
    "/",
    response_model=EstoqueResponse,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_estoque(
    estoque: EstoqueCreate,
    estoque_service: EstoqueServices = Depends(Provide[Container.estoque_service]),
) -> EstoqueResponse:
    """
    Criar um novo estoque
    """
    result = await estoque_service.create(estoque)
    return result

# Atualizar estoque por seller_id e sku
@router.put(
    "/estoque/seller/{seller_id}/sku/{sku}",
    response_model=EstoqueResponse,
    status_code=status.HTTP_200_OK,
)
@inject 
async def update_estoque_by_seller_and_sku(
    seller_id: str,
    sku: str,
    estoque: EstoqueUpdate,
    estoque_service: EstoqueServices = Depends(Provide[Container.estoque_service]),
) -> EstoqueResponse:
    """
    Atualizar um estoque por seller_id e sku
    """
    result = await estoque_service.update(seller_id, sku, estoque)
    return result


# Deletar estoque por seller_id e sku
@router.delete(
    "/{seller_id}/{sku}",
    response_model=EstoqueResponse,
    status_code=status.HTTP_200_OK,
)
@inject
async def delete_estoque_by_seller_and_sku(
    seller_id: str,
    sku: str,
    estoque_service: EstoqueServices = Depends(Provide[Container.estoque_service]),
) -> EstoqueResponse:
    """
    Deletar um estoque por seller_id e sku
    """
    result = await estoque_service.delete(seller_id, sku)
    return result