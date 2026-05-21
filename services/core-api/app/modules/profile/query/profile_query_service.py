from __future__ import annotations

from sqlalchemy.orm import Session

from ....adapter.db.persistence.profile.profile_view import ProfileView
from ....models.entities import User
from ..dto.profile_dto import ProfileResponse
from ..mapper.profile_mapper import to_profile_response


class ProfileQueryService:
    def __init__(self, db: Session) -> None:
        self._view = ProfileView(db)

    def get_for_user(self, user: User) -> ProfileResponse:
        profile = self._view.find_by_user_id(user.id)
        return to_profile_response(user, profile)
