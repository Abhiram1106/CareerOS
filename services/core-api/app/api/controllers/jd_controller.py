from __future__ import annotations

from fastapi import APIRouter, Depends

from ...dependencies import get_parse_jd_handler, require_student
from ...models.entities import User
from ...modules.jd.dto.jd_dto import JDParseRequest
from ...modules.jd.mutation.parse_jd_handler import ParseJDHandler

router = APIRouter()


@router.post("/jd/parse")
async def parse_jd(
    payload: JDParseRequest,
    user: User = Depends(require_student),
    handler: ParseJDHandler = Depends(get_parse_jd_handler),
):
    return await handler.execute(user, payload)
