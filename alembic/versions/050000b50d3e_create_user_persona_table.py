"""create user_persona_table

Revision ID: 050000b50d3e
Revises: 63ad2aa58e33
Create Date: 2025-03-28 15:29:30.755850

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '050000b50d3e'
down_revision: Union[str, None] = '63ad2aa58e33'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Gender enum 타입 생성
    gender_type = sa.Enum('male', 'female', 'non-binary', name='gender')
    
    # UserPersona 테이블 생성
    op.create_table(
        'user_personas',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('chatroom_id', sa.Integer(), sa.ForeignKey('chatrooms.id', ondelete='CASCADE'), nullable=False),
        sa.Column('nickname', sa.String(), nullable=False),
        sa.Column('age', sa.Integer(), nullable=True),
        sa.Column('gender', gender_type, nullable=True),
        sa.Column('description', sa.Text(), nullable=True)
    )
    
    # 인덱스 생성
    op.create_index('ix_user_personas_user_id', 'user_personas', ['user_id'])
    op.create_index('ix_user_personas_chatroom_id', 'user_personas', ['chatroom_id'])


def downgrade() -> None:
    # 인덱스 삭제
    op.drop_index('ix_user_personas_chatroom_id', table_name='user_personas')
    op.drop_index('ix_user_personas_user_id', table_name='user_personas')
    
    # 테이블 삭제
    op.drop_table('user_personas')
    
    # Gender enum 타입 삭제
    op.execute('DROP TYPE gender')
