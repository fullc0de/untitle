"""Create user table

Revision ID: 036b340f007a
Revises: c3d2dbffadaa
Create Date: 2024-10-31 15:50:58.219421

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision: str = '036b340f007a'
down_revision: Union[str, None] = 'c3d2dbffadaa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('nickname', sa.String(), nullable=False),
        sa.Column('role', JSONB, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False)
    )

def downgrade() -> None:
    op.drop_table('users')
