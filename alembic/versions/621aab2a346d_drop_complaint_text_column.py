"""drop complaint_text column

Revision ID: 621aab2a346d
Revises: 1b7ff8ac01a0
Create Date: 2026-08-18 21:37:35.218013

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '621aab2a346d'
down_revision: Union[str, Sequence[str], None] = '1b7ff8ac01a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column('complaints', 'complaint_text')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('complaints', sa.Column('complaint_text', sa.Text(), nullable=True))
