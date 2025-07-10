import os

import dotenv
from pydantic import Field, HttpUrl, PostgresDsn, RedisDsn

from .base import BaseSettings

ENV = os.getenv("ENV", "production")
is_dev = ENV == "dev"

dotenv.load_dotenv(override=is_dev)

class AppSettings(BaseSettings):
    version: str = Field(default="0.5.0", title="Versão da aplicação")

    app_name: str = Field(default="PC Estoque", title="Nome da aplicação")

    memory_min: int = Field(default=64, title="Limite mínimo de memória disponível em MB")
    disk_usage_max: int = Field(default=80, title="Limite máximo de 80% de uso de disco")

    low_stock_threshold: int = Field(default=15, title="Limite para notificação de estoque baixo")

    app_db_url: PostgresDsn = Field(..., title="URI para o banco Postgresql")

    app_openid_wellknown: HttpUrl = Field(..., title="URL well-known do Keycloak")

    pc_logging_level: str = Field("DEBUG", description="Nível do logging")
    pc_logging_env: str = Field("prod", description="Ambiente do logging (prod ou dev ou test)")
    
    app_redis_url: RedisDsn = Field(..., title="URL para o Redis")

settings = AppSettings()



