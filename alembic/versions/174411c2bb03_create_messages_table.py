"""Create messages table

Revision ID: 174411c2bb03
Revises: 69ee1fc24ecc
Create Date: 2024-10-21 12:18:47.444074

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '174411c2bb03'
down_revision: Union[str, None] = '69ee1fc24ecc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('text', sa.String, nullable=False),
        sa.Column('sender_type', sa.Enum('user', 'bot', name='sender_type_enum'), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now())
    )

def downgrade() -> None:
    op.drop_table('messages')
