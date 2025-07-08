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

    historico_table = sa.table(
        TABLE_NAME,
        sa.column('seller_id', sa.String),
        sa.column('sku', sa.String),
        sa.column('quantidade_anterior', sa.Integer),
        sa.column('quantidade_nova', sa.Integer),
        sa.column('tipo_movimentacao', sa.String),
        sa.column('movimentado_em', sa.DateTime(timezone=True)),
    )

    # --- SEED DATA INSERTION ---
    from datetime import datetime, timedelta

    now = datetime.utcnow()
    seed_data = [
        # History for seller_a, sku_001
        {'seller_id': 'seller_a', 'sku': 'sku_001', 'quantidade_anterior': 0, 'quantidade_nova': 150, 'tipo_movimentacao': 'CRIACAO', 'movimentado_em': now - timedelta(days=10)},
        {'seller_id': 'seller_a', 'sku': 'sku_001', 'quantidade_anterior': 150, 'quantidade_nova': 100, 'tipo_movimentacao': 'ATUALIZACAO', 'movimentado_em': now - timedelta(days=5)},

        # History for seller_a, sku_002
        {'seller_id': 'seller_a', 'sku': 'sku_002', 'quantidade_anterior': 0, 'quantidade_nova': 50, 'tipo_movimentacao': 'CRIACAO', 'movimentado_em': now - timedelta(days=8)},

        # History for seller_b, sku_004
        {'seller_id': 'seller_b', 'sku': 'sku_004', 'quantidade_anterior': 250, 'quantidade_nova': 300, 'tipo_movimentacao': 'ajuste', 'movimentado_em': now - timedelta(days=3)},
        {'seller_id': 'seller_b', 'sku': 'sku_004', 'quantidade_anterior': 300, 'quantidade_nova': 280, 'tipo_movimentacao': 'ATUALIZACAO', 'movimentado_em': now - timedelta(days=1)},

        # History for seller_c, sku_010
        {'seller_id': 'seller_c', 'sku': 'sku_010', 'quantidade_anterior': 0, 'quantidade_nova': 130, 'tipo_movimentacao': 'CRIACAO', 'movimentado_em': now - timedelta(days=20)},
        {'seller_id': 'seller_c', 'sku': 'sku_010', 'quantidade_anterior': 130, 'quantidade_nova': 100, 'tipo_movimentacao': 'ATUALIZACAO', 'movimentado_em': now - timedelta(days=15)},
        {'seller_id': 'seller_c', 'sku': 'sku_010', 'quantidade_anterior': 100, 'quantidade_nova': 110, 'tipo_movimentacao': 'CRIACAO', 'movimentado_em': now - timedelta(days=2)},
        
        # History for seller_d, sku_020
        {'seller_id': 'seller_d', 'sku': 'sku_020', 'quantidade_anterior': 200, 'quantidade_nova': 240, 'tipo_movimentacao': 'CRIACAO', 'movimentado_em': now - timedelta(days=7)},

        # History for luizalabs, sku_021
        {'seller_id': 'luizalabs', 'sku': 'sku_021', 'quantidade_anterior': 0, 'quantidade_nova': 300, 'tipo_movimentacao': 'CRIACAO', 'movimentado_em': now - timedelta(days=2)},
        {'seller_id': 'luizalabs', 'sku': 'sku_021', 'quantidade_anterior': 300, 'quantidade_nova': 250, 'tipo_movimentacao': 'ATUALIZACAO', 'movimentado_em': now - timedelta(days=1)},
        # History for luizalabs, sku_022
        {'seller_id': 'luizalabs', 'sku': 'sku_022', 'quantidade_anterior': 0, 'quantidade_nova': 500, 'tipo_movimentacao': 'CRIACAO', 'movimentado_em': now - timedelta(days=3)},
        {'seller_id': 'luizalabs', 'sku': 'sku_022', 'quantidade_anterior': 500, 'quantidade_nova': 450, 'tipo_movimentacao': 'ATUALIZACAO', 'movimentado_em': now - timedelta(days=1)},
        # History for luizalabs, sku_023
        {'seller_id': 'luizalabs', 'sku': 'sku_023', 'quantidade_anterior': 0, 'quantidade_nova': 600, 'tipo_movimentacao': 'CRIACAO', 'movimentado_em': now - timedelta(days=4)},
        {'seller_id': 'luizalabs', 'sku': 'sku_023', 'quantidade_anterior': 600, 'quantidade_nova': 550, 'tipo_movimentacao': 'ATUALIZACAO', 'movimentado_em': now - timedelta(days=2)},
        # History for luizalabs, sku_024
        {'seller_id': 'luizalabs', 'sku': 'sku_024', 'quantidade_anterior': 0, 'quantidade_nova': 700, 'tipo_movimentacao': 'CRIACAO', 'movimentado_em': now - timedelta(days=5)},
        {'seller_id': 'luizalabs', 'sku': 'sku_024', 'quantidade_anterior': 700, 'quantidade_nova': 650, 'tipo_movimentacao': 'ATUALIZACAO', 'movimentado_em': now - timedelta(days=3)},
    ]

    op.bulk_insert(historico_table, seed_data)

def downgrade() -> None:
    print("--> REVERTENDO MIGRAÇÃO SIMPLIFICADA <--")
    op.drop_index("idx_historico_estoque_seller_id_movimentado_em", table_name=TABLE_NAME)
    op.drop_table(TABLE_NAME)
    # Não precisamos mais remover o tipo ENUM, pois ele não existe mais no schema.