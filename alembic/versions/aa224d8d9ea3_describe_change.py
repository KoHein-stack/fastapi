"""describe  change

Revision ID: aa224d8d9ea3
Revises: 8f4443015c02
Create Date: 2026-05-21 01:50:14.592962

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa224d8d9ea3'
down_revision: Union[str, Sequence[str], None] = '8f4443015c02'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("published", sa.Boolean(), server_default=sa.text("true"), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "published")
    pass
