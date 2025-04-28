"""add bots table

Revision ID: 232a7965912e
Revises: ee151bdff133
Create Date: 2025-04-28 13:49:01.615050

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision: str = '232a7965912e'
down_revision: Union[str, None] = 'ee151bdff133'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'bots',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False, index=True),
        sa.Column('owner_id', sa.Integer(), nullable=False, index=True),
        sa.Column('profile', JSONB, nullable=True, server_default='{}'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('bots')
