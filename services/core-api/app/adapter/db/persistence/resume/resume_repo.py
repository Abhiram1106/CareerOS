from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from .....models.entities import Resume, User


class ResumeRepo:
    def __init__(self, db: Session) -> None:
        self._db = db

    def find_by_id_for_user(self, resume_id: int, user_id: int) -> Optional[Resume]:
        return (
            self._db.query(Resume)
            .filter(Resume.id == resume_id, Resume.user_id == user_id)
            .first()
        )

    def list_for_user(self, user_id: int) -> list[Resume]:
        return (
            self._db.query(Resume)
            .filter(Resume.user_id == user_id)
            .order_by(Resume.created_at.desc())
            .all()
        )

    def create_generated(self, *, user_id: int, template_name: str, content_text: str) -> Resume:
        resume = Resume(user_id=user_id, template_name=template_name, content_text=content_text)
        self._db.add(resume)
        self._db.commit()
        self._db.refresh(resume)
        return resume

    def create_uploaded(self, *, user_id: int, source_format: str) -> Resume:
        resume = Resume(user_id=user_id, source_format=source_format, template_name="uploaded")
        self._db.add(resume)
        self._db.commit()
        self._db.refresh(resume)
        return resume

    def delete_for_user(self, resume_id: int, user_id: int) -> bool:
        row = self.find_by_id_for_user(resume_id, user_id)
        if not row:
            return False
        self._db.delete(row)
        self._db.commit()
        return True
