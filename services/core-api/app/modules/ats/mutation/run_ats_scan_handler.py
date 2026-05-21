from __future__ import annotations

from sqlalchemy.orm import Session

from ....adapter.db.persistence.ats.ats_repo import ATSRepo
from ....adapter.db.persistence.profile.profile_view import ProfileView
from ....models.entities import User
from ....services.clients import run_ats_scan
from ...profile.mapper.profile_mapper import profile_fields_for_scan
from ..dto.ats_dto import ATSScanRequest, ATSScanResponse


class RunATSScanHandler:
    def __init__(self, db: Session) -> None:
        self._db = db
        self._scans = ATSRepo(db)
        self._profiles = ProfileView(db)

    async def execute(self, user: User, payload: ATSScanRequest) -> dict:
        profile = self._profiles.find_by_user_id(user.id)
        scan_payload = {**profile_fields_for_scan(user, profile), "jd_text": payload.jd_text}
        result = await run_ats_scan(scan_payload)
        self._scans.create_from_scan_result(user_id=user.id, result=result)
        return ATSScanResponse(**result).model_dump()
