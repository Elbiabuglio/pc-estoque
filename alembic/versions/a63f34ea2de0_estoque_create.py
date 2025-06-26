"""estoque-create

Revision ID: a63f34ea2de0
Revises: 
Create Date: 2025-06-10 15:54:24.789067

"""
from typing import Sequence, Union

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


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table(EstoqueBase.__tablename__)
