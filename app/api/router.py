from fastapi import APIRouter
from pydantic import BaseModel, Field

routes = APIRouter()

# XXX Adcionar rotas....

VERSAO_API ="0.0.1"

class RootResponse(BaseModel):
    """
    Modelo de resposta para o endpoint raiz.
    """
    versao: str = Field(
        VERSAO_API,
        description="Versão da API"
        )

@routes.get("/")
async def get_root():
    return {"message": "Bem vindo ao PC-Estoque"}

@routes.get("/api/health")
async def get_version()-> RootResponse:
    return RootResponse(versao=VERSAO_API)