from __future__ import annotations

from sqlalchemy.orm import Session

from ....models.entities import User
from ..dto.agent_dto import AgentRunRequest
from ..state_machine import AgentStateMachine


class RunAgentHandler:
    def __init__(self, db: Session) -> None:
        self._db = db

    async def execute(self, user: User, payload: AgentRunRequest) -> dict:
        return await AgentStateMachine(self._db).execute(user, payload)
