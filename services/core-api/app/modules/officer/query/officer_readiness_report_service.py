from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from ....services.pdf_export import build_cohort_readiness_html, generate_cohort_readiness_pdf_bytes
from ..officer_scope import resolve_officer_college_id
from .officer_dashboard_query_service import OfficerDashboardQueryService
from .officer_heatmap_query_service import OfficerHeatmapQueryService
from .officer_skill_gaps_query_service import OfficerSkillGapsQueryService


class OfficerReadinessReportService:
    def __init__(self, db: Session) -> None:
        self._db = db
        self._college_id = resolve_officer_college_id(db)

    def generate_pdf_bytes(self) -> bytes:
        dashboard = OfficerDashboardQueryService(self._db).get_dashboard()
        heatmap = OfficerHeatmapQueryService(self._db).get_heatmap()
        gaps = OfficerSkillGapsQueryService(self._db).get_skill_gaps()

        college_label = f"College #{self._college_id}" if self._college_id else "All colleges"
        generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

        html_doc = build_cohort_readiness_html(
            generated_at=generated_at,
            college_label=college_label,
            students_scored=dashboard.kpis.students_scored,
            avg_readiness=dashboard.kpis.avg_readiness,
            parse_safe_rate=dashboard.kpis.parse_safe_rate,
            ready_count=dashboard.kpis.ready_count,
            buckets={
                "strong": dashboard.buckets.strong,
                "ready": dashboard.buckets.ready,
                "borderline": dashboard.buckets.borderline,
                "risk": dashboard.buckets.risk,
            },
            heatmap_rows=[row.model_dump() for row in heatmap.departments],
            skill_gap_rows=[item.model_dump() for item in gaps.items],
        )
        return generate_cohort_readiness_pdf_bytes(html_doc)
