"""cria tabela historico_estoque

Revision ID: bc5f696fc21a
Revises: a63f34ea2de0
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'bc5f696fc21a'
down_revision: Union[str, None] = 'a63f34ea2de0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLE_NAME = "pc_estoque_historico"

def upgrade() -> None:
    print("--> EXECUTANDO MIGRAÇÃO SIMPLIFICADA (COLUNA COMO STRING) <--")
    op.create_table(
        TABLE_NAME,
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('seller_id', sa.String(), nullable=False, index=True),
        sa.Column('sku', sa.String(), nullable=False, index=True),
        sa.Column('quantidade_anterior', sa.Integer(), nullable=False),
        sa.Column('quantidade_nova', sa.Integer(), nullable=False),
        
        # MUDANÇA PRINCIPAL: Usando um simples String em vez de um ENUM.
        sa.Column('tipo_movimentacao', sa.String(length=20), nullable=False),
        
        sa.Column('movimentado_em', sa.DateTime(timezone=True), nullable=False, index=True),
    )

    op.create_index(
        "idx_historico_estoque_seller_id_movimentado_em",
        TABLE_NAME,
        ["seller_id", "movimentado_em"],
        unique=False
    )

def downgrade() -> None:
    print("--> REVERTENDO MIGRAÇÃO SIMPLIFICADA <--")
    op.drop_index("idx_historico_estoque_seller_id_movimentado_em", table_name=TABLE_NAME)
    op.drop_table(TABLE_NAME)
    # Não precisamos mais remover o tipo ENUM, pois ele não existe mais no schema.