"""baseline users schema

Revision ID: aa55df750f10
Revises: 
Create Date: 2026-09-25 18:46:24.598494

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = 'aa55df750f10'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the Guide 9 users table only when it is not already present."""
    if "users" not in inspect(op.get_bind()).get_table_names():
        op.create_table(
            "users",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("name", sa.String(length=100), nullable=False),
            sa.Column("email", sa.String(length=320), nullable=False),
            sa.Column("role", sa.String(length=20), nullable=False),
            sa.Column("is_active", sa.Boolean(), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.CheckConstraint(
                "role IN ('admin', 'support', 'user')",
                name="ck_users_role",
            ),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index("ix_users_email", "users", ["email"], unique=True)
        op.create_index("ix_users_id", "users", ["id"], unique=False)


def downgrade() -> None:
    """Keep users as the Guide 9 baseline; later revisions own new tables."""
    pass
