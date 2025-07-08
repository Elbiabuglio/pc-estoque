from unittest.mock import MagicMock

import pytest

from app.common.context import factory


@pytest.fixture
def mock_context():
    """
    Fixture que retorna um MagicMock para simular o contexto da aplicação.
    """
    return MagicMock()


def test_set_and_get_context(mock_context):
    """
    Testa se o contexto pode ser setado e recuperado corretamente.
    """
    factory.set_context(mock_context)
    assert factory.get_context() is mock_context

def test_get_context_raises_forbidden(monkeypatch):
    """
    Testa se ao tentar obter o contexto quando ele não está setado,
    a exceção ForbiddenException é levantada.
    """
    # Garante que o contexto está None
    monkeypatch.setattr(factory, "_app_context", factory.ContextVar("_app_context", default=None))
    with pytest.raises(factory.ForbiddenException):
        factory.get_context()