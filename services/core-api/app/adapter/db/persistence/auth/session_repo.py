from __future__ import annotations

from sqlalchemy.orm import Session

from .....models.entities import SessionToken, User
from .....services.auth import create_access_token


class SessionRepo:
    def __init__(self, db: Session) -> None:
        self._db = db

    def create_for_user(self, user: User) -> str:
        token = create_access_token(user)
        self._db.add(SessionToken(token=token, user_id=user.id, is_active=True))
        self._db.commit()
        return token

    def revoke_all_for_user(self, user_id: int) -> int:
        """Deactivate all active sessions for a user. Returns count revoked."""
        updated = (
            self._db.query(SessionToken)
            .filter(SessionToken.user_id == user_id, SessionToken.is_active.is_(True))
            .all()
        )
        for s in updated:
            s.is_active = False
        self._db.commit()
        return len(updated)

    def revoke_token(self, token: str) -> bool:
        session = (
            self._db.query(SessionToken)
            .filter(SessionToken.token == token, SessionToken.is_active.is_(True))
            .first()
        )
        if not session:
            return False
        session.is_active = False
        self._db.commit()
        return True
