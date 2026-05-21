from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from .....models.entities import User
from .....services.auth import hash_password


class UserRepo:
    def __init__(self, db: Session) -> None:
        self._db = db

    def find_by_email(self, email: str) -> Optional[User]:
        return self._db.query(User).filter(User.email == email).first()

    def create(
        self,
        *,
        email: str,
        password: str,
        full_name: str,
        role: str,
    ) -> User:
        user = User(
            email=email,
            password_hash=hash_password(password),
            full_name=full_name,
            role=role,
        )
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user
