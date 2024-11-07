"""add delete constraint to attendee

Revision ID: fd5c367d2c64
Revises: 1f2efefdcde1
Create Date: 2024-11-07 18:49:15.411847

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd5c367d2c64'
down_revision: Union[str, None] = '1f2efefdcde1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 기존 외래 키 제약 조건 삭제
    op.drop_constraint('attendees_chatroom_id_fkey', 'attendees', type_='foreignkey')
    
    # CASCADE DELETE가 포함된 새로운 외래 키 제약 조건 추가
    op.create_foreign_key(
        'attendees_chatroom_id_fkey',
        'attendees',
        'chatrooms',
        ['chatroom_id'],
        ['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    # CASCADE DELETE가 포함된 외래 키 제약 조건 삭제
    op.drop_constraint('attendees_chatroom_id_fkey', 'attendees', type_='foreignkey')
    
    # 기본 외래 키 제약 조건 복원
    op.create_foreign_key(
        'attendees_chatroom_id_fkey',
        'attendees',
        'chatrooms',
        ['chatroom_id'],
        ['id']
    )
