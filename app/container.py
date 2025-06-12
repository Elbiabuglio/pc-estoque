from dependency_injector import containers, providers

from app.repositories import EstoqueRepository
from app.services import HealthCheckService
from app.services.estoque.estoque_service import EstoqueServices
from app.settings import AppSettings

from app.integrations.database.sqlalchemy_client import SQLAlchemyClient


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    settings = providers.Singleton(AppSettings)

    # Integrações
    sql_client = providers.Singleton(SQLAlchemyClient, config.app_db_url)
    print("SQLAlchemyClient initialized with app_db_url:", config.app_db_url)

    # Repositórios
    estoque_repository = providers.Singleton(EstoqueRepository, sql_client=sql_client)

    # Serviços
    health_check_service = providers.Singleton(
        HealthCheckService, checkers=config.health_check_checkers, settings=settings
    )

    estoque_service = providers.Singleton(EstoqueServices, repository=estoque_repository)
