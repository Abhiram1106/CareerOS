import re

from ..dto.scan_dto import ScanRequest, ScanResponse


class ScanHandler:
    def execute(self, payload: ScanRequest) -> dict:
        jd = payload.jd_text.lower()
        resume_text = f"{payload.skills_csv} {payload.summary} {payload.experience_bullet}".lower()

        jd_tokens = set(re.findall(r"[a-zA-Z0-9\+#\.]{3,}", jd))
        resume_tokens = set(re.findall(r"[a-zA-Z0-9\+#\.]{3,}", resume_text))
        overlap = len(jd_tokens.intersection(resume_tokens))

        keyword = min(95, max(20, overlap * 4))
        format_score = 82
        action_hits = sum(
            1
            for w in ["built", "developed", "designed", "optimized", "deployed", "led"]
            if w in payload.experience_bullet.lower()
        )
        metric_hits = len(re.findall(r"\b\d+(%|x|k|m)?\b", payload.experience_bullet.lower()))
        quality = min(95, 55 + action_hits * 5 + metric_hits * 6)

        completeness_fields = [
            payload.full_name,
            payload.email,
            payload.target_role,
            payload.skills_csv,
            payload.summary,
            payload.experience_bullet,
        ]
        complete = round(100 * (sum(1 for f in completeness_fields if f) / len(completeness_fields)))
        contact = 95 if payload.email else 50

        composite = round(
            keyword * 0.30 + format_score * 0.20 + quality * 0.20 + complete * 0.15 + contact * 0.15,
            1,
        )

        return ScanResponse(
            composite=composite,
            keyword=keyword,
            format=format_score,
            quality=quality,
            complete=complete,
            contact=contact,
        ).model_dump()
