import pytest
from unittest.mock import AsyncMock
from app.api.common.auth_handler import do_auth
from app.integrations.auth.keycloak_adapter import OAuthException
from app.common.exceptions import UnauthorizedException, ForbiddenException

@pytest.mark.asyncio
async def test_do_auth_sucesso():
    token = "fake-token"
    seller_id = "123"
    
    # Simula adapter retornando token válido com seller_id
    fake_adapter = AsyncMock()
    fake_adapter.validate_token.return_value = {"sellers": "123,456"}
    
    await do_auth(token=token, seller_id=seller_id, openid_adapter=fake_adapter)

@pytest.mark.asyncio
async def test_do_auth_token_invalido():
    token = "invalid-token"
    seller_id = "123"
    
    fake_adapter = AsyncMock()
    fake_adapter.validate_token.side_effect = OAuthException("token inválido")

    with pytest.raises(UnauthorizedException):
        await do_auth(token=token, seller_id=seller_id, openid_adapter=fake_adapter)

@pytest.mark.asyncio
async def test_do_auth_seller_nao_autorizado():
    token = "fake-token"
    seller_id = "999"  # não está na lista
    
    fake_adapter = AsyncMock()
    fake_adapter.validate_token.return_value = {"sellers": "123,456"}
    
    with pytest.raises(ForbiddenException):
        await do_auth(token=token, seller_id=seller_id, openid_adapter=fake_adapter)
