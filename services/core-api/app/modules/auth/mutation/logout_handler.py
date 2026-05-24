from __future__ import annotations

from sqlalchemy.orm import Session

from ....adapter.db.persistence.auth.session_repo import SessionRepo
from ....dependencies import _extract_token
from ....models.entities import User
from ....services.audit import record_audit


class LogoutHandler:
    def __init__(self, db: Session) -> None:
        self._sessions = SessionRepo(db)
        self._db = db

    def execute(self, user: User, authorization: str | None) -> dict:
        token = _extract_token(authorization)
        revoked = self._sessions.revoke_token(token)
        record_audit(
            self._db,
            actor_id=user.id,
            action="auth.logout",
            target_type="user",
            target_id=user.id,
            payload={"revoked": revoked},
        )
        return {"ok": True, "revoked": revoked}
