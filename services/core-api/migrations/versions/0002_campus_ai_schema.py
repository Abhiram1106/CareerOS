"""Campus AI schema — colleges, departments, resume sections, scoring, batches, audit

Revision ID: 0002_campus_ai_schema
Revises: 0001_initial
Create Date: 2026-05-20
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0002_campus_ai_schema"
down_revision = "0001_initial"
branch_labels = None
depends_on = None

# Use Text for jsonb-compatible columns (works on both Postgres and SQLite dev)
_JSON = sa.Text


def upgrade() -> None:
    # ── users: add role column ──────────────────────────────────────────────
    op.add_column("users", sa.Column("role", sa.String(20), nullable=False, server_default="student"))
    op.create_index("ix_users_role", "users", ["role"])

    # ── colleges ───────────────────────────────────────────────────────────
    op.create_table(
        "colleges",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("state", sa.String(120), nullable=False, server_default=""),
        sa.Column("college_type", sa.String(80), nullable=False, server_default="engineering"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_colleges_name", "colleges", ["name"])

    # ── departments ────────────────────────────────────────────────────────
    op.create_table(
        "departments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("college_id", sa.Integer(), sa.ForeignKey("colleges.id"), nullable=False, index=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    # ── resume_sections ────────────────────────────────────────────────────
    op.create_table(
        "resume_sections",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("resume_id", sa.Integer(), sa.ForeignKey("resumes.id"), nullable=False, index=True),
        sa.Column("section_name", sa.String(80), nullable=False),
        sa.Column("content_json", _JSON, nullable=False, server_default="{}"),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    # ── resume_evidence ────────────────────────────────────────────────────
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

    # ── job_descriptions ───────────────────────────────────────────────────
    op.create_table(
        "job_descriptions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("college_id", sa.Integer(), sa.ForeignKey("colleges.id"), nullable=True, index=True),
        sa.Column("created_by", sa.Integer(), sa.ForeignKey("users.id"), nullable=False, index=True),
        sa.Column("company", sa.String(200), nullable=False),
        sa.Column("role", sa.String(200), nullable=False),
        sa.Column("raw_text", sa.Text(), nullable=False),
        sa.Column("skills_json", _JSON, nullable=False, server_default="[]"),
        sa.Column("eligibility_json", _JSON, nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_job_descriptions_company", "job_descriptions", ["company"])

    # ── scorecards ─────────────────────────────────────────────────────────
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

    # ── recommendations (rewriter output) ─────────────────────────────────
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

    # ── batches ────────────────────────────────────────────────────────────
    op.create_table(
        "batches",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("college_id", sa.Integer(), sa.ForeignKey("colleges.id"), nullable=False, index=True),
        sa.Column("dept_id", sa.Integer(), sa.ForeignKey("departments.id"), nullable=True, index=True),
        sa.Column("created_by", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("grad_year", sa.Integer(), nullable=False, server_default="2026"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_batches_college_year", "batches", ["college_id", "grad_year"])

    # ── batch_resumes (join) ───────────────────────────────────────────────
    op.create_table(
        "batch_resumes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("batch_id", sa.Integer(), sa.ForeignKey("batches.id"), nullable=False, index=True),
        sa.Column("resume_id", sa.Integer(), sa.ForeignKey("resumes.id"), nullable=False, index=True),
        sa.Column("status", sa.String(30), nullable=False, server_default="uploaded"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("batch_id", "resume_id", name="uq_batch_resume"),
    )

    # ── events_audit ───────────────────────────────────────────────────────
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

    # ── benchmark_runs (Intel Lab) ─────────────────────────────────────────
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
    op.drop_table("batch_resumes")
    op.drop_table("batches")
    op.drop_table("recommendations")
    op.drop_table("scorecards")
    op.drop_table("job_descriptions")
    op.drop_table("resume_evidence")
    op.drop_table("resume_sections")
    op.drop_table("departments")
    op.drop_table("colleges")
    op.drop_index("ix_users_role", table_name="users")
    op.drop_column("users", "role")
