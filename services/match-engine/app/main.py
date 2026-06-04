from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

from .intel_patch import patch_sklearn_if_available

patch_sklearn_if_available()

from .jd_parser import parse_jd
from .matcher import compute_match
from .vector_store import (
    get_index_stats,
    index_jd,
    index_resume_pattern,
    retrieve_similar_resumes,
    store_user_signal,
)

app = FastAPI(title="CareerOS Match Engine", version="0.1.0")


class ParseJdRequest(BaseModel):
    jd_text: str = Field(min_length=20)


class MatchRequest(BaseModel):
    resume_text: str = Field(min_length=10)
    jd_text: str = Field(min_length=20)
    required_skills: list[str] = Field(default_factory=list)
    student_profile: dict | None = None


# ── CARE-RAG vector store request models ────────────────────────────────────

class IndexResumeRequest(BaseModel):
    resume_id: int
    user_id: int
    resume_text: str = Field(min_length=10)
    role_family: str = ""
    quality_class: str = "interview_ready"
    overall_score: float = 0.0
    evidence_score: float = 0.0


class RetrieveSimilarRequest(BaseModel):
    query_text: str = Field(min_length=10)
    role_family: str = ""
    n_results: int = Field(default=5, ge=1, le=20)
    min_score: float = Field(default=65.0, ge=0.0, le=100.0)


class IndexJdRequest(BaseModel):
    jd_id: int
    jd_text: str = Field(min_length=20)
    role: str = ""
    required_skills: list[str] = Field(default_factory=list)


class UserSignalRequest(BaseModel):
    user_id: int
    signal_type: str   # suggestion_accepted | suggestion_rejected | interview_received
    scorecard_id: int
    content: str = Field(min_length=1)


# ── Core routes ─────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok", "service": "match-engine"}


@app.post("/jd/parse")
def jd_parse(payload: ParseJdRequest):
    return parse_jd(payload.jd_text)


@app.post("/match")
def match(payload: MatchRequest):
    parsed = parse_jd(payload.jd_text)
    required = payload.required_skills or parsed.get("required_skills", [])
    jd_eligibility = parsed.get("eligibility")
    return compute_match(
        payload.resume_text,
        payload.jd_text,
        required,
        payload.student_profile,
        jd_eligibility,
    )


# ── CARE-RAG vector store routes ─────────────────────────────────────────────

@app.get("/vector/stats")
def vector_stats():
    """Collection counts for each CARE-RAG index."""
    return get_index_stats()


@app.post("/vector/index-resume")
def vector_index_resume(payload: IndexResumeRequest):
    """Index an Interview Ready resume into the Resume Pattern Index."""
    ok = index_resume_pattern(
        resume_id=payload.resume_id,
        user_id=payload.user_id,
        resume_text=payload.resume_text,
        role_family=payload.role_family,
        quality_class=payload.quality_class,
        overall_score=payload.overall_score,
        evidence_score=payload.evidence_score,
    )
    return {"ok": ok, "resume_id": payload.resume_id}


@app.post("/vector/similar-resumes")
def vector_similar_resumes(payload: RetrieveSimilarRequest):
    """Retrieve top-N similar Interview Ready resumes."""
    patterns = retrieve_similar_resumes(
        query_text=payload.query_text,
        role_family=payload.role_family,
        n_results=payload.n_results,
        min_score=payload.min_score,
    )
    return {
        "patterns": patterns,
        "count": len(patterns),
        "source": "care_rag_resume_patterns",
    }


@app.post("/vector/index-jd")
def vector_index_jd(payload: IndexJdRequest):
    """Index a parsed JD into the JD Intelligence Index."""
    ok = index_jd(
        jd_id=payload.jd_id,
        jd_text=payload.jd_text,
        role=payload.role,
        required_skills=payload.required_skills,
    )
    return {"ok": ok, "jd_id": payload.jd_id}


@app.post("/vector/user-signal")
def vector_user_signal(payload: UserSignalRequest):
    """Log a user outcome signal (accepted suggestion, interview received, etc.)."""
    ok = store_user_signal(
        user_id=payload.user_id,
        signal_type=payload.signal_type,
        scorecard_id=payload.scorecard_id,
        content=payload.content,
    )
    return {"ok": ok}
