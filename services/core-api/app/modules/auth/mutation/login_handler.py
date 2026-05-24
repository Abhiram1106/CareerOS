from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ....adapter.db.persistence.auth.session_repo import SessionRepo
from ....adapter.db.persistence.auth.user_repo import UserRepo
from ....services.audit import record_audit
from ....services.auth import verify_password
from ..dto.auth_dto import LoginRequest
from ..mapper.auth_mapper import to_auth_response


class LoginHandler:
    def __init__(self, db: Session) -> None:
        self._users = UserRepo(db)
        self._sessions = SessionRepo(db)
        self._db = db

    def execute(self, payload: LoginRequest) -> dict:
        user = self._users.find_by_email(payload.email)
        if not user or not verify_password(payload.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = self._sessions.create_for_user(user)
        record_audit(
            self._db,
            actor_id=user.id,
            action="auth.login",
            target_type="user",
            target_id=user.id,
            payload={"role": user.role},
        )
        return to_auth_response(user, token).model_dump()
