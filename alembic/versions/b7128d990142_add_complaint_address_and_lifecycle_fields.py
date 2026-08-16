"""add complaint_address and complaint lifecycle fields

Revision ID: b7128d990142
Revises: 9a011ef9321c
Create Date: 2026-08-16 20:21:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b7128d990142"
down_revision: str | None = "9a011ef9321c"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    # 1. Alter complaints table
    op.add_column("complaints", sa.Column("complaint1", sa.Text(), nullable=True))
    op.add_column("complaints", sa.Column("response", sa.Text(), nullable=True))
    op.add_column("complaints", sa.Column("complaint2", sa.Text(), nullable=True))
    op.add_column(
        "complaints",
        sa.Column(
            "filling_on_behalf_of", sa.Boolean(), server_default="false", nullable=False
        ),
    )
    op.add_column(
        "complaints",
        sa.Column(
            "timestamp", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
    )
    op.add_column(
        "complaints", sa.Column("closing_time_stamp", sa.DateTime(), nullable=True)
    )

    # 2. Create complaint_address table
    op.create_table(
        "complaint_address",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("complaint_id", sa.String(length=36), nullable=False),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("city", sa.String(length=100), nullable=True),
        sa.Column("state", sa.String(length=100), nullable=True),
        sa.Column(
            "country", sa.String(length=100), server_default="India", nullable=False
        ),
        sa.Column("zipcode", sa.String(length=20), nullable=True),
        sa.ForeignKeyConstraint(
            ["complaint_id"], ["complaints.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_complaint_address_complaint_id"),
        "complaint_address",
        ["complaint_id"],
        unique=True,
    )
    op.create_index(
        op.f("ix_complaint_address_id"), "complaint_address", ["id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_complaint_address_id"), table_name="complaint_address")
    op.drop_index(
        op.f("ix_complaint_address_complaint_id"), table_name="complaint_address"
    )
    op.drop_table("complaint_address")

    op.drop_column("complaints", "closing_time_stamp")
    op.drop_column("complaints", "timestamp")
    op.drop_column("complaints", "filling_on_behalf_of")
    op.drop_column("complaints", "complaint2")
    op.drop_column("complaints", "response")
    op.drop_column("complaints", "complaint1")
