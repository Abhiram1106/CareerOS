from __future__ import annotations

from fastapi import APIRouter, Depends

from ...dependencies import get_chat_handler, require_student
from ...models.entities import User
from ...modules.assistant.dto.assistant_dto import AssistantChatRequest, AssistantChatResponse
from ...modules.assistant.mutation.chat_handler import ChatHandler

router = APIRouter()


@router.post("/assistant/chat", response_model=AssistantChatResponse)
async def assistant_chat(
    payload: AssistantChatRequest,
    user: User = Depends(require_student),
    handler: ChatHandler = Depends(get_chat_handler),
) -> AssistantChatResponse:
    return await handler.execute(user, payload)
