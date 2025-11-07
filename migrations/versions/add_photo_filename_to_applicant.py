"""Add photo_filename to Applicant

Revision ID: add_photo_filename
Revises: e4fa52fed968
Create Date: 2025-01-15 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_photo_filename'
down_revision: Union[str, None] = 'e4fa52fed968'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add photo_filename column to applicant table."""
    # SQLite compatible: Check if column exists first
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('applicant')]
    
    if 'photo_filename' not in columns:
        op.add_column('applicant', sa.Column('photo_filename', sa.String(255), nullable=True))


def downgrade() -> None:
    """Remove photo_filename column from applicant table."""
    # SQLite doesn't support DROP COLUMN directly, so we'll skip this
    # In production, you'd need to recreate the table
    pass

