import json
import traceback

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from pclogging import LoggingBuilder
from pydantic_core import ValidationError

from app.common.error_codes import ErrorCodes, ErrorInfo
from app.common.exceptions import ApplicationException

from .schemas.response import ErrorDetail, get_error_response

logger = LoggingBuilder.get_logger(__name__)

async def _get_request_body(request: Request) -> dict | None:
    try:
        return json.loads(await request.body())
    except Exception as ex:
        logger.error("Failed to parse request body", exc_info=ex)
        # XXX Informar que deu erro
        print(":-( ", ex)
    return None


async def _get_request_info(request: Request) -> dict:
    info = {
        "method": request.method,
        "url": str(request.url),
        "query": dict(request.query_params),
        "content": await _get_request_body(request),
    }
    logger.debug(f"Request info: {info}")
    return info


def add_error_handlers(app: FastAPI):
    @app.exception_handler(HTTPException)
    async def http_exception_handler(_, exc: HTTPException):
        logger.warning(f"HTTPException: {exc.detail} (status_code={exc.status_code})")
        response = get_error_response(ErrorCodes.SERVER_ERROR.value)
        return JSONResponse(
            status_code=exc.status_code,
            headers=exc.headers,
            content=response.model_dump(mode="json", exclude_none=True, exclude_unset=True),
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        logger.info(f"RequestValidationError: {exc.errors()}")
        errors = exc.errors()
        details: list[ErrorDetail] = []
        for error in errors:
            ctx = error.get("ctx", {})

            details.append(
                ErrorDetail(
                    **{
                        "message": error["msg"],
                        "location": "body",
                        "slug": error["type"],
                        "field": ", ".join(map(str, error["loc"][1:])),
                        "ctx": ctx,
                    }
                )
            )

        response = get_error_response(ErrorCodes.UNPROCESSABLE_ENTITY.value, details=details)

        return JSONResponse(
            status_code=ErrorCodes.UNPROCESSABLE_ENTITY.http_code,
            content=response.model_dump(mode="json", exclude_none=True, exclude_unset=True),
        )

    @app.exception_handler(ValidationError)
    async def request_pydantic_validation_error_handler(_: Request, exc: ValidationError) -> JSONResponse:
        logger.info(f"Pydantic ValidationError: {exc.errors()}")
        errors = exc.errors()
        details: list[ErrorDetail] = []
        for error in errors:
            ctx = error.get("ctx", {})

            if isinstance(ctx.get("error", {}), ValueError):  # pragma: no cover
                ctx["error"] = str(ctx["error"])

            details.append(
                ErrorDetail(
                    **{
                        "message": error["msg"],
                        "location": "body",
                        "slug": error["type"],
                        "field": ", ".join(map(str, error["loc"][1:])) if error["loc"] else "",
                        "ctx": ctx,
                    }
                )
            )

        response = get_error_response(ErrorCodes.UNPROCESSABLE_ENTITY.value, details=details)

        return JSONResponse(
            status_code=ErrorCodes.UNPROCESSABLE_ENTITY.http_code,
            content=response.model_dump(mode="json", exclude_none=True, exclude_unset=True),
        )

    @app.exception_handler(Exception)
    async def default_validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.error(f"Unhandled Exception: {exc}", exc_info=exc)
        response = get_error_response(ErrorCodes.SERVER_ERROR.value)
        return JSONResponse(
            status_code=ErrorCodes.SERVER_ERROR.http_code,
            content=response.model_dump(mode="json", exclude_none=True, exclude_unset=True),
        )

    @app.exception_handler(ApplicationException)
    async def application_exception_handler(_, exc: ApplicationException):
        logger.warning(f"ApplicationException: {exc.error_response}")
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.error_response.model_dump(mode="json", exclude_none=True, exclude_unset=True),
        )
