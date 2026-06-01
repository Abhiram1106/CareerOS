"""Password reset — console-mode (no email service required).

Flow:
  1. POST /auth/reset-request  {email}
     → generates a short-lived token, prints it to server stdout.
     → respond 200 regardless (don't leak whether the email exists).

  2. POST /auth/reset-confirm  {token, new_password}
     → validates the token, hashes the new password, clears all sessions.

The token is printed to docker logs (visible via `docker compose logs core-api`).
This is intentional for a bootcamp/dev context — replace with an email
transport when moving to production.
"""

from __future__ import annotations

import logging
import secrets
from datetime import datetime, timedelta, timezone
from typing import ClassVar

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ....adapter.db.persistence.auth.session_repo import SessionRepo
from ....adapter.db.persistence.auth.user_repo import UserRepo
from ....services.auth import hash_password

log = logging.getLogger(__name__)

# In-process token store: {token: (user_id, expires_at)}
# A restart clears all pending resets — acceptable for a dev context.
_PENDING: dict[str, tuple[int, datetime]] = {}
_TTL_MINUTES: int = 30


class RequestPasswordResetHandler:
    def __init__(self, db: Session) -> None:
        self._users = UserRepo(db)

    def execute(self, email: str) -> dict:
        user = self._users.find_by_email(email)
        if user:
            token = secrets.token_urlsafe(32)
            expires = datetime.now(timezone.utc) + timedelta(minutes=_TTL_MINUTES)
            _PENDING[token] = (user.id, expires)
            # Console-mode: print token to server logs — no email sent.
            log.warning(
                "PASSWORD_RESET_TOKEN email=%s token=%s expires=%s "
                "(retrieve with: docker compose logs core-api | grep PASSWORD_RESET_TOKEN)",
                email,
                token,
                expires.isoformat(),
            )
        # Always 200 — do not reveal whether the email exists.
        return {"ok": True, "note": "If this email is registered, check server logs for the reset token."}


class ConfirmPasswordResetHandler:
    def __init__(self, db: Session) -> None:
        self._db = db
        self._users = UserRepo(db)
        self._sessions = SessionRepo(db)

    def execute(self, token: str, new_password: str) -> dict:
        entry = _PENDING.get(token)
        if not entry:
            raise HTTPException(status_code=400, detail="Invalid or expired reset token.")

        user_id, expires = entry
        if datetime.now(timezone.utc) > expires:
            del _PENDING[token]
            raise HTTPException(status_code=400, detail="Reset token has expired. Request a new one.")

        if len(new_password) < 8:
            raise HTTPException(status_code=422, detail="Password must be at least 8 characters.")

        user = self._users.find_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        user.password_hash = hash_password(new_password)
        self._db.commit()
        self._sessions.revoke_all_for_user(user_id)
        del _PENDING[token]
        return {"ok": True, "detail": "Password updated. All sessions have been revoked — please log in again."}
