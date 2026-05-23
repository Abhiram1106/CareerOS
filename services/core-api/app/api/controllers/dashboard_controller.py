from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...database import get_db
from ...dependencies import require_student
from ...models.entities import User
from ...modules.dashboard.query.dashboard_query_service import DashboardQueryService

router = APIRouter()


@router.get("/dashboard")
def dashboard(user: User = Depends(require_student), db: Session = Depends(get_db)):
    return DashboardQueryService(db).get_for_user(user).model_dump()
