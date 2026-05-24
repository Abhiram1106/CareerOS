from __future__ import annotations

from fastapi import APIRouter, Depends

from ...dependencies import get_profile_query_service, get_upsert_profile_handler, require_student
from ...models.entities import User
from ...modules.profile.dto.profile_dto import ProfileUpsert
from ...modules.profile.mutation.upsert_profile_handler import UpsertProfileHandler
from ...modules.profile.query.profile_query_service import ProfileQueryService

router = APIRouter()


@router.get("/profile")
def get_profile(
    user: User = Depends(require_student),
    service: ProfileQueryService = Depends(get_profile_query_service),
):
    return service.get_for_user(user).model_dump()


@router.put("/profile")
def update_profile(
    payload: ProfileUpsert,
    user: User = Depends(require_student),
    handler: UpsertProfileHandler = Depends(get_upsert_profile_handler),
):
    return handler.execute(user, payload)
