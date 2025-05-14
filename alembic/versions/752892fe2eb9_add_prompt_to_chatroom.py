"""add prompt to chatroom

Revision ID: 752892fe2eb9
Revises: 46958ac11f21
Create Date: 2025-05-14 15:48:34.918733

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision: str = '752892fe2eb9'
down_revision: Union[str, None] = '46958ac11f21'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('chatrooms', sa.Column('prompt_modifier', JSONB, nullable=True))


def downgrade() -> None:
    op.drop_column('chatrooms', 'prompt_modifier')
