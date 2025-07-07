"""cria tabela historico_estoque

Revision ID: bc5f696fc21a
Revises: a63f34ea2de0
Create Date: 2025-07-07 18:00:37.019962

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'bc5f696fc21a'
down_revision: Union[str, None] = 'a63f34ea2de0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLE_NAME = "pc_estoque_historico"

tipo_movimentacao_enum = sa.Enum(
    "CRIACAO", "ATUALIZACAO", "EXCLUSAO",
    name="tipomovimentacaoenum"
)

def upgrade() -> None:
    tipo_movimentacao_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        TABLE_NAME,
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('seller_id', sa.String(), nullable=False),
        sa.Column('sku', sa.String(), nullable=False),
        sa.Column('quantidade_anterior', sa.Integer(), nullable=False),
        sa.Column('quantidade_nova', sa.Integer(), nullable=False),
        sa.Column('tipo_movimentacao', tipo_movimentacao_enum, nullable=False),
        sa.Column('movimentado_em', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_index(
        "idx_historico_estoque_seller_id_movimentado_em",
        TABLE_NAME,
        ["seller_id", "movimentado_em"],
        unique=False
    )
    op.create_index(
        "idx_historico_estoque_sku",
        TABLE_NAME,
        ["sku"],
        unique=False
    )

def downgrade() -> None:
    op.drop_index("idx_historico_estoque_seller_id_movimentado_em", table_name=TABLE_NAME, if_exists=True)
    op.drop_index("idx_historico_estoque_sku", table_name=TABLE_NAME, if_exists=True)
    op.drop_table(TABLE_NAME)
    tipo_movimentacao_enum.drop(op.get_bind(), checkfirst=True)