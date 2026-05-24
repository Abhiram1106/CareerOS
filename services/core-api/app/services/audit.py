from __future__ import annotations

import json
from typing import Any, Optional

from sqlalchemy.orm import Session

from ..models.entities import EventAudit


def record_audit(
    db: Session,
    *,
    actor_id: int,
    action: str,
    target_type: str = "",
    target_id: Optional[int] = None,
    payload: Optional[dict[str, Any]] = None,
) -> EventAudit:
    row = EventAudit(
        actor_id=actor_id,
        action=action,
        target_type=target_type,
        target_id=target_id,
        payload_json=json.dumps(payload or {}),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
