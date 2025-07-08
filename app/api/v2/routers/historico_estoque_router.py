from dependency_injector.wiring import Provide, inject
from pclogging import LoggingBuilder

from fastapi import APIRouter, Depends, status, HTTPException

from app.api.common.dependencies import get_required_seller_id
from app.api.common.schemas import ListResponse
from app.api.common.auth_handler import do_auth 
from app.api.v2.schemas.historico_estoque_schema import HistoricoEstoqueResponse
from app.services.historico_estoque_service import HistoricoEstoqueService
from app.container import Container

router = APIRouter(prefix="/historico_estoque", tags=["Histórico de Estoque"], dependencies=[Depends(do_auth)])

logger = LoggingBuilder.get_logger(__name__)

@router.get(
    "/semana",
    response_model=ListResponse[HistoricoEstoqueResponse],
    status_code=status.HTTP_200_OK,
)
@inject
async def list_historico_estoque_semana_v2(
    seller_id: str = Depends(get_required_seller_id),
    historico_estoque_service: HistoricoEstoqueService = Depends(Provide[Container.historico_estoque_service]),
):
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
)
@inject
async def list_historico_estoque_dia_v2(
    seller_id: str = Depends(get_required_seller_id),
    historico_estoque_service: HistoricoEstoqueService = Depends(Provide[Container.historico_estoque_service]),
):
    logger.info(f"Gerando histórico de estoque do dia para seller_id={seller_id}")
    historico = await historico_estoque_service.get_relatorio_diario(seller_id)
    if not historico:
        logger.warning(f"Nenhum histórico encontrado para seller_id={seller_id} no dia de hoje")
        raise HTTPException(status_code=404, detail="Nenhum histórico encontrado")
    return ListResponse[HistoricoEstoqueResponse](results=historico, total=len(historico))