from datetime import datetime, timedelta, timezone
from typing import List
from app.models.historico_estoque_model import HistoricoEstoque
from app.repositories.historico_estoque_repository import HistoricoEstoqueRepository

class HistoricoEstoqueService:
    def __init__(self, historico_repository: HistoricoEstoqueRepository):
        self.historico_repository = historico_repository

    async def get_relatorio_semanal(self, seller_id: str | None) -> List[HistoricoEstoque]:
        """
        Retorna o histórico de movimentações dos últimos 7 dias.
        """
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=7)
        return await self.historico_repository.find_by_period(start_date, end_date, seller_id)

    async def get_relatorio_diario(self, seller_id: str | None) -> List[HistoricoEstoque]:
        """
        Retorna o histórico de movimentações do dia atual.
        """
        end_date = datetime.now(timezone.utc)
        start_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0)
        return await self.historico_repository.find_by_period(start_date, end_date, seller_id)