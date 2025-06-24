from unittest.mock import patch, MagicMock
import pytest

from app.api.v2.schemas.estoque_schema import (
    EstoqueSchema,
    EstoqueCreateV2,
    EstoqueUpdateV2,
)

@pytest.fixture
def estoque_data():
    """
    Fixture que retorna um dicionário com dados válidos para Estoque.
    """
    return {"sku": "ABC123", "quantidade": 10}


def test_estoque_schema_fields(estoque_data):
    """
    Testa se o EstoqueSchema inicializa corretamente com dados válidos.
    """
    schema = EstoqueSchema(**estoque_data)
    assert schema.sku == "ABC123"
    assert schema.quantidade == 10

def test_estoque_create_v2_to_model(estoque_data):
    """
    Testa o método to_model de EstoqueCreateV2,
    garantindo que instancia o modelo Estoque com os dados.
    """
    with patch("app.api.v2.schemas.estoque_schema.Estoque") as MockEstoque:
        mock_instance = MagicMock()
        MockEstoque.return_value = mock_instance
        schema = EstoqueCreateV2(**estoque_data)
        model = schema.to_model()
        MockEstoque.assert_called_once_with(**estoque_data)
        assert model == mock_instance

def test_estoque_update_v2_fields():
    """
    Testa se EstoqueUpdateV2 inicializa corretamente com o campo quantidade.
    """
    schema = EstoqueUpdateV2(quantidade=5)
    assert schema.quantidade == 5

def test_estoque_schema_invalid_quantidade():
    """
    Testa se o EstoqueSchema levanta ValueError para quantidade negativa.
    """
    with pytest.raises(ValueError):
        EstoqueSchema(sku="ABC123", quantidade=-1)

def test_estoque_schema_invalid_sku():
    """
    Testa se o EstoqueSchema levanta ValueError para sku vazio.
    """
    with pytest.raises(ValueError):
        EstoqueSchema(sku="", quantidade=1)