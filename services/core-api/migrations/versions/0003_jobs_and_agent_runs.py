"""Add jobs feed cache table and agent run tracking.

Revision ID: 0003_jobs_and_agent_runs
Revises: 0002_campus_ai_schema
Create Date: 2026-05-23
"""

from alembic import op
import sqlalchemy as sa

revision = "0003_jobs_and_agent_runs"
down_revision = "0002_campus_ai_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "jobs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("source", sa.String(40), nullable=False, server_default="seed"),
        sa.Column("external_id", sa.String(200), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("company", sa.String(255), nullable=False, server_default=""),
        sa.Column("location", sa.String(255), nullable=False, server_default=""),
        sa.Column("skills_required", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("raw_jd_text", sa.Text(), nullable=False, server_default=""),
        sa.Column("fetched_at", sa.DateTime(), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_jobs_external_id", "jobs", ["external_id"])

    op.create_table(
        "agent_runs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("student_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("resume_id", sa.Integer(), sa.ForeignKey("resumes.id"), nullable=False),
        sa.Column("job_id", sa.Integer(), sa.ForeignKey("jobs.id"), nullable=True),
        sa.Column("scorecard_id", sa.Integer(), sa.ForeignKey("scorecards.id"), nullable=True),
        sa.Column("current_step", sa.String(40), nullable=False, server_default="INIT"),
        sa.Column("summary_json", sa.Text(), nullable=False, server_default="{}"),
        sa.Column("status", sa.String(30), nullable=False, server_default="running"),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("finished_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_agent_runs_student_id", "agent_runs", ["student_id"])
    op.create_index("ix_agent_runs_resume_id", "agent_runs", ["resume_id"])
    op.create_index("ix_agent_runs_job_id", "agent_runs", ["job_id"])
    op.create_index("ix_agent_runs_scorecard_id", "agent_runs", ["scorecard_id"])


def downgrade() -> None:
    op.drop_index("ix_agent_runs_scorecard_id", table_name="agent_runs")
    op.drop_index("ix_agent_runs_job_id", table_name="agent_runs")
    op.drop_index("ix_agent_runs_resume_id", table_name="agent_runs")
    op.drop_index("ix_agent_runs_student_id", table_name="agent_runs")
    op.drop_table("agent_runs")
    op.drop_index("ix_jobs_external_id", table_name="jobs")
    op.drop_table("jobs")
