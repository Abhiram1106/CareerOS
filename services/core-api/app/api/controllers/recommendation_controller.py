from __future__ import annotations

from fastapi import APIRouter, Depends

from ...dependencies import get_recommendation_query_service, get_run_rewrite_handler, require_student
from ...models.entities import User
from ...modules.recommendation.dto.recommendation_dto import RunRewriteRequest
from ...modules.recommendation.mutation.run_rewrite_handler import RunRewriteHandler
from ...modules.recommendation.query.recommendation_query_service import RecommendationQueryService

router = APIRouter()


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
