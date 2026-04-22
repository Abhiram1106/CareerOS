"""add alert notifications

Revision ID: 0002_alert_notifications
Revises: 0001_initial
Create Date: 2026-04-21
"""

from alembic import op
import sqlalchemy as sa


revision = "0002_alert_notifications"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "alert_notifications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("alert_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("is_read", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["alert_id"], ["job_alerts.id"]),
    )


def downgrade() -> None:
    op.drop_table("alert_notifications")
