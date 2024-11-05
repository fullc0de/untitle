"""Create bot table

Revision ID: e115aadabc2d
Revises: 036b340f007a
Create Date: 2024-10-31 15:54:48.075385

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision: str = 'e115aadabc2d'
down_revision: Union[str, None] = '036b340f007a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'bots',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('ai_model', sa.String(), nullable=False),
        sa.Column('property', JSONB, nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False)
    )

def downgrade() -> None:
    op.drop_table('bots')
