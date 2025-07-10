import pytest
from unittest.mock import AsyncMock
from datetime import datetime, timedelta, timezone

from app.services.historico_estoque_service import HistoricoEstoqueService

@pytest.fixture
def mock_repository():
    repo = AsyncMock()
    return repo

@pytest.fixture
def service(mock_repository):
    return HistoricoEstoqueService(historico_repository=mock_repository)

@pytest.mark.asyncio
async def test_get_relatorio_semanal(service, mock_repository):
    mock_repository.find_by_period.return_value = ["item1", "item2"]
    seller_id = "seller1"
    result = await service.get_relatorio_semanal(seller_id)
    assert result == ["item1", "item2"]
    args, kwargs = mock_repository.find_by_period.call_args
    start_date, end_date, sid = args
    assert sid == seller_id
    assert (end_date - start_date).days == 7

@pytest.mark.asyncio
async def test_get_relatorio_diario(service, mock_repository):
    mock_repository.find_by_period.return_value = ["itemA"]
    seller_id = "seller2"
    result = await service.get_relatorio_diario(seller_id)
    assert result == ["itemA"]
    args, kwargs = mock_repository.find_by_period.call_args
    start_date, end_date, sid = args
    assert sid == seller_id
    assert start_date.hour == 0 and start_date.minute == 0 and start_date.second == 0 and start_date.microsecond == 0
    assert end_date > start_date