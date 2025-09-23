"""init

Revision ID: 0001
Revises: 
Create Date: 2025-09-15

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("username", sa.String(length=100), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=10), nullable=False, server_default="user"),
    )
    op.create_index("ix_users_id", "users", ["id"], unique=False)
    op.create_index("ix_users_username", "users", ["username"], unique=True)

    op.create_table(
        "measurements",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("ph", sa.Float(), nullable=False),
        sa.Column("ec", sa.Float(), nullable=False),
        sa.Column("oxygen", sa.Float(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_measurements_id", "measurements", ["id"], unique=False)
    op.create_index("ix_measurements_user_id", "measurements", ["user_id"], unique=False)
    op.create_index("ix_measurements_timestamp", "measurements", ["timestamp"], unique=False)

    op.create_table(
        "thresholds",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("ph_min", sa.Float(), nullable=False),
        sa.Column("ph_max", sa.Float(), nullable=False),
        sa.Column("ec_min", sa.Float(), nullable=False),
        sa.Column("ec_max", sa.Float(), nullable=False),
        sa.Column("oxygen_min", sa.Float(), nullable=False),
        sa.Column("oxygen_max", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="SET NULL"),
    )
    op.create_index("ix_thresholds_id", "thresholds", ["id"], unique=False)
    op.create_index("ix_thresholds_user_id", "thresholds", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_thresholds_user_id", table_name="thresholds")
    op.drop_index("ix_thresholds_id", table_name="thresholds")
    op.drop_table("thresholds")

    op.drop_index("ix_measurements_timestamp", table_name="measurements")
    op.drop_index("ix_measurements_user_id", table_name="measurements")
    op.drop_index("ix_measurements_id", table_name="measurements")
    op.drop_table("measurements")

    op.drop_index("ix_users_username", table_name="users")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_table("users")



