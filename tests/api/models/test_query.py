import pytest
from app.models.query import QueryModel

class EstoqueQuery(QueryModel):
    seller_id: str | None = None
    sku: str | None = None
    quantidade__ge: int | None = None

@pytest.fixture
def filtro_produtos():
    """Retorna filtro preenchido para consultas no estoque."""
    return EstoqueQuery(
        seller_id="abc123",
        sku="SKU-456",
        quantidade__ge=50
    )

@pytest.fixture
def filtro_vazio():
    """Retorna um filtro vazio."""
    return EstoqueQuery()

def test_filtro_produtos_query_dict(filtro_produtos):
    """Deve montar corretamente o dicionário de filtros para consulta de estoque."""
    resultado = filtro_produtos.to_query_dict()
    assert resultado == {
        "seller_id": "abc123",
        "sku": "SKU-456",
        "quantidade": {"$gte": 50}
    }

def test_filtro_vazio(filtro_vazio):
    """Deve retornar um dicionário vazio se nenhum filtro for informado."""
    assert filtro_vazio.to_query_dict() == {}