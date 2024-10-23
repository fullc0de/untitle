"""Create msg_embeddings table

Revision ID: 18871db411df
Revises: 4888c13e4d60
Create Date: 2024-10-22 16:32:32.882919

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '18871db411df'
down_revision: Union[str, None] = '4888c13e4d60'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # pgvector 확장 생성
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')

    # msg_embeddings 테이블 생성
    op.create_table(
        'msg_embeddings',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('embedding', sa.dialects.postgresql.ARRAY(sa.Float), nullable=False),
        sa.Column('message_id', sa.Integer, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )

    # embedding 컬럼을 vector 타입으로 변경
    op.execute('ALTER TABLE msg_embeddings ALTER COLUMN embedding TYPE vector(3072)')

    # embedding 컬럼에 인덱스 생성
    #op.execute('CREATE INDEX embedding_idx ON msg_embeddings USING hnsw (embedding vector_cosine_ops)')


def downgrade() -> None:
    # 인덱스 삭제
    #op.execute('DROP INDEX IF EXISTS embedding_idx')

    # 테이블 삭제
    op.drop_table('msg_embeddings')

    # pgvector 확장 삭제 (선택적)
    op.execute('DROP EXTENSION IF EXISTS vector')
