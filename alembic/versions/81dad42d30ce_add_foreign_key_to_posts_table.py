"""add foreign key to posts table

Revision ID: 81dad42d30ce
Revises: 0869686181af
Create Date: 2025-07-17 22:11:47.585709

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "81dad42d30ce"
down_revision: Union[str, Sequence[str], None] = "0869686181af"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "posts",
        sa.Column(
            "author_id",
            sa.Integer,
            nullable=False,
        ),
    )
    op.create_foreign_key(
        "fk_posts_author_id_users",
        "posts",
        "users",
        ["author_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("fk_posts_author_id_users", "posts", type_="foreignkey")
    op.drop_column("posts", "author_id")
