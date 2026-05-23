from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...database import get_db
from ...dependencies import require_student
from ...models.entities import User
from ...modules.scorecard.dto.scorecard_dto import ScorecardScoreRequest
from ...modules.scorecard.mutation.score_resume_handler import ScoreResumeHandler

router = APIRouter()


@router.post("/scorecards/score")
async def score_resume(
    payload: ScorecardScoreRequest,
    user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    return await ScoreResumeHandler(db).execute(user, payload)
