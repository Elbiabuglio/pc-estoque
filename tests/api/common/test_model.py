import pytest
from app.common.context.model import AppContext, AppContextScope


@pytest.fixture
def context_data():
    """Fornece dados de contexto padrão para os testes."""
    return {
        "tenant": "tenant1",
        "azp": "azp1",
        "sub": "sub1",
        "trace_id": "trace123",
        "scope": AppContextScope.SELLER,
    }

def test_app_context_fields(context_data):
    """Verifica se os campos do AppContext são atribuídos corretamente."""
    ctx = AppContext(**context_data)
    assert ctx.tenant == "tenant1"
    assert ctx.azp == "azp1"
    assert ctx.sub == "sub1"
    assert ctx.trace_id == "trace123"
    assert ctx.scope == AppContextScope.SELLER

def test_app_context_scope_enum():
    """Valida os valores do enum AppContextScope."""
    assert AppContextScope.CHANNEL == "channel"
    assert AppContextScope.SELLER == "seller"

def test_app_context_optional_fields():
    """Testa que os campos opcionais do AppContext podem ser None."""
    ctx = AppContext()
    assert ctx.tenant is None
    assert ctx.azp is None
    assert ctx.sub is None
    assert ctx.trace_id is None
    assert ctx.scope is None