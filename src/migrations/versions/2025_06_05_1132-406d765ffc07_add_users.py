"""add users

Revision ID: 406d765ffc07
Revises: 02b1fe912137
Create Date: 2025-06-05 11:32:12.578678

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "406d765ffc07"
down_revision: Union[str, None] = "02b1fe912137"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
