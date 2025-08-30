"""initial

Revision ID: 0e9c7928a5d8
Revises: 
Create Date: 2025-08-30 14:15:40.967980
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '0e9c7928a5d8'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('full_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('disabled', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)

    op.create_table(
        'event',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('ts', sa.DateTime(), nullable=False),
        sa.Column('source', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('url', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('title', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('duration_sec', sa.Integer(), nullable=False),
        sa.Column('category', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('subcategory', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('productive_score', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_event_ts'), 'event', ['ts'], unique=False)
    op.create_index(op.f('ix_event_user_id'), 'event', ['user_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_event_user_id'), table_name='event')
    op.drop_index(op.f('ix_event_ts'), table_name='event')
    op.drop_table('event')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
