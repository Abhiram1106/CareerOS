from __future__ import annotations

import json

from sqlalchemy.orm import Session

from ....adapter.db.persistence.jd.jd_repo import JDRepo
from ....models.entities import User
from ....services.clients import parse_jd_text
from ..dto.jd_dto import JDParseRequest, JDParseResponse


class ParseJDHandler:
    def __init__(self, db: Session) -> None:
        self._db = db
        self._jds = JDRepo(db)

    async def execute(self, user: User, payload: JDParseRequest) -> dict:
        parsed = await parse_jd_text(payload.jd_text)
        company = payload.company.strip() or parsed.get("company", "Unknown")
        role = payload.role.strip() or parsed.get("role", "Role")
        row = self._jds.create(
            created_by=user.id,
            college_id=payload.college_id,
            company=company,
            role=role,
            raw_text=payload.jd_text,
            skills_json=json.dumps(
                {
                    "required": parsed.get("required_skills", []),
                    "optional": parsed.get("optional_skills", []),
                    "all": parsed.get("all_skills", []),
                }
            ),
            eligibility_json=json.dumps(parsed.get("eligibility", {})),
        )
        return JDParseResponse(
            jd_id=row.id,
            company=row.company,
            role=row.role,
            required_skills=parsed.get("required_skills", []),
            optional_skills=parsed.get("optional_skills", []),
            eligibility=parsed.get("eligibility", {}),
        ).model_dump()
