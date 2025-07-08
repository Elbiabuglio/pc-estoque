from fastapi import APIRouter

from app.api.v2.routers.estoque_router import router as estoque_router_v2
from app.api.v2.routers.historico_estoque_router import router as historico_router_v2 
from app.settings import api_settings

router_estoque_v2 = APIRouter(prefix="/seller/v2")

def load_routes(router_estoque: APIRouter):
    if api_settings.enable_estoque_resources:
        router_estoque.include_router(estoque_router_v2)
        router_estoque.include_router(historico_router_v2)

load_routes(router_estoque_v2)