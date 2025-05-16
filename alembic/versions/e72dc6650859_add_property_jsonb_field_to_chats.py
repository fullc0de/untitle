"""add property jsonb field to chats

Revision ID: e72dc6650859
Revises: c3ba8e7c57fd
Create Date: 2025-05-16 17:54:24.510405

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision: str = 'e72dc6650859'
down_revision: Union[str, None] = 'c3ba8e7c57fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('chats', sa.Column('property', JSONB, nullable=False, server_default='{}'))


def downgrade() -> None:
    op.drop_column('chats', 'property')
