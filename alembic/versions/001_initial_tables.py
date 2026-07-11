"""initial tables

Revision ID: 001_initial
Revises:
Create Date: 2026-07-12

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Users table
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("telegram_id", sa.BigInteger(), unique=True, nullable=False, index=True),
        sa.Column("username", sa.String(255), nullable=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("gender", sa.String(10), nullable=False),
        sa.Column("birth_date", sa.Date(), nullable=False),
        sa.Column("birth_time", sa.Time(), nullable=True),
        sa.Column("birth_city", sa.String(255), nullable=False),
        sa.Column("timezone", sa.String(50), server_default="UTC"),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.CheckConstraint("gender IN ('male', 'female')", name="valid_gender"),
    )
    op.create_index("idx_user_birth_date", "users", ["birth_date"])

    # Horoscopes table
    op.create_table(
        "horoscopes",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("date", sa.Date(), nullable=False, index=True),
        sa.Column("astronomy_json", sa.Text(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("status", sa.String(20), server_default="pending"),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("user_id", "date", name="unique_user_date"),
        sa.CheckConstraint(
            "status IN ('pending', 'sent', 'failed')", name="valid_status"
        ),
    )
    op.create_index("idx_horoscope_date_status", "horoscopes", ["date", "status"])

    # Subscriptions table
    op.create_table(
        "subscriptions",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("plan", sa.String(50), nullable=False),
        sa.Column("status", sa.String(20), server_default="active"),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.CheckConstraint("plan IN ('free', 'premium')", name="valid_plan"),
        sa.CheckConstraint(
            "status IN ('active', 'cancelled', 'expired')",
            name="valid_subscription_status",
        ),
    )


def downgrade() -> None:
    op.drop_table("subscriptions")
    op.drop_table("horoscopes")
    op.drop_index("idx_user_birth_date", table_name="users")
    op.drop_table("users")
