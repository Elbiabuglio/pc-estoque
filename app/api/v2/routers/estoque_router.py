import json
from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from pclogging import LoggingBuilder

from app.api.common.auth_handler import do_auth
from app.api.common.dependencies import get_required_seller_id
from app.api.common.schemas import ListResponse, Paginator
from app.api.common.schemas.pagination import get_request_pagination
from app.api.v2.schemas.estoque_schema import EstoqueCreateV2, EstoqueResponseV2, EstoqueUpdateV2
from app.container import Container
from app.models.estoque_model import Estoque
from app.services import EstoqueServices

router = APIRouter(prefix="/estoque", tags=["Estoque V2"], dependencies=[Depends(do_auth)])

logger = LoggingBuilder.get_logger(__name__)

@router.get(
    "",
    response_model=ListResponse[EstoqueResponseV2],
    status_code=status.HTTP_200_OK,
    summary="Lista todo o estoque",
)
@inject
async def list_estoque_v2(
    seller_id: str = Depends(get_required_seller_id),
    quantity: Optional[int] = None,  
    paginator: Paginator = Depends(get_request_pagination),
    estoque_service: EstoqueServices = Depends(Provide[Container.estoque_service]),
):
    """
    Lista os itens de estoque de um vendedor com filtros e paginação.

    Recupera uma lista paginada de todos os itens de estoque pertencentes
    ao `seller_id` associado ao token de autenticação. Permite a filtragem
    opcional por quantidade.

    Args:
        seller_id (str): O ID do vendedor, extraído do token JWT.
        quantity (Optional[int]): Filtro opcional para listar apenas itens
                                  com uma quantidade específica.
        paginator (Paginator): Dependência para controle de paginação (limit/offset).
        estoque_service (EstoqueServices): Injeção de dependência do serviço de estoque.

    Returns:
        ListResponse[EstoqueResponseV2]: Uma resposta paginada contendo a lista
                                         de itens de estoque e metadados de paginação.
    """
    logger.info(f"Listando estoque para seller_id={seller_id} com quantity={quantity}")
    filters = {"seller_id": seller_id}
    if quantity is not None:
        filters["quantidade"] = str(quantity)
    result = await estoque_service.list(paginator=paginator, filters=filters)
    return paginator.paginate(results=result)

@router.get(
    "/{sku}",
    response_model=EstoqueResponseV2,
    status_code=status.HTTP_200_OK,
    response_model_exclude_unset=True,
    summary="Busca um item do estoque por SKU",  
)
@inject
async def list_estoque_by_seller_and_sku_v2(
    sku: str,
    seller_id: str = Depends(get_required_seller_id),
    estoque_service: EstoqueServices = Depends(Provide[Container.estoque_service]),
):
    """
    Busca um item de estoque específico por SKU para um vendedor.

    Recupera os detalhes de um único item de estoque com base no seu SKU e no
    `seller_id` do usuário autenticado.

    Args:
        sku (str): O SKU (Stock Keeping Unit) do produto a ser buscado.
        seller_id (str): O ID do vendedor, extraído do token JWT.
        estoque_service (EstoqueServices): Injeção de dependência do serviço de estoque.

    Returns:
        EstoqueResponseV2: O objeto de estoque correspondente ao SKU e vendedor.

    Raises:
        HTTPException (404 Not Found): Se nenhum item de estoque for encontrado
                                       para a combinação de SKU e vendedor.
    """
    logger.info(f"Buscando estoque para seller_id={seller_id}, sku={sku}")
    
    if estoque_service is None:
        logger.error("Estoque service não encontrado")
        raise HTTPException(status_code=404, detail="Estoque service not found")
    estoque = await estoque_service.get_by_seller_id_and_sku(seller_id, sku)
    if estoque is None:
        logger.warning(f"Estoque não encontrado para seller_id={seller_id}, sku={sku}")
        raise HTTPException(status_code=404, detail="Estoque não encontrado")
    return estoque


