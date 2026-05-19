from __future__ import annotations

from datetime import datetime, timedelta, timezone
import secrets
from typing import Optional

from sqlalchemy.orm import Session

from ..config import JWT_ALG, JWT_EXPIRE_MINUTES, JWT_SECRET
from ..models.entities import SessionToken, User

try:
    from jose import jwt, JWTError
except Exception:  # pragma: no cover
    jwt = None
    JWTError = Exception

try:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
except Exception:  # pragma: no cover
    pwd_context = None


def hash_password(password: str) -> str:
    if pwd_context:
        return pwd_context.hash(password)
    import hashlib
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    if pwd_context:
        return pwd_context.verify(password, hashed)
    return hash_password(password) == hashed


def create_access_token(user: User) -> str:
    """Create a JWT embedding user_id and role."""
    if not jwt:
        return f"dev-{user.id}-{user.role}-{secrets.token_urlsafe(16)}"
    expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES)
    payload = {
        "sub": str(user.id),
        "role": user.role,
        "exp": expire,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)


def decode_token(token: str) -> Optional[dict]:
    """Return the decoded payload or None if invalid/expired."""
    if not jwt:
        # Dev fallback: tokens look like "dev-{id}-{role}-{random}"
        parts = token.split("-")
        if len(parts) >= 3:
            return {"sub": parts[1], "role": parts[2]}
        return None
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
    except JWTError:
        return None


def create_session(db: Session, user: User) -> str:
    token = create_access_token(user)
    db.add(SessionToken(token=token, user_id=user.id, is_active=True))
    db.commit()
    return token


def get_user_by_token(db: Session, token: str) -> Optional[User]:
    session = db.query(SessionToken).filter(
        SessionToken.token == token,
        SessionToken.is_active.is_(True),
    ).first()
    if not session:
        return None
    return db.query(User).filter(User.id == session.user_id).first()
