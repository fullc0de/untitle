"""add chats table

Revision ID: 46958ac11f21
Revises: 7c7a75aedb95
Create Date: 2025-04-28 14:41:33.314824

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46958ac11f21'
down_revision: Union[str, None] = '7c7a75aedb95'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    sender_type = sa.Enum('user', 'bot', name='sender_type')

    op.create_table(
        'chats',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('chatroom_id', sa.Integer(), nullable=False, index=True),
        sa.Column('sender_id', sa.Integer(), nullable=False),
        sa.Column('sender_type', sender_type, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, index=True),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('chats')
    op.execute("DROP TYPE IF EXISTS sender_type")