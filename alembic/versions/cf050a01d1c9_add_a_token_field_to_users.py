"""add a token field to users

Revision ID: cf050a01d1c9
Revises: a109b15fd0e8
Create Date: 2024-11-05 17:51:29.611672

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cf050a01d1c9'
down_revision: Union[str, None] = 'a109b15fd0e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('token', sa.String(), nullable=True))
    op.create_index(op.f('ix_users_token'), 'users', ['token'], unique=True)

def downgrade() -> None:
    op.drop_index(op.f('ix_users_token'), table_name='users')
    op.drop_column('users', 'token')