from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...database import get_db
from ...dependencies import require_student
from ...models.entities import User
from ...modules.jd.dto.jd_dto import JDParseRequest
from ...modules.jd.mutation.parse_jd_handler import ParseJDHandler

router = APIRouter()


@router.post("/jd/parse")
async def parse_jd(
    payload: JDParseRequest,
    user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    return await ParseJDHandler(db).execute(user, payload)
