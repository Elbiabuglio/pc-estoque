from logging.config import fileConfig
import os
import dotenv
import asyncio

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context

# Carrega as variáveis de ambiente
ENV = os.getenv("ENV", "production")
is_dev = ENV == "dev"
dotenv.load_dotenv(override=is_dev)

# Configuração do Alembic
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Alvo de metadados para autogeração
from app.integrations.database.sqlalchemy_client import Base
target_metadata = Base.metadata

# Configura a URL a partir da variável de ambiente
if (app_db_url := os.getenv("APP_DB_URL")) is not None:
    print("URL DB carregada da memoria")
    print("APP_DB_URL:", app_db_url)
    config.set_main_option("sqlalchemy.url", app_db_url)

def run_migrations_offline() -> None:
    """Executa as migrações no modo offline (com URL estática)."""
    url = config.get_main_option("sqlalchemy.url")
    print("URL carregada (offline):", url)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Executa as migrações no modo online, usando um AsyncEngine."""
    # Cria um AsyncEngine usando a URL configurada
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # Executa as migrações de forma sincronizada no contexto assíncrono
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())