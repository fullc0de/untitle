"""Add session_id to messages with delete constraint

Revision ID: 34aa5446bdae
Revises: e88f8fa14aac
Create Date: 2024-11-05 11:40:31.012906

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '34aa5446bdae'
down_revision: Union[str, None] = 'e88f8fa14aac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # session_id 컬럼 추가
    op.add_column(
        'messages',
        sa.Column('session_id', sa.Integer(), nullable=True)
    )

    # 외래 키 제약 조건 추가 (CASCADE DELETE 포함)
    op.create_foreign_key(
        'fk_messages_session_id',
        'messages',
        'sessions',
        ['session_id'],
        ['id'],
        ondelete='CASCADE'
    )

    # session_id에 대한 인덱스 생성
    op.create_index(
        'ix_messages_session_id',
        'messages',
        ['session_id']
    )


def downgrade() -> None:
    # 인덱스 삭제
    op.drop_index('ix_messages_session_id', table_name='messages')
    
    # 외래 키 제약 조건 삭제
    op.drop_constraint('fk_messages_session_id', 'messages', type_='foreignkey')
    
    # 컬럼 삭제
    op.drop_column('messages', 'session_id')
