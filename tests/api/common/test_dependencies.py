import pytest
from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

from app.api.common.dependencies import get_required_seller_id
from app.common.exceptions import BadRequestException

app = FastAPI()

@app.exception_handler(BadRequestException)
async def bad_request_exception_handler(request: Request, exc: BadRequestException):
    return JSONResponse(
        status_code=400,
        content={
            "detail": [
                            detail.model_dump() if hasattr(detail, "model_dump") else detail
                            for detail in (exc.details or [])
                        ]
        },
    )

@app.get("/teste")
async def rota_teste(seller_id: str = Depends(get_required_seller_id)):
    return {"seller_id": seller_id}

client = TestClient(app)

def test_get_required_seller_id_sucesso():
    response = client.get("/teste", headers={"x-seller-id": "abc123"})
    assert response.status_code == 200
    assert response.json() == {"seller_id": "abc123"}

def test_get_required_seller_id_erro():
    response = client.get("/teste")  # sem o header
    assert response.status_code == 400
    assert response.json()["detail"][0]["slug"] == "missing_required_header"
