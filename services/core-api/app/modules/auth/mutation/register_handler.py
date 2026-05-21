from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ....adapter.db.persistence.auth.session_repo import SessionRepo
from ....adapter.db.persistence.auth.user_repo import UserRepo
from ....adapter.db.persistence.profile.profile_repo import ProfileRepo
from ..dto.auth_dto import RegisterRequest
from ..mapper.auth_mapper import to_auth_response


class RegisterHandler:
    def __init__(self, db: Session) -> None:
        self._users = UserRepo(db)
        self._sessions = SessionRepo(db)
        self._profiles = ProfileRepo(db)

    def execute(self, payload: RegisterRequest) -> dict:
        if self._users.find_by_email(payload.email):
            raise HTTPException(status_code=400, detail="Email already exists")

        user = self._users.create(
            email=payload.email,
            password=payload.password,
            full_name=payload.full_name,
            role=payload.role,
        )
        self._profiles.create_default_for_user(user)
        token = self._sessions.create_for_user(user)
        return to_auth_response(user, token).model_dump()
