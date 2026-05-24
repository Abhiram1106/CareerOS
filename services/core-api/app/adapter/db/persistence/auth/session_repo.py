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
