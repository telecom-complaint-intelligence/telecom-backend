"""merge heads

Revision ID: aedc82d5ccbd
Revises: 40810a7ae7a2, b7128d990142
Create Date: 2026-08-16 23:40:22.502204

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aedc82d5ccbd'
down_revision: Union[str, Sequence[str], None] = ('40810a7ae7a2', 'b7128d990142')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
