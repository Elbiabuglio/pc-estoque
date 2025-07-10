from pclogging import LoggingBuilder

from app.services.estoque_service import EstoqueServices

logger = LoggingBuilder.get_logger(__name__)


async def run_low_stock_check_task(estoque_service: EstoqueServices):
    """
    Tarefa que busca todos os itens com estoque baixo no banco de dados e dispara
    notificações para cada um deles.
    """
    logger.info("Executando a tarefa de verificação de estoque baixo.")
    await estoque_service.check_and_notify_all_low_stock()