from dependency_injector import containers, providers

from app.integrations.auth.keycloak_adapter import KeycloakAdapter
from app.integrations.database.sqlalchemy_client import SQLAlchemyClient
from app.integrations.kv_db.redis_asyncio_adapter import RedisAsyncioAdapter
from app.repositories import EstoqueRepository
from app.repositories.historico_estoque_repository import HistoricoEstoqueRepository
from app.services import EstoqueServices, HealthCheckService
from app.services.historico_estoque_service import HistoricoEstoqueService
from app.settings import AppSettings


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    settings = providers.Singleton(AppSettings)

    # Integrações
    sql_client = providers.Singleton(SQLAlchemyClient, config.app_db_url)

    # Keycloak Adapter
    keycloak_adapter = providers.Singleton(KeycloakAdapter, config.app_openid_wellknown)

    # Redis Adapter
    redis_adapter = providers.Singleton(RedisAsyncioAdapter, config.app_redis_url)

    # Repositórios
    estoque_repository = providers.Singleton(EstoqueRepository, sql_client=sql_client)
    historico_estoque_repository = providers.Singleton(HistoricoEstoqueRepository, sql_client=sql_client) 


    # Serviços
    health_check_service = providers.Singleton(
        HealthCheckService, checkers=config.health_check_checkers, settings=settings
    )
    estoque_service = providers.Singleton(
        EstoqueServices,
        repository=estoque_repository,
        redis_adapter=redis_adapter,
        historico_repository=historico_estoque_repository,
        settings=settings
    )
    historico_estoque_service = providers.Singleton(
        HistoricoEstoqueService,
        historico_repository=historico_estoque_repository
    )
