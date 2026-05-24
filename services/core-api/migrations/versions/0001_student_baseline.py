"""Student-only baseline schema.

Revision ID: 0001_student_baseline
Revises:
Create Date: 2026-05-24
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_student_baseline"
down_revision = None
branch_labels = None
depends_on = None

_JSON = sa.Text


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False, server_default="student"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_role", "users", ["role"])

    op.create_table(
        "session_tokens",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("token", sa.String(length=300), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )
    op.create_index("ix_session_tokens_token", "session_tokens", ["token"], unique=True)

    op.create_table(
        "career_profiles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("city", sa.String(length=120), nullable=False, server_default=""),
        sa.Column("professional_status", sa.String(length=80), nullable=False, server_default="Fresher"),
        sa.Column("target_role", sa.String(length=120), nullable=False, server_default="Software Engineer"),
        sa.Column("skills_csv", sa.Text(), nullable=False, server_default=""),
        sa.Column("summary", sa.Text(), nullable=False, server_default=""),
        sa.Column("experience_bullet", sa.Text(), nullable=False, server_default=""),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.UniqueConstraint("user_id"),
    )

    op.create_table(
        "resumes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("template_name", sa.String(length=50), nullable=False, server_default="classic"),
        sa.Column("content_text", sa.Text(), nullable=False, server_default=""),
        sa.Column("file_uri", sa.String(length=500), nullable=False, server_default=""),
        sa.Column("source_format", sa.String(length=10), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )

    op.create_table(
        "resume_sections",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("resume_id", sa.Integer(), sa.ForeignKey("resumes.id"), nullable=False, index=True),
        sa.Column("section_name", sa.String(80), nullable=False),
        sa.Column("content_json", _JSON, nullable=False, server_default="{}"),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "resume_evidence",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("resume_id", sa.Integer(), sa.ForeignKey("resumes.id"), nullable=False, index=True),
        sa.Column("claim_id", sa.String(80), nullable=False),
        sa.Column("proof_uri", sa.String(500), nullable=False, server_default=""),
        sa.Column("verified_by", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("status", sa.String(30), nullable=False, server_default="pending"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "ats_scans",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("composite_score", sa.Float(), nullable=False),
        sa.Column("keyword_score", sa.Float(), nullable=False),
        sa.Column("format_score", sa.Float(), nullable=False),
        sa.Column("quality_score", sa.Float(), nullable=False),
        sa.Column("completeness_score", sa.Float(), nullable=False),
        sa.Column("contact_score", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )

    op.create_table(
        "resume_export_jobs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("resume_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="queued"),
        sa.Column("file_path", sa.String(length=500), nullable=False, server_default=""),
        sa.Column("error_message", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["resume_id"], ["resumes.id"]),
    )

    op.create_table(
        "job_descriptions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("created_by", sa.Integer(), sa.ForeignKey("users.id"), nullable=False, index=True),
        sa.Column("company", sa.String(200), nullable=False),
        sa.Column("role", sa.String(200), nullable=False),
        sa.Column("raw_text", sa.Text(), nullable=False),
        sa.Column("skills_json", _JSON, nullable=False, server_default="[]"),
        sa.Column("eligibility_json", _JSON, nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_job_descriptions_company", "job_descriptions", ["company"])

    op.create_table(
        "scorecards",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("resume_id", sa.Integer(), sa.ForeignKey("resumes.id"), nullable=False, index=True),
        sa.Column("jd_id", sa.Integer(), sa.ForeignKey("job_descriptions.id"), nullable=False, index=True),
        sa.Column("jd_match", sa.Float(), nullable=False, server_default="0"),
        sa.Column("ats_safety", sa.Float(), nullable=False, server_default="0"),
        sa.Column("evidence_quality", sa.Float(), nullable=False, server_default="0"),
        sa.Column("profile_completeness", sa.Float(), nullable=False, server_default="0"),
        sa.Column("interview_readiness", sa.Float(), nullable=False, server_default="0"),
        sa.Column("placement_hygiene", sa.Float(), nullable=False, server_default="0"),
        sa.Column("overall_score", sa.Float(), nullable=False, server_default="0"),
        sa.Column("bucket", sa.String(20), nullable=False, server_default="high-risk"),
        sa.Column("score_detail_json", _JSON, nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "recommendations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("scorecard_id", sa.Integer(), sa.ForeignKey("scorecards.id"), nullable=False, index=True),
        sa.Column("rec_type", sa.String(40), nullable=False),
        sa.Column("section", sa.String(80), nullable=False, server_default=""),
        sa.Column("before_text", sa.Text(), nullable=False, server_default=""),
        sa.Column("after_text", sa.Text(), nullable=False, server_default=""),
        sa.Column("evidence_ids", _JSON, nullable=False, server_default="[]"),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="0"),
        sa.Column("accepted", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

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
        sa.Column("summary_json", _JSON, nullable=False, server_default="{}"),
        sa.Column("status", sa.String(30), nullable=False, server_default="running"),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("finished_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_agent_runs_student_id", "agent_runs", ["student_id"])
    op.create_index("ix_agent_runs_resume_id", "agent_runs", ["resume_id"])
    op.create_index("ix_agent_runs_job_id", "agent_runs", ["job_id"])
    op.create_index("ix_agent_runs_scorecard_id", "agent_runs", ["scorecard_id"])

    op.create_table(
        "events_audit",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("actor_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False, index=True),
        sa.Column("action", sa.String(80), nullable=False),
        sa.Column("target_type", sa.String(40), nullable=False, server_default=""),
        sa.Column("target_id", sa.Integer(), nullable=True),
        sa.Column("payload_json", _JSON, nullable=False, server_default="{}"),
        sa.Column("ts", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_events_audit_actor_ts", "events_audit", ["actor_id", "ts"])

    op.create_table(
        "benchmark_runs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("workload", sa.String(80), nullable=False),
        sa.Column("dataset_size", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("baseline_ms", sa.Float(), nullable=False, server_default="0"),
        sa.Column("intel_ms", sa.Float(), nullable=False, server_default="0"),
        sa.Column("throughput_rph", sa.Float(), nullable=False, server_default="0"),
        sa.Column("accuracy_delta", sa.Float(), nullable=False, server_default="0"),
        sa.Column("memory_mb", sa.Float(), nullable=False, server_default="0"),
        sa.Column("hw_label", sa.String(120), nullable=False, server_default=""),
        sa.Column("notes", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("benchmark_runs")
    op.drop_table("events_audit")
    op.drop_index("ix_agent_runs_scorecard_id", table_name="agent_runs")
    op.drop_index("ix_agent_runs_job_id", table_name="agent_runs")
    op.drop_index("ix_agent_runs_resume_id", table_name="agent_runs")
    op.drop_index("ix_agent_runs_student_id", table_name="agent_runs")
    op.drop_table("agent_runs")
    op.drop_index("ix_jobs_external_id", table_name="jobs")
    op.drop_table("jobs")
    op.drop_table("recommendations")
    op.drop_table("scorecards")
    op.drop_index("ix_job_descriptions_company", table_name="job_descriptions")
    op.drop_table("job_descriptions")
    op.drop_table("resume_export_jobs")
    op.drop_table("ats_scans")
    op.drop_table("resume_evidence")
    op.drop_table("resume_sections")
    op.drop_table("resumes")
    op.drop_table("career_profiles")
    op.drop_index("ix_session_tokens_token", table_name="session_tokens")
    op.drop_table("session_tokens")
    op.drop_index("ix_users_role", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
