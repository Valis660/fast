"""make email unique

Revision ID: c0d52701f315
Revises: 406d765ffc07
Create Date: 2025-06-05 14:35:59.075250

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c0d52701f315"
down_revision: Union[str, None] = "406d765ffc07"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "users", type_="unique")
