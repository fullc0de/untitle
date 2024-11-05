"""Create attendees table

Revision ID: e88f8fa14aac
Revises: a90472827929
Create Date: 2024-11-05 11:33:51.452309

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e88f8fa14aac'
down_revision: Union[str, None] = 'a90472827929'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # AttendeeType enum 생성
    attendee_type = sa.Enum('user', 'bot', name='attendeetype')
    
    op.create_table(
        'attendees',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('session_id', sa.Integer(), sa.ForeignKey('sessions.id'), nullable=False),
        sa.Column('attendee_id', sa.Integer(), nullable=False),
        sa.Column('attendee_type', attendee_type, nullable=False),
    )
    
    # 인덱스 생성
    op.create_index(
        'ix_attendees_session_id',
        'attendees',
        ['session_id']
    )
    op.create_index(
        'ix_attendees_attendee_id',
        'attendees',
        ['attendee_id']
    )


def downgrade() -> None:
    op.drop_index('ix_attendees_attendee_id', table_name='attendees')
    op.drop_index('ix_attendees_session_id', table_name='attendees')
    op.drop_table('attendees')
    
    # AttendeeType enum 삭제
    attendee_type = sa.Enum(name='attendeetype')
    attendee_type.drop(op.get_bind())
