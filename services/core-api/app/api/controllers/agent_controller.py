from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...database import get_db
from ...dependencies import require_student
from ...models.entities import User
from ...modules.agent.dto.agent_dto import AgentRunRequest
from ...modules.agent.mutation.run_agent_handler import RunAgentHandler
from ...modules.agent.query.agent_run_query_service import AgentRunQueryService

router = APIRouter()


@router.post("/agent/run")
async def run_agent(
    payload: AgentRunRequest,
    user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    return await RunAgentHandler(db).execute(user, payload)


@router.get("/agent/runs/{run_id}")
def get_agent_run(
    run_id: int,
    user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    return AgentRunQueryService(db).get_for_student(user, run_id)
