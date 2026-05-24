from __future__ import annotations

from fastapi import APIRouter, Depends

from ...dependencies import get_agent_run_query_service, get_run_agent_handler, require_student
from ...models.entities import User
from ...modules.agent.dto.agent_dto import AgentRunRequest
from ...modules.agent.mutation.run_agent_handler import RunAgentHandler
from ...modules.agent.query.agent_run_query_service import AgentRunQueryService

router = APIRouter()


@router.post("/agent/run")
async def run_agent(
    payload: AgentRunRequest,
    user: User = Depends(require_student),
    handler: RunAgentHandler = Depends(get_run_agent_handler),
):
    return await handler.execute(user, payload)


@router.get("/agent/runs/{run_id}")
def get_agent_run(
    run_id: int,
    user: User = Depends(require_student),
    service: AgentRunQueryService = Depends(get_agent_run_query_service),
):
    return service.get_for_student(user, run_id)
