import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timedelta
from app.repositories.historico_estoque_repository import HistoricoEstoqueRepository, HistoricoEstoqueBase
from app.models.historico_estoque_model import HistoricoEstoque, TipoMovimentacaoEnum
from app.integrations.database.sqlalchemy_client import SQLAlchemyClient


@pytest.fixture
def session_mock():
    """
    Fixture que cria um mock de uma sessão assíncrona do SQLAlchemy.
    """
    mock = AsyncMock()
    transaction_mock = AsyncMock()
    mock.begin.return_value = transaction_mock
    
    return mock

@pytest.fixture
def fake_sql_client(session_mock):
    """
    Fixture que cria um mock do cliente SQLAlchemy. A única coisa que ele faz
    é fornecer o nosso `session_mock` quando o código chama `make_session()`.
    """
    client = MagicMock(spec=SQLAlchemyClient)
    
    session_manager = AsyncMock()
    session_manager.__aenter__.return_value = session_mock
    
    client.make_session.return_value = session_manager
    return client

@pytest.fixture
def repository(fake_sql_client):
    """Fixture que cria uma instância real do repositório em teste,
    injetando nossa dependência falsa (o fake_sql_client)."""
    return HistoricoEstoqueRepository(sql_client=fake_sql_client)

@pytest.fixture
def sample_datetime():
    """Fixture que fornece uma data e hora padrão para os testes."""
    return datetime(2025, 7, 8, 12, 0, 0)

@pytest.fixture
def historico_pydantic_model(sample_datetime):
    """Fixture que cria um objeto do modelo Pydantic (entrada para `create`)."""
    return HistoricoEstoque(
        id=1,
        seller_id="seller-123",
        sku="SKU-ABC-001",
        quantidade_anterior=50,
        quantidade_nova=60,
        tipo_movimentacao=TipoMovimentacaoEnum.ATUALIZACAO,
        movimentado_em=sample_datetime
    )

@pytest.fixture
def historico_sqlalchemy_base(sample_datetime):
    """Fixture que cria um objeto da entidade SQLAlchemy (simula retorno do DB)."""
    base = HistoricoEstoqueBase()
    base.id = 1
    base.seller_id = "seller-123"
    base.sku = "SKU-ABC-001"
    base.quantidade_anterior = 50
    base.quantidade_nova = 60
    base.tipo_movimentacao = "ATUALIZACAO"
    base.movimentado_em = sample_datetime
    return base

class TestHistoricoEstoqueRepository:

    def test_to_model_converte_com_sucesso(self, repository, historico_sqlalchemy_base):
        """
        Cenário: Testa a conversão de uma entidade SQLAlchemy para o modelo Pydantic.
        Resultado Esperado: O modelo Pydantic é retornado com todos os dados corretos.
        """
        model = repository.to_model(historico_sqlalchemy_base)

        assert isinstance(model, HistoricoEstoque)
        assert model.id == 1
        assert model.seller_id == "seller-123"
        assert model.sku == "SKU-ABC-001"
        assert model.tipo_movimentacao == "ATUALIZACAO"

    def test_to_model_retorna_none_para_entrada_nula(self, repository):
        """
        Cenário: Testa o comportamento do método ao receber None.
        Resultado Esperado: Retorna None.
        """
        assert repository.to_model(None) is None

    @pytest.mark.asyncio
    async def test_find_by_period_com_seller_id(self, repository, session_mock, historico_sqlalchemy_base):
        """
        Cenário: Busca registros em um período para um vendedor específico.
        Resultado Esperado: Retorna uma lista de históricos para aquele vendedor.
        """
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [historico_sqlalchemy_base]
        session_mock.execute.return_value = mock_result
        
        start_date = datetime.now() - timedelta(days=1)
        end_date = datetime.now()
        results = await repository.find_by_period(start_date, end_date, seller_id="seller-123")

        session_mock.execute.assert_called_once()
        assert len(results) == 1
        assert results[0].seller_id == "seller-123"

        executed_stmt_str = str(session_mock.execute.call_args[0][0])
        assert "pc_estoque_historico.seller_id = :seller_id_1" in executed_stmt_str

    @pytest.mark.asyncio
    async def test_find_by_period_sem_seller_id(self, repository, session_mock, historico_sqlalchemy_base):
        """
        Cenário: Busca registros em um período sem especificar o vendedor.
        Resultado Esperado: Retorna uma lista de históricos sem o filtro de vendedor.
        """
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [historico_sqlalchemy_base]
        session_mock.execute.return_value = mock_result
        
        start_date = datetime.now() - timedelta(days=1)
        end_date = datetime.now()
        results = await repository.find_by_period(start_date, end_date)

        session_mock.execute.assert_called_once()
        assert len(results) == 1

        executed_stmt_str = str(session_mock.execute.call_args[0][0])
        assert "pc_estoque_historico.seller_id = :seller_id_1" not in executed_stmt_str

    @pytest.mark.asyncio
    async def test_find_by_period_retorna_lista_vazia(self, repository, session_mock):
        """
        Cenário: A busca por período não encontra nenhum registro no banco.
        Resultado Esperado: O método retorna uma lista vazia.
        """
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []  # Banco não retornou nada
        session_mock.execute.return_value = mock_result
        
        start_date = datetime.now() - timedelta(days=1)
        end_date = datetime.now()
        results = await repository.find_by_period(start_date, end_date)

        session_mock.execute.assert_called_once()
        assert results == []