"""add complaints table with ai features

Revision ID: 8cbcf838420b
Revises: 39db37721a51
Create Date: 2026-08-16 09:32:49.592834

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '8cbcf838420b'
down_revision: Union[str, Sequence[str], None] = '39db37721a51'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        'complaints',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('ticket_number', sa.String(length=50), nullable=True),
        sa.Column('user_id', sa.String(length=36), nullable=True),
        sa.Column('complaint_text', sa.Text(), nullable=False),
        sa.Column('received_via', sa.String(), nullable=True),
        sa.Column('city', sa.String(), nullable=True),
        sa.Column('state', sa.String(), nullable=True),
        sa.Column('zip_code', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=False, server_default='OPEN'),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('category_confidence', sa.Float(), nullable=True),
        sa.Column('negativity_score', sa.Float(), nullable=True),
        sa.Column('sentiment_score', sa.Float(), nullable=True),
        sa.Column('technical_information', sa.JSON(), nullable=True),
        sa.Column('complexity', sa.String(), nullable=True),
        sa.Column('complexity_score', sa.Integer(), nullable=True),
        sa.Column('weighted_complexity_score', sa.Float(), nullable=True),
        sa.Column('weighted_negativity_score', sa.Float(), nullable=True),
        sa.Column('total_complexity_score', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_complaints_id'), 'complaints', ['id'], unique=False)
    op.create_index(op.f('ix_complaints_ticket_number'), 'complaints', ['ticket_number'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_complaints_ticket_number'), table_name='complaints')
    op.drop_index(op.f('ix_complaints_id'), table_name='complaints')
    op.drop_table('complaints')
