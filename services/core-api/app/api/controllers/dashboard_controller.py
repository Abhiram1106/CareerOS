from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...database import get_db
from ...dependencies import get_dashboard_query_service, require_student
from ...models.entities import Resume, Scorecard, User
from ...modules.dashboard.query.dashboard_query_service import DashboardQueryService

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
        db.query(Scorecard.id, Scorecard.overall_score, Scorecard.bucket, Scorecard.created_at)
        .join(Resume, Resume.id == Scorecard.resume_id)
        .filter(Resume.user_id == user.id)
        .order_by(Scorecard.created_at.asc())
        .limit(50)
        .all()
    )
    history = [
        {
            "scorecard_id": r.id,
            "overall_score": round(r.overall_score, 1),
            "bucket": r.bucket,
            "date": r.created_at.strftime("%Y-%m-%d"),
            "timestamp": r.created_at.isoformat(),
        }
        for r in rows
    ]
    # Compute delta from first to last
    delta = None
    if len(history) >= 2:
        delta = round(history[-1]["overall_score"] - history[0]["overall_score"], 1)

    return {"history": history, "delta": delta, "total": len(history)}
