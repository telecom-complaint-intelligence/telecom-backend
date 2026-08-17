"""merge heads

Revision ID: aedc82d5ccbd
Revises: 40810a7ae7a2, b7128d990142
Create Date: 2026-08-16 23:40:22.502204

"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "aedc82d5ccbd"
down_revision: str | Sequence[str] | None = ("40810a7ae7a2", "b7128d990142")
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""


def downgrade() -> None:
    """Downgrade schema."""
