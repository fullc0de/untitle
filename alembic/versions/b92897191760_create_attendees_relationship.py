"""create attendees_relationship

Revision ID: b92897191760
Revises: 050000b50d3e
Create Date: 2025-03-28 15:40:52.580670

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b92897191760'
down_revision: Union[str, None] = '050000b50d3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'attendees_relationship',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('chatroom_id', sa.Integer(), sa.ForeignKey('chatrooms.id', ondelete='CASCADE'), nullable=False),
        sa.Column('relationship', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_index(
        'ix_attendees_relationship_chatroom_id',
        'attendees_relationship',
        ['chatroom_id']
    )


def downgrade() -> None:
    op.drop_index('ix_attendees_relationship_chatroom_id')
    op.drop_table('attendees_relationship')
