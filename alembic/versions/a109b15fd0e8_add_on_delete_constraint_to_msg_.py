"""Add on delete constraint to msg_embeddings_message_id_fkey

Revision ID: a109b15fd0e8
Revises: 34aa5446bdae
Create Date: 2024-11-05 11:57:40.754723

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a109b15fd0e8'
down_revision: Union[str, None] = '34aa5446bdae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 기존 외래 키 제약 조건 삭제
    op.drop_constraint('msg_embeddings_message_id_fkey', 'msg_embeddings', type_='foreignkey')
    
    # CASCADE DELETE가 포함된 새로운 외래 키 제약 조건 추가
    op.create_foreign_key(
        'msg_embeddings_message_id_fkey',
        'msg_embeddings',
        'messages',
        ['message_id'],
        ['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    # CASCADE DELETE가 포함된 외래 키 제약 조건 삭제
    op.drop_constraint('msg_embeddings_message_id_fkey', 'msg_embeddings', type_='foreignkey')
    
    # 기존 외래 키 제약 조건 복원
    op.create_foreign_key(
        'msg_embeddings_message_id_fkey',
        'msg_embeddings',
        'messages',
        ['message_id'],
        ['id']
    )
