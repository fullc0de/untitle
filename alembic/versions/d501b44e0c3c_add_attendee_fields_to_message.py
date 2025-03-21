"""add attendee fields to message

Revision ID: d501b44e0c3c
Revises: fd5c367d2c64
Create Date: 2025-03-21 10:38:10.262643

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd501b44e0c3c'
down_revision: Union[str, None] = 'fd5c367d2c64'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # sender_type enum 삭제를 위해 기존 컬럼 제거
    op.drop_column('messages', 'sender_type')
    
    # sender_type enum 타입 삭제
    op.execute('DROP TYPE IF EXISTS sendertype')
    
    # attendee_id와 attendee_type 컬럼 추가
    op.add_column('messages', sa.Column('attendee_id', sa.Integer(), nullable=False))
    op.add_column('messages', sa.Column('attendee_type', sa.Enum(name='attendeetype'), nullable=False))
    
    # 인덱스 생성
    op.create_index('ix_messages_attendee_id', 'messages', ['attendee_id'])
    
    # 외래 키 제약 조건 추가
    op.create_foreign_key(
        'fk_messages_attendee',
        'messages',
        'attendees',
        ['attendee_id'],
        ['id']
    )


def downgrade() -> None:
    # 외래 키 제약 조건 삭제
    op.drop_constraint('fk_messages_attendee', 'messages', type_='foreignkey')
    
    # 인덱스 삭제
    op.drop_index('ix_messages_attendee_id', table_name='messages')
    
    # attendee 관련 컬럼 삭제
    op.drop_column('messages', 'attendee_type')
    op.drop_column('messages', 'attendee_id')
    
    # sender_type enum 타입 생성
    op.execute("CREATE TYPE sendertype AS ENUM ('user', 'assistant')")
    
    # sender_type 컬럼 추가
    op.add_column('messages', sa.Column('sender_type', sa.Enum('user', 'assistant', name='sendertype'), nullable=False))