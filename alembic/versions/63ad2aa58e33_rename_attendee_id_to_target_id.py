"""rename attendee_id to target_id

Revision ID: 63ad2aa58e33
Revises: d501b44e0c3c
Create Date: 2025-03-21 11:33:13.173228

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '63ad2aa58e33'
down_revision: Union[str, None] = 'd501b44e0c3c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # attendees 테이블의 인덱스 삭제
    op.drop_index('ix_attendees_attendee_id', table_name='attendees')
    
    # 컬럼 이름 변경
    op.alter_column('attendees', 'attendee_id', new_column_name='target_id')
    
    # 새로운 인덱스 생성
    op.create_index('ix_attendees_target_id', 'attendees', ['target_id'])


def downgrade() -> None:
    # 새로운 인덱스 삭제
    op.drop_index('ix_attendees_target_id', table_name='attendees')
    
    # 컬럼 이름을 원래대로 변경
    op.alter_column('attendees', 'target_id', new_column_name='attendee_id')
    
    # 원래 인덱스 복원
    op.create_index('ix_attendees_attendee_id', 'attendees', ['attendee_id'])
