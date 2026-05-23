from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...database import get_db
from ...dependencies import require_student
from ...models.entities import User
from ...modules.recommendation.dto.recommendation_dto import RunRewriteRequest
from ...modules.recommendation.mutation.run_rewrite_handler import RunRewriteHandler
from ...modules.recommendation.query.recommendation_query_service import RecommendationQueryService

router = APIRouter()


@router.post("/recommendations/rewrite")
async def run_rewrite(
    payload: RunRewriteRequest,
    user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    return await RunRewriteHandler(db).execute(user, payload)


@router.get("/recommendations/{scorecard_id}")
def list_recommendations(
    scorecard_id: int,
    user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    return RecommendationQueryService(db).for_scorecard(user, scorecard_id)
