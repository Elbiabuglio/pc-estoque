import pytest
from unittest.mock import AsyncMock

from app.services.estoque_service import EstoqueServices
from app.models.estoque_model import Estoque


@pytest.fixture
def mock_repository():
    """
    Retorna um repositório mockado com métodos assíncronos simulados.
    
    Usado para substituir chamadas reais ao banco de dados durante os testes.
    """
    return AsyncMock()


@pytest.fixture
def service(mock_repository):
    """
    Instancia o serviço de EstoqueServices com o repositório simulado.

    Permite testar a lógica do serviço sem dependência externa.
    """
    return EstoqueServices(mock_repository)


@pytest.fixture
def estoque_exemplo():
    """
    Retorna uma instância exemplo de um estoque válido.

    Útil para evitar duplicação de dados comuns em múltiplos testes.
    """
    return Estoque(id=1, seller_id="vendedor1", sku="sku1", quantidade=10)


class FakePaginator:
    """
    Classe auxiliar que simula um paginador simples para testes.

    Permite testar funções que esperam objetos com atributos limit e offset.
    """
    def __init__(self, limit, offset):
        self.limit = limit
        self.offset = offset