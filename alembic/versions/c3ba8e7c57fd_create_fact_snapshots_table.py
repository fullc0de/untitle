"""create fact_snapshots table

Revision ID: c3ba8e7c57fd
Revises: 752892fe2eb9
Create Date: 2025-05-15 10:27:07.222081

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision: str = 'c3ba8e7c57fd'
down_revision: Union[str, None] = '752892fe2eb9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'fact_snapshots',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('chatroom_id', sa.Integer(), nullable=False, index=True),
        sa.Column('chat_id', sa.Integer(), nullable=False),
        sa.Column('character_info', JSONB, nullable=True),
        sa.Column('conversation_summary', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, index=True),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['chatroom_id'], ['chatrooms.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('fact_snapshots')
