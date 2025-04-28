"""add chatrooms table

Revision ID: 7c7a75aedb95
Revises: 232a7965912e
Create Date: 2025-04-28 14:27:18.934323

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision: str = '7c7a75aedb95'
down_revision: Union[str, None] = '232a7965912e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'chatrooms',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.Column('bot_id', sa.Integer(), nullable=False),
        sa.Column('property', JSONB, nullable=False, server_default='{}'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['bot_id'], ['bots.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('chatrooms')
