"""Add structured career profile sections and user social links.

Revision ID: 0003_structured_profile
Revises: 0002_profile_eligibility_fields
Create Date: 2026-05-31
"""

from alembic import op
import sqlalchemy as sa

revision = "0003_structured_profile"
down_revision = "0002_profile_eligibility_fields"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Extend users with social links
    op.add_column("users", sa.Column("phone", sa.String(20), nullable=False, server_default=""))
    op.add_column("users", sa.Column("linkedin_url", sa.String(300), nullable=False, server_default=""))
    op.add_column("users", sa.Column("github_url", sa.String(300), nullable=False, server_default=""))
    op.add_column("users", sa.Column("portfolio_url", sa.String(300), nullable=False, server_default=""))

    op.create_table(
        "work_experiences",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("company", sa.String(200), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("employment_type", sa.String(50), nullable=False, server_default="Full-time"),
        sa.Column("location", sa.String(200), nullable=False, server_default=""),
        sa.Column("start_date", sa.String(20), nullable=False),
        sa.Column("end_date", sa.String(20), nullable=False, server_default=""),
        sa.Column("is_current", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("bullets", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_work_experiences_user_id", "work_experiences", ["user_id"])

    op.create_table(
        "educations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("institution", sa.String(300), nullable=False),
        sa.Column("degree", sa.String(200), nullable=False),
        sa.Column("field", sa.String(200), nullable=False),
        sa.Column("start_year", sa.Integer(), nullable=True),
        sa.Column("end_year", sa.Integer(), nullable=True),
        sa.Column("cgpa", sa.Float(), nullable=True),
        sa.Column("percentage", sa.Float(), nullable=True),
        sa.Column("coursework", sa.Text(), nullable=False, server_default=""),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_educations_user_id", "educations", ["user_id"])

    op.create_table(
        "skills",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("category", sa.String(50), nullable=False, server_default="technical"),
        sa.Column("proficiency", sa.String(30), nullable=False, server_default="intermediate"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_skills_user_id", "skills", ["user_id"])

    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("tech_stack", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("github_url", sa.String(300), nullable=False, server_default=""),
        sa.Column("live_url", sa.String(300), nullable=False, server_default=""),
        sa.Column("start_date", sa.String(20), nullable=False, server_default=""),
        sa.Column("end_date", sa.String(20), nullable=False, server_default=""),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_projects_user_id", "projects", ["user_id"])

    op.create_table(
        "certifications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("issuer", sa.String(200), nullable=False),
        sa.Column("issue_date", sa.String(20), nullable=False, server_default=""),
        sa.Column("expiry_date", sa.String(20), nullable=False, server_default=""),
        sa.Column("credential_id", sa.String(200), nullable=False, server_default=""),
        sa.Column("credential_url", sa.String(300), nullable=False, server_default=""),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_certifications_user_id", "certifications", ["user_id"])

    op.create_table(
        "job_applications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("job_external_id", sa.String(200), nullable=False),
        sa.Column("job_title", sa.String(255), nullable=False, server_default=""),
        sa.Column("company", sa.String(255), nullable=False, server_default=""),
        sa.Column("apply_url", sa.String(500), nullable=False, server_default=""),
        sa.Column("status", sa.String(30), nullable=False, server_default="saved"),
        sa.Column("resume_id", sa.Integer(), sa.ForeignKey("resumes.id"), nullable=True),
        sa.Column("notes", sa.Text(), nullable=False, server_default=""),
        sa.Column("applied_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_job_applications_user_id", "job_applications", ["user_id"])


def downgrade() -> None:
    op.drop_table("job_applications")
    op.drop_table("certifications")
    op.drop_table("projects")
    op.drop_table("skills")
    op.drop_table("educations")
    op.drop_table("work_experiences")
    op.drop_column("users", "portfolio_url")
    op.drop_column("users", "github_url")
    op.drop_column("users", "linkedin_url")
    op.drop_column("users", "phone")
