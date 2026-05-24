from __future__ import annotations

from fastapi import APIRouter, Depends

from ...dependencies import get_score_resume_handler, require_student
from ...models.entities import User
from ...modules.scorecard.dto.scorecard_dto import ScorecardScoreRequest
from ...modules.scorecard.mutation.score_resume_handler import ScoreResumeHandler

router = APIRouter()


@router.post("/scorecards/score")
async def score_resume(
    payload: ScorecardScoreRequest,
    user: User = Depends(require_student),
    handler: ScoreResumeHandler = Depends(get_score_resume_handler),
):
    return await handler.execute(user, payload)
