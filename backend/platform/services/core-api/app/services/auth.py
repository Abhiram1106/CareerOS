from datetime import datetime, timedelta, timezone
import secrets
from typing import Optional

from sqlalchemy.orm import Session

from ..config import JWT_ALG, JWT_EXPIRE_MINUTES, JWT_SECRET
from ..models.entities import SessionToken, User

try:
    from jose import jwt
except Exception:
    jwt = None

try:
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
except Exception:
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


def create_access_token(subject: str) -> str:
    if not jwt:
        return f"dev-{subject}-{secrets.token_urlsafe(24)}"
    expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)


def create_session(db: Session, user: User) -> str:
    token = create_access_token(str(user.id))
    db.add(SessionToken(token=token, user_id=user.id, is_active=True))
    db.commit()
    return token


def get_user_by_token(db: Session, token: str) -> Optional[User]:
    session = db.query(SessionToken).filter(SessionToken.token == token, SessionToken.is_active.is_(True)).first()
    if not session:
        return None
    return db.query(User).filter(User.id == session.user_id).first()
