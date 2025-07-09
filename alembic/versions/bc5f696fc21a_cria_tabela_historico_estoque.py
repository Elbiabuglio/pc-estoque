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
        {'seller_id': 'seller_a', 'sku': 'sku_001', 'quantidade_anterior': 0, 'quantidade_nova': 120, 'tipo_movimentacao': 'CRIACAO', 'movimentado_em': now - timedelta(days=10)},
        {'seller_id': 'seller_a', 'sku': 'sku_001', 'quantidade_anterior': 0, 'quantidade_nova': 100, 'tipo_movimentacao': 'ATUALIZACAO', 'movimentado_em': now - timedelta(days=5)},
        {'seller_id': 'seller_a', 'sku': 'sku_002', 'quantidade_anterior': 0, 'quantidade_nova': 50, 'tipo_movimentacao': 'CRIACAO', 'movimentado_em': now - timedelta(days=8)},
        {'seller_id': 'seller_a', 'sku': 'sku_003', 'quantidade_anterior': 0, 'quantidade_nova': 300, 'tipo_movimentacao': 'CRIACAO', 'movimentado_em': now - timedelta(days=5)},
        {'seller_id': 'seller_a', 'sku': 'sku_003', 'quantidade_anterior': 0, 'quantidade_nova': 200, 'tipo_movimentacao': 'ATUALIZACAO', 'movimentado_em': now - timedelta(days=3)},
        {'seller_id': 'seller_b', 'sku': 'sku_003', 'quantidade_anterior': 0, 'quantidade_nova': 50, 'tipo_movimentacao': 'CRIACAO', 'movimentado_em': now - timedelta(days=3)},
        {'seller_id': 'seller_b', 'sku': 'sku_004', 'quantidade_anterior': 0, 'quantidade_nova': 300, 'tipo_movimentacao': 'CRIACAO', 'movimentado_em': now - timedelta(days=2)},
        {'seller_id': 'seller_b', 'sku': 'sku_005', 'quantidade_anterior': 0, 'quantidade_nova': 120, 'tipo_movimentacao': 'CRIACAO', 'movimentado_em': now - timedelta(days=1)},
        {'seller_id': 'seller_b', 'sku': 'sku_006', 'quantidade_anterior': 0, 'quantidade_nova': 97, 'tipo_movimentacao': 'CRIACAO', 'movimentado_em': now - timedelta(days=1)},
        {'seller_id': 'seller_b', 'sku': 'sku_006', 'quantidade_anterior': 0, 'quantidade_nova': 80, 'tipo_movimentacao': 'ATUALIZACAO', 'movimentado_em': now},
        {'seller_id': 'seller_b', 'sku': 'sku_007', 'quantidade_anterior': 0, 'quantidade_nova': 60, 'tipo_movimentacao': 'CRIACAO', 'movimentado_em': now - timedelta(days=7)},
        {'seller_id': 'luizalabs', 'sku': 'sku_008', 'quantidade_anterior': 0, 'quantidade_nova': 112, 'tipo_movimentacao': 'CRIACAO', 'movimentado_em': now - timedelta(days=20)},
        {'seller_id': 'luizalabs', 'sku': 'sku_008', 'quantidade_anterior': 0, 'quantidade_nova': 100, 'tipo_movimentacao': 'ATUALIZACAO', 'movimentado_em': now - timedelta(days=14)},
        {'seller_id': 'luizalabs', 'sku': 'sku_008', 'quantidade_anterior': 0, 'quantidade_nova': 90, 'tipo_movimentacao': 'ATUALIZACAO', 'movimentado_em': now - timedelta(days=10)},
        {'seller_id': 'luizalabs', 'sku': 'sku_009', 'quantidade_anterior': 0, 'quantidade_nova': 223, 'tipo_movimentacao': 'CRIACAO', 'movimentado_em': now - timedelta(days=15)},
        {'seller_id': 'luizalabs', 'sku': 'sku_009', 'quantidade_anterior': 0, 'quantidade_nova': 110, 'tipo_movimentacao': 'ATUALIZACAO', 'movimentado_em': now - timedelta(days=7)},
        {'seller_id': 'luizalabs', 'sku': 'sku_010', 'quantidade_anterior': 0, 'quantidade_nova': 138, 'tipo_movimentacao': 'CRIACAO', 'movimentado_em': now - timedelta(days=10)},
        {'seller_id': 'luizalabs', 'sku': 'sku_010', 'quantidade_anterior': 0, 'quantidade_nova': 130, 'tipo_movimentacao': 'ATUALIZACAO', 'movimentado_em': now - timedelta(days=6)},
        {'seller_id': 'luizalabs', 'sku': 'sku_011', 'quantidade_anterior': 0, 'quantidade_nova': 140, 'tipo_movimentacao': 'CRIACAO', 'movimentado_em': now - timedelta(days=5)},
        {'seller_id': 'luizalabs', 'sku': 'sku_012', 'quantidade_anterior': 0, 'quantidade_nova': 160, 'tipo_movimentacao': 'CRIACAO', 'movimentado_em': now - timedelta(days=3)},
        {'seller_id': 'luizalabs', 'sku': 'sku_013', 'quantidade_anterior': 0, 'quantidade_nova': 170, 'tipo_movimentacao': 'CRIACAO', 'movimentado_em': now - timedelta(days=1)},
        {'seller_id': 'luizalabs', 'sku': 'sku_014', 'quantidade_anterior': 0, 'quantidade_nova': 180, 'tipo_movimentacao': 'CRIACAO', 'movimentado_em': now - timedelta(days=2)},
        {'seller_id': 'luizalabs', 'sku': 'sku_015', 'quantidade_anterior': 0, 'quantidade_nova': 190, 'tipo_movimentacao': 'CRIACAO', 'movimentado_em': now - timedelta(days=1)},
        {'seller_id': 'seller_d', 'sku': 'sku_016', 'quantidade_anterior': 0, 'quantidade_nova': 200, 'tipo_movimentacao': 'CRIACAO', 'movimentado_em': now - timedelta(days=9)},
        {'seller_id': 'seller_d', 'sku': 'sku_017', 'quantidade_anterior': 0, 'quantidade_nova': 210, 'tipo_movimentacao': 'CRIACAO', 'movimentado_em': now - timedelta(days=4)},
        {'seller_id': 'seller_d', 'sku': 'sku_018', 'quantidade_anterior': 0, 'quantidade_nova': 220, 'tipo_movimentacao': 'CRIACAO', 'movimentado_em': now - timedelta(days=4)},
        {'seller_id': 'seller_d', 'sku': 'sku_019', 'quantidade_anterior': 0, 'quantidade_nova': 230, 'tipo_movimentacao': 'CRIACAO', 'movimentado_em': now},
        {'seller_id': 'seller_d', 'sku': 'sku_020', 'quantidade_anterior': 0, 'quantidade_nova': 240, 'tipo_movimentacao': 'CRIACAO', 'movimentado_em': now},
    ]

    op.bulk_insert(historico_table, seed_data)

def downgrade() -> None:
    print("--> REVERTENDO MIGRAÇÃO SIMPLIFICADA <--")
    op.drop_index("idx_historico_estoque_seller_id_movimentado_em", table_name=TABLE_NAME)
    op.drop_table(TABLE_NAME)
    # Não precisamos mais remover o tipo ENUM, pois ele não existe mais no schema.