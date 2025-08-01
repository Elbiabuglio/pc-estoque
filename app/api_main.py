import os

import dotenv
from fastapi import FastAPI, Request
from pclogging import LoggingBuilder

from app.container import Container
from app.settings import api_settings

ENV = os.getenv("ENV", "production")
is_dev = ENV == "dev"

dotenv.load_dotenv(override=is_dev)


# Inicia a biblioteca de logging
LoggingBuilder.init()

def init() -> FastAPI:
    from app.api.api_application import create_app
    from app.api.router import routes as api_routes

    container = Container()

    container.config.from_pydantic(api_settings)

    app_api = create_app(api_settings, api_routes)

    @app_api.middleware("http")
    async def log_auth_header(request: Request, call_next):
        auth_header = request.headers.get("authorization")
        response = await call_next(request)
        return response

    app_api.container = container  # type: ignore[attr-defined]

    # Autowiring
    container.wire(modules=["app.api.common.routers.health_check_routers"])
    container.wire(modules=["app.api.v2.routers.estoque_router"])
    container.wire(modules=["app.api.v2.routers.historico_estoque_router"])


    # Outros middlewares podem ser adicionados aqui se necessário

    return app_api


app = init()
