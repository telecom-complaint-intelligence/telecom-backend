"""split complaints into three normalized tables with solution_a

Revision ID: 9a011ef9321c
Revises: 8cbcf838420b
Create Date: 2026-08-16 19:02:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9a011ef9321c"
down_revision: str | None = "8cbcf838420b"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    # 1. Drop old columns from complaints if they exist
    with op.batch_alter_table("complaints", schema=None) as batch_op:
        for col in [
            "category_confidence",
            "negativity_score",
            "sentiment_score",
            "technical_information",
            "complexity",
            "complexity_score",
            "weighted_complexity_score",
            "weighted_negativity_score",
            "total_complexity_score",
        ]:
            try:
                batch_op.drop_column(col)
            except Exception:  # noqa: BLE001, S110
                pass

    # 2. Create complaint_ai_analysis table (including solution_a)
    op.create_table(
        "complaint_ai_analysis",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("complaint_id", sa.String(length=36), nullable=False),
        sa.Column("category_confidence", sa.Float(), nullable=True),
        sa.Column("negativity_score", sa.Float(), nullable=True),
        sa.Column("sentiment_score", sa.Float(), nullable=True),
        sa.Column("component", sa.JSON(), nullable=True),
        sa.Column("failure_type", sa.JSON(), nullable=True),
        sa.Column("scope", sa.String(length=50), nullable=True),
        sa.Column("service_impact", sa.String(length=50), nullable=True),
        sa.Column("duration_hours", sa.Float(), nullable=True),
        sa.Column("occurrence_pattern", sa.String(length=50), nullable=True),
        sa.Column("solution_a", sa.Text(), nullable=True),
        sa.Column("extraction_source", sa.String(length=50), nullable=True),
        sa.Column("lowest_confidence", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["complaint_id"], ["complaints.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_complaint_ai_analysis_complaint_id"),
        "complaint_ai_analysis",
        ["complaint_id"],
        unique=True,
    )
    op.create_index(
        op.f("ix_complaint_ai_analysis_id"),
        "complaint_ai_analysis",
        ["id"],
        unique=False,
    )

    # 3. Create complaint_priority_scores table
    op.create_table(
        "complaint_priority_scores",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("complaint_id", sa.String(length=36), nullable=False),
        sa.Column("complexity", sa.String(length=50), nullable=False),
        sa.Column("complexity_score", sa.Integer(), nullable=False),
        sa.Column("weighted_complexity_score", sa.Float(), nullable=False),
        sa.Column("weighted_negativity_score", sa.Float(), nullable=False),
        sa.Column("total_complexity_score", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["complaint_id"], ["complaints.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_complaint_priority_scores_complaint_id"),
        "complaint_priority_scores",
        ["complaint_id"],
        unique=True,
    )
    op.create_index(
        op.f("ix_complaint_priority_scores_id"),
        "complaint_priority_scores",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_complaint_priority_scores_id"), table_name="complaint_priority_scores"
    )
    op.drop_index(
        op.f("ix_complaint_priority_scores_complaint_id"),
        table_name="complaint_priority_scores",
    )
    op.drop_table("complaint_priority_scores")

    op.drop_index(
        op.f("ix_complaint_ai_analysis_id"), table_name="complaint_ai_analysis"
    )
    op.drop_index(
        op.f("ix_complaint_ai_analysis_complaint_id"),
        table_name="complaint_ai_analysis",
    )
    op.drop_table("complaint_ai_analysis")
