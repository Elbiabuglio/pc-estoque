"""
Testes para as funções utilitárias de hash em hash_utils.
"""

import hashlib
from unittest.mock import MagicMock

import pytest

from app.common.hash_utils import generate_hash

"""
Fixtures e utilitários auxiliares para os testes de hash_utils.
"""
@pytest.fixture
def mock_hash(monkeypatch):
    """
    Cria e aplica um mock para a função hashlib.sha256.

    Simula o retorno do método hexdigest com valor pré-definido.
    Retorna:
        tuple: (mock_sha256, mock_hasher)
    """
    mock_hasher = MagicMock()
    mock_hasher.hexdigest.return_value = "valor_falso"
    mock_sha256 = MagicMock(return_value=mock_hasher)

    monkeypatch.setattr(hashlib, "sha256", mock_sha256)

    return mock_sha256, mock_hasher
def test_generate_hash(mock_hash):
    """
    Testa a função generate_hash para garantir que:
    - A função hashlib.sha256 é chamada com os bytes esperados.
    - O método hexdigest é chamado uma vez.
    - O valor retornado pelo hexdigest é corretamente devolvido pela função.

    Cenário:
    - Dado um dado de entrada em string.
    - Quando a função for chamada.
    - Então deve retornar o valor falso simulado no mock.
    """
    mock_sha256, mock_hasher = mock_hash

    result = generate_hash("algum_dado")

    mock_sha256.assert_called_once_with(b"algum_dado")
    mock_hasher.hexdigest.assert_called_once()
    assert result == "valor_falso"
    
    

