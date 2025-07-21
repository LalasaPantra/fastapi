"""create posts table

Revision ID: da74712fd8a1
Revises:
Create Date: 2025-07-17 21:53:16.137000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "da74712fd8a1"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("title", sa.String, nullable=False, unique=True),
        sa.Column("subtitle", sa.String, nullable=False),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("img_url", sa.String, nullable=False),
        sa.Column("created_at", sa.String, nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("posts")
