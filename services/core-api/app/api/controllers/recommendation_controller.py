from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ...adapter.db.persistence.recommendation.recommendation_repo import RecommendationRepo
from ...database import get_db
from ...dependencies import get_recommendation_query_service, get_run_rewrite_handler, require_student
from ...models.entities import User
from ...modules.recommendation.dto.recommendation_dto import RunRewriteRequest
from ...modules.recommendation.mutation.run_rewrite_handler import RunRewriteHandler
from ...modules.recommendation.query.recommendation_query_service import RecommendationQueryService
from ...services.clients import vector_user_signal

router = APIRouter()


class RecommendationFeedback(BaseModel):
    accepted: bool


@router.post("/recommendations/rewrite")
async def run_rewrite(
    payload: RunRewriteRequest,
    user: User = Depends(require_student),
    handler: RunRewriteHandler = Depends(get_run_rewrite_handler),
):
    return await handler.execute(user, payload)


@router.get("/recommendations/{scorecard_id}")
def list_recommendations(
    scorecard_id: int,
    user: User = Depends(require_student),
    service: RecommendationQueryService = Depends(get_recommendation_query_service),
):
    return service.for_scorecard(user, scorecard_id)


@router.put("/recommendations/feedback/{rec_id}")
async def record_feedback(
    rec_id: int,
    payload: RecommendationFeedback,
    user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    """CARE-RAG Layer 6: record suggestion accept/reject and log to user memory."""
    repo = RecommendationRepo(db)
    row = repo.set_feedback(rec_id, payload.accepted)
    if not row:
        raise HTTPException(status_code=404, detail="Recommendation not found")

    signal_type = "suggestion_accepted" if payload.accepted else "suggestion_rejected"
    content = (
        f"{signal_type}: section={row.section} "
        f"before={row.before_text[:100]} after={row.after_text[:100]}"
    )
    await vector_user_signal(
        user_id=user.id,
        signal_type=signal_type,
        scorecard_id=row.scorecard_id,
        content=content,
    )

    return {"ok": True, "rec_id": rec_id, "accepted": payload.accepted, "signal": signal_type}
