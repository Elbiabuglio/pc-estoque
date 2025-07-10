# app/worker/main.py

import asyncio
import os

from pclogging import LoggingBuilder

from dotenv import load_dotenv
load_dotenv(override=True)

os.environ.setdefault("ENV", "dev")

from app.container import Container
from .tasks import run_low_stock_check_task

LoggingBuilder.init(log_level="DEBUG")
logger = LoggingBuilder.get_logger(__name__)


async def worker_loop():
    """
    Função principal do worker.
    Configura o container de dependências e executa a tarefa em um loop.
    """
    logger.info("Iniciando o loop do Worker de Estoque...")
    
    container = Container()
    container.config.from_yaml("config.yml")
    
    container.config.app_db_url.from_env("APP_DB_URL")
    container.config.app_redis_url.from_env("APP_REDIS_URL")
    container.config.app_openid_wellknown.from_env("APP_OPENID_WELLKNOWN")
    
    estoque_service = container.estoque_service()
    
    check_interval_seconds = 60

    logger.info(f"O worker em background irá verificar o estoque a cada {check_interval_seconds} segundos.")

    while True:
        try:
            await run_low_stock_check_task(estoque_service)
        except Exception as e:
            logger.error(f"Erro inesperado no loop principal do worker: {e}", exc_info=True)
        
        logger.info(f"Worker aguardando {check_interval_seconds} segundos para a próxima execução.")
        await asyncio.sleep(check_interval_seconds)


if __name__ == "__main__":
    try:
        print("Executando o worker de forma independente para teste...")
        asyncio.run(worker_loop()) 
    except KeyboardInterrupt:
        logger.info("Worker independente interrompido pelo usuário.")