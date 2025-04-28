"""add users table

Revision ID: ee151bdff133
Revises: 
Create Date: 2025-04-28 13:43:40.779939

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision: str = 'ee151bdff133'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nickname', sa.String(), nullable=False, index=True),
        sa.Column('password', sa.String(), nullable=True),
        sa.Column('profile', JSONB, nullable=False, server_default='{}'),
        sa.Column('token', sa.String(), nullable=True, index=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('users')
