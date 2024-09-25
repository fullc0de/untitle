"""Add quantity field to items table

Revision ID: 69ee1fc24ecc
Revises: 4bd713038b5a
Create Date: 2024-09-25 11:04:50.942086

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '69ee1fc24ecc'
down_revision: Union[str, None] = '4bd713038b5a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('items', sa.Column('quantity', sa.Integer(), nullable=True))

def downgrade() -> None:
    op.drop_column('items', 'quantity')
