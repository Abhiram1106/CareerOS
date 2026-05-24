from __future__ import annotations

from fastapi import APIRouter, Depends

from ...dependencies import get_dashboard_query_service, require_student
from ...models.entities import User
from ...modules.dashboard.query.dashboard_query_service import DashboardQueryService

router = APIRouter()


@router.get("/dashboard")
def dashboard(
    user: User = Depends(require_student),
    service: DashboardQueryService = Depends(get_dashboard_query_service),
):
    return service.get_for_user(user).model_dump()
