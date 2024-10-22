"""Change sender_type enum from bot to assistant

Revision ID: 4888c13e4d60
Revises: 174411c2bb03
Create Date: 2024-10-22 11:53:57.411509

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4888c13e4d60'
down_revision: Union[str, None] = '174411c2bb03'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 기존 enum 타입 변경
    op.execute("ALTER TYPE sender_type_enum RENAME TO sender_type_enum_old")
    
    # 새로운 enum 타입 생성
    op.execute("CREATE TYPE sender_type_enum AS ENUM('user', 'assistant')")
    
    # 컬럼 타입 변경
    op.execute("ALTER TABLE messages ALTER COLUMN sender_type TYPE sender_type_enum USING sender_type::text::sender_type_enum")
    
    # 이전 enum 타입 삭제
    op.execute("DROP TYPE sender_type_enum_old")

def downgrade() -> None:
    # 기존 enum 타입 변경
    op.execute("ALTER TYPE sender_type_enum RENAME TO sender_type_enum_old")
    
    # 이전 enum 타입 생성
    op.execute("CREATE TYPE sender_type_enum AS ENUM('user', 'bot')")
    
    # 컬럼 타입 변경 (assistant를 bot으로 변경)
    op.execute("ALTER TABLE messages ALTER COLUMN sender_type TYPE sender_type_enum USING (CASE WHEN sender_type = 'assistant' THEN 'bot'::sender_type_enum ELSE sender_type::text::sender_type_enum END)")
    
    # 새로운 enum 타입 삭제
    op.execute("DROP TYPE sender_type_enum_old")
