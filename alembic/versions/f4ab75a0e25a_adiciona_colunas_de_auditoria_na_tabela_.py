"""adiciona colunas de auditoria na tabela de historico de estoque

Revision ID: f4ab75a0e25a
Revises: bc5f696fc21a
Create Date: 2025-07-07 20:23:14.128378

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4ab75a0e25a'
down_revision: Union[str, None] = 'bc5f696fc21a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLE_NAME = "pc_estoque_historico"

def upgrade() -> None:
    print("--> ADICIONANDO COLUNAS DE AUDITORIA (created_at, updated_at) <--")
    op.add_column(TABLE_NAME, sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))
    op.add_column(TABLE_NAME, sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))


def downgrade() -> None:
    print("--> REMOVENDO COLUNAS DE AUDITORIA (created_at, updated_at) <--")
    op.drop_column(TABLE_NAME, 'updated_at')
    op.drop_column(TABLE_NAME, 'created_at')
