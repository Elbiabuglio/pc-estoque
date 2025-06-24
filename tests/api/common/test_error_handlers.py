import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from app.api.common import error_handlers
from app.api.common.schemas.response import get_error_response
from app.common.error_codes import ErrorCodes
import pytest
from fastapi import Request
from unittest.mock import AsyncMock


@pytest.fixture
def valid_json_request():
    """Fixture para request simulada com JSON válido."""
    mock_request = AsyncMock(spec=Request)
    mock_request.method = "POST"
    mock_request.url = "http://testserver/test"
    mock_request.query_params = {"q": "yes"}
    mock_request.body.return_value = b'{"key": "value"}'
    return mock_request


@pytest.fixture
def invalid_json_request():
    """Fixture para request simulada com JSON inválido (malformado)."""
    mock_request = AsyncMock(spec=Request)
    mock_request.method = "PUT"
    mock_request.url = "http://testserver/test"
    mock_request.query_params = {}
    mock_request.body.return_value = b'{"key": "value"'  # malformado
    return mock_request

@pytest.mark.asyncio
async def test__get_request_body_success(valid_json_request):
    """Deve extrair o corpo JSON corretamente."""
    result = await error_handlers._get_request_body(valid_json_request)
    assert result == {"key": "value"}


@pytest.mark.asyncio
async def test__get_request_body_invalid_json(invalid_json_request, monkeypatch):
    """Deve retornar None e capturar erro de JSON inválido."""
    printed = []

    def fake_print(msg, ex):
        printed.append((msg.strip(), str(ex)))

    monkeypatch.setattr("builtins.print", fake_print)

    result = await error_handlers._get_request_body(invalid_json_request)
    assert result is None
    assert printed
    assert printed[0][0].startswith(":-(")


@pytest.mark.asyncio
async def test__get_request_info(valid_json_request):
    """Deve extrair informações completas do request simulado."""
    result = await error_handlers._get_request_info(valid_json_request)
    assert result["method"] == "POST"
    assert str(result["url"]) == "http://testserver/test"
    assert dict(result["query"]) == {"q": "yes"}
    assert result["content"] == {"key": "value"}


def test_http_exception_handler():
    """Deve capturar HTTPException e retornar o error response padrão."""
    app = FastAPI()

    @app.get("/error")
    async def throw_error():
        raise HTTPException(status_code=404, detail="Página não encontrada")

    error_handlers.add_error_handlers(app)
    client = TestClient(app)

    expected = get_error_response(ErrorCodes.SERVER_ERROR.value).model_dump(
        mode="json", exclude_none=True, exclude_unset=True
    )

    response = client.get("/error")
    assert response.status_code == 404
    assert response.json() == expected


def test_request_validation_exception_handler():
    """Deve validar erro de payload inválido e formatar resposta padrão."""
    app = FastAPI()

    class Item(BaseModel):
        name: str = Field(..., min_length=3)
        quantity: int

    @app.post("/items")
    async def create_item(item: Item):
        return item

    error_handlers.add_error_handlers(app)
    client = TestClient(app)

    response = client.post("/items", json={"name": "ab", "quantity": 10})

    assert response.status_code == 422
    body = response.json()
    assert "message" in body
    assert "slug" in body
    assert "details" in body
    assert isinstance(body["details"], list)
    assert body["details"][0]["field"] == "name"
    assert body["details"][0]["location"] == "body"
    assert "too_short" in body["details"][0]["slug"]


def test_pydantic_validation_exception_handler():
    """Deve capturar exceção Pydantic ValidationError manual."""
    app = FastAPI()

    class Item(BaseModel):
        name: str
        quantity: int

    @app.get("/validate")
    async def validate():
        Item(quantity="abc")

    error_handlers.add_error_handlers(app)
    client = TestClient(app)

    response = client.get("/validate")
    assert response.status_code == 422
    body = response.json()
    assert "message" in body
    assert "slug" in body
    assert "details" in body
    assert isinstance(body["details"], list)
    assert body["details"][0]["field"] == ""
    assert body["details"][0]["location"] == "body"


def test_default_exception_handler():
    """Deve capturar erro inesperado e retornar SERVER_ERROR."""
    app = FastAPI()

    @app.get("/error")
    async def error_route():
        raise Exception("Erro inesperado")

    error_handlers.add_error_handlers(app)
    client = TestClient(app, raise_server_exceptions=False)

    response = client.get("/error")
    assert response.status_code == ErrorCodes.SERVER_ERROR.http_code
    body = response.json()
    assert body["message"] == ErrorCodes.SERVER_ERROR.value.message
    assert "details" not in body or isinstance(body.get("details"), list)


class ApplicationException(Exception):
    def __init__(self, status_code: int, error_response):
        self.status_code = status_code
        self.error_response = error_response


def test_application_exception_handler():
    """Deve capturar ApplicationException customizada."""
    app = FastAPI()

    @app.get("/raise-app-exc")
    async def raise_app_exc():
        class ErrorResponseMock:
            def model_dump(self, **kwargs):
                return {"error": "app error"}
        raise ApplicationException(status_code=400, error_response=ErrorResponseMock())

    @app.exception_handler(ApplicationException)
    async def application_exception_handler(_, exc: ApplicationException):
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.error_response.model_dump(mode="json", exclude_none=True, exclude_unset=True),
        )

    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/raise-app-exc")

    assert response.status_code == 400
    assert response.json() == {"error": "app error"}