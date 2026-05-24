from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...database import get_db
from ...dependencies import require_student
from ...models.entities import User
from ...modules.assistant.dto.assistant_dto import AssistantChatRequest, AssistantChatResponse
from ...modules.assistant.mutation.chat_handler import ChatHandler

router = APIRouter()


@router.post("/assistant/chat", response_model=AssistantChatResponse)
async def assistant_chat(
    payload: AssistantChatRequest,
    user: User = Depends(require_student),
    db: Session = Depends(get_db),
) -> AssistantChatResponse:
    return await ChatHandler(db).execute(user, payload)
