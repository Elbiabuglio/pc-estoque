from fastapi import APIRouter

from app.api.v2 import router_estoque_v2

routes = APIRouter()


routes.include_router(router_estoque_v2)
