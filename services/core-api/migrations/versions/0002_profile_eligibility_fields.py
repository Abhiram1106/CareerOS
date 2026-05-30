"""Add eligibility fields to career_profiles.

Revision ID: 0002_profile_eligibility_fields
Revises: 0001_student_baseline
Create Date: 2026-05-30
"""

from alembic import op
import sqlalchemy as sa

revision = "0002_profile_eligibility_fields"
down_revision = "0001_student_baseline"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("career_profiles", sa.Column("cgpa", sa.Float(), nullable=True))
    op.add_column("career_profiles", sa.Column("active_backlogs", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("career_profiles", sa.Column("branch", sa.String(length=80), nullable=False, server_default=""))
    op.add_column("career_profiles", sa.Column("grad_year", sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column("career_profiles", "grad_year")
    op.drop_column("career_profiles", "branch")
    op.drop_column("career_profiles", "active_backlogs")
    op.drop_column("career_profiles", "cgpa")
