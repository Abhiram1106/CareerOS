from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


# ── Core auth ────────────────────────────────────────────────────────────────

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="student", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    profile = relationship("CareerProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    resumes = relationship("Resume", back_populates="user", cascade="all, delete-orphan")
    scans = relationship("ATSScan", back_populates="user", cascade="all, delete-orphan")


class SessionToken(Base):
    __tablename__ = "session_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    token: Mapped[str] = mapped_column(String(300), unique=True, index=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


# ── Institutional ─────────────────────────────────────────────────────────────

class College(Base):
    __tablename__ = "colleges"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    state: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    college_type: Mapped[str] = mapped_column(String(80), nullable=False, default="engineering")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    departments = relationship("Department", back_populates="college", cascade="all, delete-orphan")
    batches = relationship("Batch", back_populates="college", cascade="all, delete-orphan")


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    college_id: Mapped[int] = mapped_column(ForeignKey("colleges.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    college = relationship("College", back_populates="departments")
    batches = relationship("Batch", back_populates="department")


# ── Profile ───────────────────────────────────────────────────────────────────

class CareerProfile(Base):
    __tablename__ = "career_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    city: Mapped[str] = mapped_column(String(120), default="")
    professional_status: Mapped[str] = mapped_column(String(80), default="Fresher")
    target_role: Mapped[str] = mapped_column(String(120), default="Software Engineer")
    skills_csv: Mapped[str] = mapped_column(Text, default="")
    summary: Mapped[str] = mapped_column(Text, default="")
    experience_bullet: Mapped[str] = mapped_column(Text, default="")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="profile")


# ── Resume ────────────────────────────────────────────────────────────────────

class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    template_name: Mapped[str] = mapped_column(String(50), default="classic")
    content_text: Mapped[str] = mapped_column(Text, default="")
    file_uri: Mapped[str] = mapped_column(String(500), default="")
    source_format: Mapped[str] = mapped_column(String(10), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="resumes")
    sections = relationship("ResumeSection", back_populates="resume", cascade="all, delete-orphan")
    evidence = relationship("ResumeEvidence", back_populates="resume", cascade="all, delete-orphan")


class ResumeSection(Base):
    __tablename__ = "resume_sections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"), nullable=False, index=True)
    section_name: Mapped[str] = mapped_column(String(80), nullable=False)
    content_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    resume = relationship("Resume", back_populates="sections")


class ResumeEvidence(Base):
    __tablename__ = "resume_evidence"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"), nullable=False, index=True)
    claim_id: Mapped[str] = mapped_column(String(80), nullable=False)
    proof_uri: Mapped[str] = mapped_column(String(500), nullable=False, default="")
    verified_by: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    resume = relationship("Resume", back_populates="evidence")


class ResumeExportJob(Base):
    __tablename__ = "resume_export_jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(30), default="queued")
    file_path: Mapped[str] = mapped_column(String(500), default="")
    error_message: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ── JD + Scoring ─────────────────────────────────────────────────────────────

class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    college_id: Mapped[Optional[int]] = mapped_column(ForeignKey("colleges.id"), nullable=True, index=True)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    company: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    role: Mapped[str] = mapped_column(String(200), nullable=False)
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    skills_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    eligibility_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    scorecards = relationship("Scorecard", back_populates="jd")


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source: Mapped[str] = mapped_column(String(40), nullable=False, default="seed")
    external_id: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    company: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    location: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    skills_required: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    raw_jd_text: Mapped[str] = mapped_column(Text, nullable=False, default="")
    fetched_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    expires_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Scorecard(Base):
    __tablename__ = "scorecards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"), nullable=False, index=True)
    jd_id: Mapped[int] = mapped_column(ForeignKey("job_descriptions.id"), nullable=False, index=True)
    jd_match: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    ats_safety: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    evidence_quality: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    profile_completeness: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    interview_readiness: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    placement_hygiene: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    overall_score: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    bucket: Mapped[str] = mapped_column(String(20), nullable=False, default="high-risk")
    score_detail_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    jd = relationship("JobDescription", back_populates="scorecards")
    recommendations = relationship("Recommendation", back_populates="scorecard", cascade="all, delete-orphan")


class AgentRun(Base):
    __tablename__ = "agent_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"), nullable=False, index=True)
    job_id: Mapped[Optional[int]] = mapped_column(ForeignKey("jobs.id"), nullable=True, index=True)
    scorecard_id: Mapped[Optional[int]] = mapped_column(ForeignKey("scorecards.id"), nullable=True, index=True)
    current_step: Mapped[str] = mapped_column(String(40), nullable=False, default="INIT")
    summary_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="running")
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scorecard_id: Mapped[int] = mapped_column(ForeignKey("scorecards.id"), nullable=False, index=True)
    rec_type: Mapped[str] = mapped_column(String(40), nullable=False)
    section: Mapped[str] = mapped_column(String(80), nullable=False, default="")
    before_text: Mapped[str] = mapped_column(Text, nullable=False, default="")
    after_text: Mapped[str] = mapped_column(Text, nullable=False, default="")
    evidence_ids: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    accepted: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    scorecard = relationship("Scorecard", back_populates="recommendations")


# ── ATS Scan (legacy, kept for backward compat) ───────────────────────────────

class ATSScan(Base):
    __tablename__ = "ats_scans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    composite_score: Mapped[float] = mapped_column(Float, default=0)
    keyword_score: Mapped[float] = mapped_column(Float, default=0)
    format_score: Mapped[float] = mapped_column(Float, default=0)
    quality_score: Mapped[float] = mapped_column(Float, default=0)
    completeness_score: Mapped[float] = mapped_column(Float, default=0)
    contact_score: Mapped[float] = mapped_column(Float, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="scans")


# ── Cohort / Batch ────────────────────────────────────────────────────────────

class Batch(Base):
    __tablename__ = "batches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    college_id: Mapped[int] = mapped_column(ForeignKey("colleges.id"), nullable=False, index=True)
    dept_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True, index=True)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    grad_year: Mapped[int] = mapped_column(Integer, nullable=False, default=2026)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    college = relationship("College", back_populates="batches")
    department = relationship("Department", back_populates="batches")
    batch_resumes = relationship("BatchResume", back_populates="batch", cascade="all, delete-orphan")


class BatchResume(Base):
    __tablename__ = "batch_resumes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    batch_id: Mapped[int] = mapped_column(ForeignKey("batches.id"), nullable=False, index=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="uploaded")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint("batch_id", "resume_id", name="uq_batch_resume"),)

    batch = relationship("Batch", back_populates="batch_resumes")


# ── Audit + Intel ─────────────────────────────────────────────────────────────

class EventAudit(Base):
    __tablename__ = "events_audit"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    actor_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(80), nullable=False)
    target_type: Mapped[str] = mapped_column(String(40), nullable=False, default="")
    target_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    payload_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    ts: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)


class BenchmarkRun(Base):
    __tablename__ = "benchmark_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    workload: Mapped[str] = mapped_column(String(80), nullable=False)
    dataset_size: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    baseline_ms: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    intel_ms: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    throughput_rph: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    accuracy_delta: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    memory_mb: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    hw_label: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    notes: Mapped[str] = mapped_column(Text, nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
