from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from pclogging import LoggingBuilder

from app.api.common.auth_handler import do_auth
from app.api.common.dependencies import get_required_seller_id
from app.api.common.schemas import ListResponse
from app.api.v2.schemas.historico_estoque_schema import HistoricoEstoqueResponse
from app.container import Container
from app.services.historico_estoque_service import HistoricoEstoqueService

router = APIRouter(prefix="/historico_estoque", tags=["Histórico de Estoque"], dependencies=[Depends(do_auth)])

logger = LoggingBuilder.get_logger(__name__)

@router.get(
    "/semana",
    response_model=ListResponse[HistoricoEstoqueResponse],
    status_code=status.HTTP_200_OK,
    summary="Lista o histórico do estoque da última semana",
)
@inject
async def list_historico_estoque_semana_v2(
    seller_id: str = Depends(get_required_seller_id),
    historico_estoque_service: HistoricoEstoqueService = Depends(Provide[Container.historico_estoque_service]),
):
    """
    Recupera o relatório de movimentações de estoque da última semana.

    Este endpoint retorna uma lista de todas as movimentações de estoque
    (entradas, saídas, ajustes) registradas nos últimos 7 dias para o `seller_id` informado.

    Args:
        seller_id (str): O ID do vendedor, extraído automaticamente do
                         cabeçalho da requisição.

    Returns:
        ListResponse[HistoricoEstoqueResponse]: Um objeto de resposta contendo a
                                                lista de movimentações de estoque
                                                e o total de registros.

    Raises:
        HTTPException (404 Not Found): Se nenhum registro de histórico for
                                       encontrado para o vendedor no período.
    """ 
    logger.info(f"Gerando histórico de estoque da semana para seller_id={seller_id}")
    historico = await historico_estoque_service.get_relatorio_semanal(seller_id)
    if not historico:
        logger.warning(f"Nenhum histórico encontrado para seller_id={seller_id} na última semana")
        raise HTTPException(status_code=404, detail="Nenhum histórico encontrado")
    return ListResponse[HistoricoEstoqueResponse](results=historico, total=len(historico))

@router.get(
    "/dia",
    response_model=ListResponse[HistoricoEstoqueResponse],
    status_code=status.HTTP_200_OK,
    summary="Lista o histórico do estoque do dia corrente",
)
@inject
async def list_historico_estoque_dia_v2(
    seller_id: str = Depends(get_required_seller_id),
    historico_estoque_service: HistoricoEstoqueService = Depends(Provide[Container.historico_estoque_service]),
):
    """
    Recupera o relatório de movimentações de estoque do dia corrente.

    Este endpoint retorna uma lista de todas as movimentações de estoque
    (entradas, saídas, ajustes) registradas para o `seller_id` informado 
    desde a meia-noite (00:00) do dia atual.

    Args:
        seller_id (str): O ID do vendedor, extraído automaticamente do
                         cabeçalho da requisição.

    Returns:
        ListResponse[HistoricoEstoqueResponse]: Um objeto de resposta contendo a
                                                lista de movimentações de estoque
                                                e o total de registros.

    Raises:
        HTTPException (404 Not Found): Se nenhum registro de histórico for
                                       encontrado para o vendedor no dia.
    """
    logger.info(f"Gerando histórico de estoque do dia para seller_id={seller_id}")
    historico = await historico_estoque_service.get_relatorio_diario(seller_id)
    if not historico:
        logger.warning(f"Nenhum histórico encontrado para seller_id={seller_id} no dia de hoje")
        raise HTTPException(status_code=404, detail="Nenhum histórico encontrado")
    return ListResponse[HistoricoEstoqueResponse](results=historico, total=len(historico))