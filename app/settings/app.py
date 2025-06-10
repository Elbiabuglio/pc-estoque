from pydantic import Field, PostgresDsn
from dotenv import load_dotenv

from .base import BaseSettings

load_dotenv()

class AppSettings(BaseSettings):
    version: str = Field(default="0.2.1", title="Versão da aplicação")

    app_name: str = Field(default="PC Estoque", title="Nome da aplicação")

    memory_min: int = Field(default=64, title="Limite mínimo de memória disponível em MB")
    disk_usage_max: int = Field(default=80, title="Limite máximo de 80% de uso de disco")


settings = AppSettings()

app_db_url: PostgresDsn = Field(..., title="URI para o banco Postgresql")

