import pytest
from unittest.mock import MagicMock, AsyncMock
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer

from app.integrations.database.sqlalchemy_client import SQLAlchemyClient

Base = declarative_base()

class DummyModel(Base):
    __tablename__ = 'dummy'
    id = Column(Integer, primary_key=True)

class AsyncContextManagerMock:
    def __init__(self, mock):
        self.mock = mock

    async def __aenter__(self):
        return self.mock

    async def __aexit__(self, exc_type, exc, tb):
        pass

def test_init_and_close():
    client = SQLAlchemyClient("postgresql+asyncpg://user:pass@localhost/dbname")

    mock_engine = MagicMock()
    mock_session_maker = MagicMock()

    client.engine = mock_engine
    client.session_maker = mock_session_maker

    client.close()

    mock_session_maker.close_all.assert_called_once()
    mock_engine.dispose.assert_called_once()
    assert client.engine is None

@pytest.mark.asyncio
async def test_make_session():
    client = SQLAlchemyClient("postgresql+asyncpg://user:pass@localhost/dbname")

    mock_session = AsyncMock()
    client.session_maker = MagicMock(return_value=AsyncContextManagerMock(mock_session))

    async with client.make_session() as session:
        assert session == mock_session

def test_init_select_and_delete():
    sel = SQLAlchemyClient.init_select_estoque(DummyModel)
    assert sel is not None

    dele = SQLAlchemyClient.init_delete_estoque(DummyModel)
    assert dele is not None

def test_to_dict():
    class Dummy:
        def __init__(self):
            self.a = 1
            self.b = 2
            self._sa_instance_state = "state"
            self.__dict__ = {"a": self.a, "b": self.b, "_sa_instance_state": self._sa_instance_state}

    dummy = Dummy()
    d = SQLAlchemyClient.to_dict(dummy)
    assert "_sa_instance_state" not in d
    assert d["a"] == 1
    assert d["b"] == 2

    assert SQLAlchemyClient.to_dict(None) is None

def test_get_pk_fields():
    class Dummy:
        __table__ = MagicMock()
        __table__.columns = []

        col1 = MagicMock()
        col1.name = "id"
        col1.primary_key = True

        col2 = MagicMock()
        col2.name = "name"
        col2.primary_key = False

        col3 = MagicMock()
        col3.name = "code"
        col3.primary_key = True

        __table__.columns.extend([col1, col2, col3])

    pk_fields = SQLAlchemyClient.get_pk_fields(Dummy)
    assert "id" in pk_fields
    assert "code" in pk_fields
    assert "name" not in pk_fields
