from fastapi import APIRouter

from app.api.v1 import router_estoque

routes = APIRouter()

routes.include_router(router_estoque)
