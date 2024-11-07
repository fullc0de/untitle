"""add a password field to user table

Revision ID: c51ac95d4daa
Revises: cf050a01d1c9
Create Date: 2024-11-07 17:44:25.418171

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c51ac95d4daa'
down_revision: Union[str, None] = 'cf050a01d1c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('password', sa.String(), nullable=True))

def downgrade() -> None:
    op.drop_column('users', 'password')
