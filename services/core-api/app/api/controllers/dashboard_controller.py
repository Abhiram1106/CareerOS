from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ...database import get_db
from ...dependencies import get_dashboard_query_service, require_student
from ...models.entities import Resume, Scorecard, User
from ...modules.dashboard.query.dashboard_query_service import DashboardQueryService
from ...services.clients import vector_similar_resumes

from careeros_scoring import classify_resume_quality

router = APIRouter()


@router.get("/dashboard")
def dashboard(
    user: User = Depends(require_student),
    service: DashboardQueryService = Depends(get_dashboard_query_service),
):
    return service.get_for_user(user).model_dump()


@router.get("/analytics/score-history")
def score_history(
    user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    """Return the user's scorecard history newest-first (up to 50 entries)."""
    rows = (
        db.query(
            Scorecard.id, Scorecard.overall_score, Scorecard.bucket,
            Scorecard.ats_safety, Scorecard.evidence_quality,
            Scorecard.profile_completeness, Scorecard.jd_match,
            Scorecard.created_at,
        )
        .join(Resume, Resume.id == Scorecard.resume_id)
        .filter(Resume.user_id == user.id)
        .order_by(Scorecard.created_at.asc())
        .limit(50)
        .all()
    )

    # Derive quality_class for each historical scorecard
    history = []
    for i, r in enumerate(rows):
        qc = classify_resume_quality(
            overall_score=r.overall_score,
            ats_parse_safety=getattr(r, "ats_safety", 0) or 0,
            jd_match=getattr(r, "jd_match", 0) or 0,
            evidence_quality=getattr(r, "evidence_quality", 0) or 0,
            profile_completeness=getattr(r, "profile_completeness", 0) or 0,
            required_skill_recall=50.0,  # not stored per-scan; use neutral default
        )
        history.append({
            "scorecard_id": r.id,
            "version": i + 1,
            "overall_score": round(r.overall_score, 1),
            "bucket": r.bucket,
            "quality_class": qc,
            "date": r.created_at.strftime("%Y-%m-%d"),
            "timestamp": r.created_at.isoformat(),
        })
    # Compute delta from first to last
    delta = None
    if len(history) >= 2:
        delta = round(history[-1]["overall_score"] - history[0]["overall_score"], 1)

    return {"history": history, "delta": delta, "total": len(history)}


@router.get("/analytics/similar-resumes")
async def similar_resumes(
    role_family: str = Query(default="", description="Role family: backend, frontend, data, devops"),
    n: int = Query(default=3, ge=1, le=10),
    user: User = Depends(require_student),
):
    """Retrieve similar Interview Ready resumes from the CARE-RAG knowledge base.
    Used by the wizard Step 2 (Compare) to show real patterns instead of static examples.
    """
    # Use the student's latest resume text as query context (best available)
    # For now, query by role family without text — patterns are returned by role
    result = await vector_similar_resumes(
        query_text=f"Interview Ready {role_family} software engineer resume with strong technical skills",
        role_family=role_family,
        n_results=n,
    )
    return result
