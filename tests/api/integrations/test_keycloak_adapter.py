import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from app.integrations.auth.keycloak_adapter import KeycloakAdapter, InvalidTokenException

@pytest.fixture
def adapter():
    """
    Fixture para criar uma instância do KeycloakAdapter
    com uma URL fake para uso nos testes.
    """
    return KeycloakAdapter("https://fake-url.com/.well-known/openid-configuration")

def test_get_authorization_endpoint(adapter):
    """
    Testa se o método get_authorization_endpoint retorna o endpoint correto.
    Mocka o atributo _well_known para simular a resposta esperada.
    """
    adapter._well_known = {
        "authorization_endpoint": "https://example.com/auth"
    }
    result = adapter.get_authorization_endpoint()
    assert result == "https://example.com/auth"

@pytest.mark.asyncio
async def test_get_public_keys_success(adapter):
    """
    Testa se o método get_public_keys obtém corretamente as chaves públicas.
    Mocka a resposta HTTP do httpx.AsyncClient.get para simular o retorno esperado.
    """
    adapter._well_known = {"jwks_uri": "https://example.com/jwks"}

    mock_response = AsyncMock()
    # .json() é um método síncrono aqui, retornando dicionário com chaves
    mock_response.json = MagicMock(return_value={"keys": [{"kid": "abc123", "kty": "RSA"}]})
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.AsyncClient.get", return_value=mock_response) as mock_get:
        keys = await adapter.get_public_keys()
        assert keys == [{"kid": "abc123", "kty": "RSA"}]
        mock_get.assert_called_once_with("https://example.com/jwks")

@pytest.mark.asyncio
async def test_get_public_keys_http_error(adapter):
    """
    Testa se o método get_public_keys lança exceção corretamente
    quando a resposta HTTP retorna erro.
    Mocka o método raise_for_status para lançar exceção simulada.
    """
    adapter._well_known = {"jwks_uri": "https://example.com/jwks"}

    mock_response = MagicMock()
    mock_response.json = MagicMock(return_value={"keys": [{"kid": "abc123"}]})
    mock_response.raise_for_status.side_effect = Exception("HTTP error")

    async def mock_get(*args, **kwargs):
        return mock_response

    with patch("httpx.AsyncClient.get", new=mock_get):
        with pytest.raises(Exception, match="HTTP error"):
            await adapter.get_public_keys()

@pytest.mark.asyncio
async def test_get_alg_key_for_kid_found(adapter):
    """
    Testa se o método get_alg_key_for_kid retorna a chave correta
    quando o 'kid' é encontrado na lista de chaves públicas.
    """
    adapter.get_public_keys = AsyncMock(return_value=[{"kid": "abc123", "alg": "RS256"}])
    key = await adapter.get_alg_key_for_kid("abc123")
    assert key["kid"] == "abc123"

@pytest.mark.asyncio
async def test_get_alg_key_for_kid_not_found(adapter):
    """
    Testa se o método get_alg_key_for_kid lança InvalidTokenException
    quando o 'kid' não é encontrado nas chaves públicas.
    """
    adapter.get_public_keys = AsyncMock(return_value=[{"kid": "xyz"}])
    with pytest.raises(InvalidTokenException):
        await adapter.get_alg_key_for_kid("abc123")