"""add attendee_id to user_persona

Revision ID: ba9ccbea2d06
Revises: b92897191760
Create Date: 2025-03-28 15:55:51.358928

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba9ccbea2d06'
down_revision: Union[str, None] = 'b92897191760'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # user_persons 테이블에 attendee_id 컬럼 추가
    op.add_column('user_personas', sa.Column('attendee_id', sa.Integer(), nullable=True))
    
    # attendee_id에 대한 외래키 제약조건 추가
    op.create_foreign_key(
        'fk_user_personas_attendee_id',
        'user_personas',
        'attendees',
        ['attendee_id'],
        ['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    # 외래키 제약조건 삭제
    op.drop_constraint('fk_user_personas_attendee_id', 'user_personas', type_='foreignkey')
    
    # attendee_id 컬럼 삭제
    op.drop_column('user_personas', 'attendee_id')
