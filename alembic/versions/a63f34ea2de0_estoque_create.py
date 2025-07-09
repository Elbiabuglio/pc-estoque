"""estoque-create

Revision ID: a63f34ea2de0
Revises: 
Create Date: 2025-06-10 15:54:24.789067

"""
from typing import Sequence, Union
from datetime import datetime

from alembic import op
import sqlalchemy as sa

from app.repositories.estoque_repository import EstoqueBase

# revision identifiers, used by Alembic.
revision: str = 'a63f34ea2de0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    
    op.create_table(
        EstoqueBase.__tablename__,
        sa.Column('id', sa.INTEGER(), primary_key=True, nullable=False),
        sa.Column('seller_id', sa.String(), nullable=False),
        sa.Column('sku', sa.String(), nullable=False),
        sa.Column('quantidade', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_index(
        "idx_estoque_sellerid_sku",
        EstoqueBase.__tablename__,
        ["seller_id", "sku"],
        unique=True
    )

    estoque_table = sa.table(
        EstoqueBase.__tablename__,
        sa.column('seller_id', sa.String),
        sa.column('sku', sa.String),
        sa.column('quantidade', sa.Integer),
        sa.column('created_at', sa.DateTime(timezone=True)),
        sa.column('updated_at', sa.DateTime(timezone=True)),
    )

    now = datetime.utcnow()
    op.bulk_insert(
        estoque_table,
        [
            {'seller_id': 'seller_a', 'sku': 'sku_001', 'quantidade': 100, 'created_at': now, 'updated_at': now},
            {'seller_id': 'seller_a', 'sku': 'sku_002', 'quantidade': 50, 'created_at': now, 'updated_at': now},
            {'seller_id': 'seller_a', 'sku': 'sku_003', 'quantidade': 200, 'created_at': now, 'updated_at': now},
            {'seller_id': 'seller_b', 'sku': 'sku_003', 'quantidade': 50, 'created_at': now, 'updated_at': now},
            {'seller_id': 'seller_b', 'sku': 'sku_004', 'quantidade': 300, 'created_at': now, 'updated_at': now},
            {'seller_id': 'seller_b', 'sku': 'sku_005', 'quantidade': 120, 'created_at': now, 'updated_at': now},
            {'seller_id': 'seller_b', 'sku': 'sku_006', 'quantidade': 80, 'created_at': now, 'updated_at': now},
            {'seller_id': 'seller_b', 'sku': 'sku_007', 'quantidade': 60, 'created_at': now, 'updated_at': now},
            {'seller_id': 'luizalabs', 'sku': 'sku_008', 'quantidade': 90, 'created_at': now, 'updated_at': now},
            {'seller_id': 'luizalabs', 'sku': 'sku_009', 'quantidade': 110, 'created_at': now, 'updated_at': now},
            {'seller_id': 'luizalabs', 'sku': 'sku_010', 'quantidade': 130, 'created_at': now, 'updated_at': now},
            {'seller_id': 'luizalabs', 'sku': 'sku_011', 'quantidade': 140, 'created_at': now, 'updated_at': now},
            {'seller_id': 'luizalabs', 'sku': 'sku_012', 'quantidade': 160, 'created_at': now, 'updated_at': now},
            {'seller_id': 'luizalabs', 'sku': 'sku_013', 'quantidade': 170, 'created_at': now, 'updated_at': now},
            {'seller_id': 'luizalabs', 'sku': 'sku_014', 'quantidade': 180, 'created_at': now, 'updated_at': now},
            {'seller_id': 'luizalabs', 'sku': 'sku_015', 'quantidade': 190, 'created_at': now, 'updated_at': now},
            {'seller_id': 'seller_d', 'sku': 'sku_016', 'quantidade': 200, 'created_at': now, 'updated_at': now},
            {'seller_id': 'seller_d', 'sku': 'sku_017', 'quantidade': 210, 'created_at': now, 'updated_at': now},
            {'seller_id': 'seller_d', 'sku': 'sku_018', 'quantidade': 220, 'created_at': now, 'updated_at': now},
            {'seller_id': 'seller_d', 'sku': 'sku_019', 'quantidade': 230, 'created_at': now, 'updated_at': now},
            {'seller_id': 'seller_d', 'sku': 'sku_020', 'quantidade': 240, 'created_at': now, 'updated_at': now},
        ],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table(EstoqueBase.__tablename__)
