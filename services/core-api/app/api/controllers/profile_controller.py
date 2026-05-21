from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...database import get_db
from ...dependencies import current_user
from ...models.entities import User
from ...modules.profile.dto.profile_dto import ProfileUpsert
from ...modules.profile.mutation.upsert_profile_handler import UpsertProfileHandler
from ...modules.profile.query.profile_query_service import ProfileQueryService

router = APIRouter()


@router.get("/profile")
def get_profile(user: User = Depends(current_user), db: Session = Depends(get_db)):
    return ProfileQueryService(db).get_for_user(user).model_dump()


@router.put("/profile")
def update_profile(
    payload: ProfileUpsert,
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
):
    return UpsertProfileHandler(db).execute(user, payload)
