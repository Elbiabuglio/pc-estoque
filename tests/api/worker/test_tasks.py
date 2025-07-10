import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.worker import tasks

@pytest.mark.asyncio
async def test_run_low_stock_check_task(monkeypatch):
    # Mock do logger para capturar logs
    mock_logger = MagicMock()
    monkeypatch.setattr(tasks, "logger", mock_logger)

    # Mock do serviço
    mock_service = AsyncMock()
    await tasks.run_low_stock_check_task(mock_service)

    # Verifica se o método foi chamado
    mock_service.check_and_notify_all_low_stock.assert_awaited_once()
    # Verifica se o log foi registrado
    mock_logger.info.assert_any_call("Executando a tarefa de verificação de estoque baixo.")