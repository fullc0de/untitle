"""rename sessions to chatrooms

Revision ID: 1f2efefdcde1
Revises: c51ac95d4daa
Create Date: 2024-11-07 18:11:33.584779

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1f2efefdcde1'
down_revision: Union[str, None] = 'c51ac95d4daa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 기존 외래 키 제약 조건 삭제
    op.drop_constraint('fk_messages_session_id', 'messages', type_='foreignkey')
    op.drop_constraint('attendees_session_id_fkey', 'attendees', type_='foreignkey')
    
    # 인덱스 삭제
    op.drop_index('ix_messages_session_id', table_name='messages')
    op.drop_index('ix_attendees_session_id', table_name='attendees')
    
    # sessions 테이블 이름 변경
    op.rename_table('sessions', 'chatrooms')
    
    # messages 테이블의 컬럼 이름 변경
    op.alter_column('messages', 'session_id', new_column_name='chatroom_id')
    
    # attendees 테이블의 컬럼 이름 변경
    op.alter_column('attendees', 'session_id', new_column_name='chatroom_id')
    
    # 새로운 외래 키 제약 조건 추가
    op.create_foreign_key(
        'fk_messages_chatroom_id',
        'messages',
        'chatrooms',
        ['chatroom_id'],
        ['id'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'attendees_chatroom_id_fkey',
        'attendees',
        'chatrooms',
        ['chatroom_id'],
        ['id']
    )
    
    # 새로운 인덱스 생성
    op.create_index('ix_messages_chatroom_id', 'messages', ['chatroom_id'])
    op.create_index('ix_attendees_chatroom_id', 'attendees', ['chatroom_id'])


def downgrade() -> None:
    # 외래 키 제약 조건 삭제
    op.drop_constraint('fk_messages_chatroom_id', 'messages', type_='foreignkey')
    op.drop_constraint('attendees_chatroom_id_fkey', 'attendees', type_='foreignkey')
    
    # 인덱스 삭제
    op.drop_index('ix_messages_chatroom_id', table_name='messages')
    op.drop_index('ix_attendees_chatroom_id', table_name='attendees')
    
    # chatrooms 테이블 이름을 다시 sessions로 변경
    op.rename_table('chatrooms', 'sessions')
    
    # messages 테이블의 컬럼 이름 변경
    op.alter_column('messages', 'chatroom_id', new_column_name='session_id')
    
    # attendees 테이블의 컬럼 이름 변경
    op.alter_column('attendees', 'session_id', new_column_name='session_id')
    
    # 이전 외래 키 제약 조건 복원
    op.create_foreign_key(
        'fk_messages_session_id',
        'messages',
        'sessions',
        ['session_id'],
        ['id'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'attendees_session_id_fkey',
        'attendees',
        'sessions',
        ['session_id'],
        ['id']
    )
    
    # 이전 인덱스 복원
    op.create_index('ix_messages_session_id', 'messages', ['session_id'])
    op.create_index('ix_attendees_session_id', 'attendees', ['session_id'])