@router.post(
    "",
    response_model=EstoqueResponseV2,
    status_code=status.HTTP_201_CREATED,
    summary="Insere um novo item no estoque",
)
@inject
async def create_estoque_v2(
    estoque: EstoqueCreateV2,
    seller_id: str = Depends(get_required_seller_id),
    estoque_service: EstoqueServices = Depends(Provide[Container.estoque_service]),
):
    """
    Cria um novo item de estoque para o vendedor autenticado.

    Registra um novo produto no sistema de estoque. O `seller_id` é
    automaticamente associado com base no token de autenticação.

    Args:
        estoque (EstoqueCreateV2): O corpo da requisição contendo o `sku` e a `quantidade`.
        seller_id (str): O ID do vendedor, extraído do token JWT.
        estoque_service (EstoqueServices): Injeção de dependência do serviço de estoque.

    Returns:
        EstoqueResponseV2: O objeto de estoque recém-criado.

    Raises:
        HTTPException (400 Bad Request): Se um item de estoque com o mesmo SKU
                                         já existir para este vendedor.
    """
    logger.info(f"Criando estoque para seller_id={seller_id}, dados={estoque.model_dump(exclude_unset=True)}")
    data = estoque.model_dump(exclude_unset=True)
    data["seller_id"] = seller_id
    estoque_model = Estoque(**data)
    result = await estoque_service.create(estoque_model)
    logger.info(f"Estoque criado para seller_id={seller_id}, sku={result.sku}")
    return result

@router.patch(
    "/{sku}",
    response_model=EstoqueResponseV2,
    status_code=status.HTTP_200_OK,
    summary="Atualiza a quantidade de um item no estoque",
)
@inject 
async def update_estoque_by_seller_and_sku_v2(
    sku: str,
    estoque_update: EstoqueUpdateV2,
    seller_id: str = Depends(get_required_seller_id),
    estoque_service: EstoqueServices = Depends(Provide[Container.estoque_service]),
):
    """
    Atualiza a quantidade de um item de estoque existente.

    Modifica a quantidade de um produto específico no estoque, identificado
    pelo seu SKU e pelo `seller_id` do usuário autenticado.

    Args:
        sku (str): O SKU do item de estoque a ser atualizado.
        estoque_update (EstoqueUpdateV2): O corpo da requisição com a nova `quantidade`.
        seller_id (str): O ID do vendedor, extraído do token JWT.
        estoque_service (EstoqueServices): Injeção de dependência do serviço de estoque.

    Returns:
        EstoqueResponseV2: O objeto de estoque com a quantidade atualizada.

    Raises:
        HTTPException (404 Not Found): Se o item de estoque não for encontrado.
    """
    logger.info(f"Atualizando estoque para seller_id={seller_id}, sku={sku}, nova quantidade={estoque_update.quantidade}")
    result = await estoque_service.update(seller_id, sku, estoque_update.quantidade)
    if result is None:
        logger.warning(f"Estoque não encontrado para update - seller_id={seller_id}, sku={sku}")
        raise HTTPException(status_code=404, detail="Estoque não encontrado")
    logger.info(f"Estoque atualizado para seller_id={seller_id}, sku={sku}")
    return result

@router.delete(
    "/{sku}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove um item do estoque",
)
@inject
async def delete_estoque_by_seller_and_sku_v2(
    sku: str,
    seller_id: str = Depends(get_required_seller_id),
    estoque_service: EstoqueServices = Depends(Provide[Container.estoque_service]),
):
    """
    Remove um item de estoque do sistema.

    Deleta permanentemente um item de estoque, identificado pelo seu SKU e
    pelo `seller_id` do usuário autenticado.

    Args:
        sku (str): O SKU do item de estoque a ser deletado.
        seller_id (str): O ID do vendedor, extraído do token JWT.
        estoque_service (EstoqueServices): Injeção de dependência do serviço de estoque.

    Returns:
        None: Retorna uma resposta vazia com status 204 em caso de sucesso.

    Raises:
        HTTPException (404 Not Found): Se o item de estoque não for encontrado.
    """
    logger.info(f"Deletando estoque para seller_id={seller_id}, sku={sku}")
    result = await estoque_service.delete(seller_id, sku)
    if not result:
        raise HTTPException(status_code=404, detail="Estoque não encontrado")
    logger.info(f"Estoque deletado para seller_id={seller_id}, sku={sku}")
    return None
