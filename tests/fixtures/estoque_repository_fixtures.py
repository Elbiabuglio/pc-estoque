"""
Fixtures e classes auxiliares para os testes do EstoqueRepository.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from app.repositories.estoque_repository import EstoqueRepository


@pytest.fixture
def mock_sql_client():
    """
    Cria e retorna um cliente SQL mockado com sessão assíncrona simulada.

    Retorna:
        MagicMock: Cliente SQL com sessão AsyncMock.
    """
    mock_client = MagicMock()
    mock_client.session = AsyncMock()
    return mock_client


@pytest.fixture
def estoque_repository(mock_sql_client):
    """
    Instancia o EstoqueRepository usando o cliente SQL mockado.

    Retorna:
        EstoqueRepository: Repositório com cliente SQL simulado.
    """
    return EstoqueRepository(sql_client=mock_sql_client)