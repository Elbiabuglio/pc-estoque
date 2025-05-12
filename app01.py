from fastapi import FastAPI
from pydantic import BaseModel, Field
from app.api.v1 import estoque_api  # <-- importa o estoque_routes
from fastapi import APIRouter
from app.api.v1.estoque_api import estoque_routes
from pathlib import Path
import json

app = FastAPI(title="API01", version="0.0.1")

VERSAO_API = "0.0.2"


class RootResponse(BaseModel):
    versao: str = Field(
        VERSAO_API,
        description="Versão da API"
    )


@app.get("/")
async def get_root():
    return {"message": "Bem vindo ao PC-Estoque"}


@app.get("/api/health")
async def get_version() -> RootResponse:
    return RootResponse(versao=VERSAO_API)

# Caminho para o arquivo JSON
DATA_PATH = Path("app/data/estoque.json")

# Inclui as rotas de estoque
app.include_router(estoque_api.estoque_routes)