from __future__ import annotations

from sqlalchemy.orm import Session

from ...config import OFFICER_DEFAULT_COLLEGE_ID
from ...models.entities import College


def resolve_officer_college_id(db: Session) -> int | None:
    """College scope for officer queries. None = no filter (all cohort data)."""
    if OFFICER_DEFAULT_COLLEGE_ID <= 0:
        return None
    exists = db.query(College.id).filter(College.id == OFFICER_DEFAULT_COLLEGE_ID).first()
    return OFFICER_DEFAULT_COLLEGE_ID if exists else None


def ensure_officer_college_id(db: Session) -> int:
    """College id for batch mutations — creates a demo college when unset."""
    scoped = resolve_officer_college_id(db)
    if scoped is not None:
        return scoped
    existing = db.query(College).order_by(College.id.asc()).first()
    if existing:
        return existing.id
    college = College(name="Demo Campus", state="KA", college_type="engineering")
    db.add(college)
    db.commit()
    db.refresh(college)
    return college.id
