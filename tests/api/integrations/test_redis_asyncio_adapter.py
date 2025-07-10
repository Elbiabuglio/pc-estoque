import pytest
import json
from unittest.mock import AsyncMock, MagicMock, patch

from app.integrations.kv_db.redis_asyncio_adapter import RedisAsyncioAdapter

@pytest.fixture
def redis_client_mock():
    """Cria um mock completo do cliente Redis para ser injetado no adaptador."""
    return AsyncMock()

@pytest.fixture
@patch('app.integrations.kv_db.redis_asyncio_adapter.Redis.from_url')
def adapter(from_url_mock, redis_client_mock):
    """
    Cria uma instância do nosso RedisAsyncioAdapter, substituindo o cliente
    real por um mock logo após a sua criação.
    """
    from_url_mock.return_value = redis_client_mock
    
    adapter_instance = RedisAsyncioAdapter("redis://fake-host:6379")
    return adapter_instance


class TestRedisAsyncioAdapter:

    @patch('app.integrations.kv_db.redis_asyncio_adapter.Redis.from_url')
    def test_init_conecta_na_instanciacao(self, from_url_mock):
        """
        Cenário: Garante que o cliente Redis é instanciado com a URL correta
                 quando a classe é criada.
        """
        redis_url = "redis://testhost:1234"
        _ = RedisAsyncioAdapter(redis_url) 
        from_url_mock.assert_called_once_with(redis_url)

    @pytest.mark.asyncio
    async def test_aclose_chama_aclose_do_cliente(self, adapter, redis_client_mock):
        """
        Cenário: Testa se o método `aclose` do adaptador chama o `aclose` do cliente Redis.
        """
        await adapter.aclose()
        redis_client_mock.aclose.assert_awaited_once()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("redis_return, expected_result", [(1, True), (2, True), (0, False)])
    async def test_exists_retorna_booleano_correto(self, adapter, redis_client_mock, redis_return, expected_result):
        """
        Cenário: Testa se o método `exists` retorna True se o cliente Redis retornar > 0, e False caso contrário.
        """
        redis_client_mock.exists.return_value = redis_return
        result = await adapter.exists("some-key")
        assert result is expected_result
        redis_client_mock.exists.assert_awaited_once_with("some-key")

    @pytest.mark.asyncio
    async def test_get_str_retorna_string_decodificada(self, adapter, redis_client_mock):
        """
        Cenário: Busca uma chave que existe e cujo valor é bytes.
        Resultado: O valor é retornado como uma string decodificada.
        """
        redis_client_mock.get.return_value = b'{"value": "test"}'
        result = await adapter.get_str("my-key")
        assert result == '{"value": "test"}'
        redis_client_mock.get.assert_awaited_once_with("my-key")

    @pytest.mark.asyncio
    async def test_get_str_retorna_none_se_chave_nao_existe(self, adapter, redis_client_mock):
        """
        Cenário: Busca uma chave que não existe.
        Resultado: Retorna None.
        """
        redis_client_mock.get.return_value = None
        result = await adapter.get_str("non-existent-key")
        assert result is None

    @pytest.mark.asyncio
    async def test_set_str_chama_set_do_cliente(self, adapter, redis_client_mock):
        """
        Cenário: Salva um valor string com expiração.
        Resultado: O método `set` do cliente é chamado com os argumentos corretos.
        """
        await adapter.set_str("my-key", "my-value", expires_in_seconds=3600)
        redis_client_mock.set.assert_awaited_once_with("my-key", "my-value", 3600)

    @pytest.mark.asyncio
    async def test_set_str_converte_nao_string_para_string(self, adapter, redis_client_mock):
        """
        Cenário: Tenta salvar um valor que não é string (ex: um número).
        Resultado: O valor é convertido para string antes de ser salvo.
        """
        await adapter.set_str("my-key", 12345)
        redis_client_mock.set.assert_awaited_once_with("my-key", "12345", None)

    @pytest.mark.asyncio
    async def test_set_str_chama_delete_se_valor_for_none(self, adapter, redis_client_mock):
        """
        Cenário: Tenta salvar um valor `None`.
        Resultado: O método `delete` é chamado em vez de `set`.
        """
        await adapter.set_str("my-key", None)
        redis_client_mock.delete.assert_awaited_once_with("my-key")
        redis_client_mock.set.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_chama_delete_do_cliente_com_uma_chave(self, adapter, redis_client_mock):
        """
        Cenário: Deleta uma chave.
        Resultado: O método `delete` do cliente é chamado com a chave correta.
        """
        await adapter.delete("key-to-delete")
        redis_client_mock.delete.assert_awaited_once_with("key-to-delete")

    @pytest.mark.asyncio
    @patch('app.integrations.kv_db.redis_asyncio_adapter.RedisAsyncioAdapter.get_str')
    async def test_get_json_desserializa_string(self, get_str_mock, adapter):
        """
        Cenário: Busca um valor JSON.
        Resultado: O método `get_str` é chamado e seu resultado é desserializado com `json.loads`.
        """
        get_str_mock.return_value = '{"id": 1, "name": "test"}'
        result = await adapter.get_json("my-key")
        assert result == {"id": 1, "name": "test"}
        get_str_mock.assert_awaited_once_with("my-key")

    @pytest.mark.asyncio
    @patch('app.integrations.kv_db.redis_asyncio_adapter.RedisAsyncioAdapter.set_str')
    async def test_set_json_serializa_e_chama_set_str(self, set_str_mock, adapter):
        """
        Cenário: Salva um dicionário como JSON.
        Resultado: O dicionário é serializado com `json.dumps` e passado para o método `set_str`.
        """
        data = {"id": 1, "name": "test"}
        await adapter.set_json("my-key", data, expires_in_seconds=60)
        expected_json_string = json.dumps(data)
        set_str_mock.assert_awaited_once_with("my-key", expected_json_string, 60)