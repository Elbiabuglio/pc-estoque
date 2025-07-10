import pytest
from app.common.exceptions.estoque_exceptions import EstoqueNotFoundException, EstoqueBadRequestException

def test_estoque_not_found_exception_default():
    exc = EstoqueNotFoundException("seller1", "sku1")
    assert isinstance(exc, EstoqueNotFoundException)
    assert "seller1" in str(exc)
    assert "sku1" in str(exc)

def test_estoque_bad_request_exception_default():
    exc = EstoqueBadRequestException("mensagem de erro", field="sku", value="abc")
    assert isinstance(exc, EstoqueBadRequestException)
    assert "mensagem de erro" in str(exc)
    assert "sku" in str(exc) or "abc" in str(exc)