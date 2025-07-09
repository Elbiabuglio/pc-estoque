import pytest
from unittest.mock import AsyncMock, patch, MagicMock

@pytest.mark.asyncio
async def test_worker_loop_execucao_uma_vez(monkeypatch):
    # Mock do logger para não poluir o output
    mock_logger = MagicMock()
    monkeypatch.setattr("app.worker.main.logger", mock_logger)

    # Mock do container e do estoque_service
    mock_container = MagicMock()
    mock_estoque_service = MagicMock()
    mock_container.estoque_service.return_value = mock_estoque_service
    monkeypatch.setattr("app.worker.main.Container", lambda: mock_container)

    # Mock da task de verificação
    mock_task = AsyncMock()
    monkeypatch.setattr("app.worker.main.run_low_stock_check_task", mock_task)

    # Mock do asyncio.sleep para não esperar de verdade
    sleep_calls = []
    async def fake_sleep(seconds):
        sleep_calls.append(seconds)
        raise KeyboardInterrupt()  # Para sair do loop após uma iteração

    monkeypatch.setattr("app.worker.main.asyncio.sleep", fake_sleep)

    # Executa o loop (deve rodar só uma vez por causa do KeyboardInterrupt)
    from app.worker import main
    with pytest.raises(KeyboardInterrupt):
        await main.worker_loop()

    # Verifica se a task foi chamada
    mock_task.assert_called_once_with(mock_estoque_service)
    # Verifica se o sleep foi chamado com o intervalo correto
    assert sleep_calls == [120]