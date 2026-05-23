from __future__ import annotations

from typing import Any
from urllib.parse import quote_plus

import httpx

BASE_URL = "https://api.adzuna.com/v1/api/jobs/in/search"


def _to_job_row(raw: dict[str, Any]) -> dict[str, Any]:
    salary_min = raw.get("salary_min")
    salary_max = raw.get("salary_max")
    salary_currency = raw.get("salary_currency")
    if salary_min is not None and salary_max is not None and salary_currency:
        salary = f"{int(salary_min)}-{int(salary_max)} {salary_currency}"
    else:
        salary = "Not disclosed"

    title = str(raw.get("title") or "Role not specified").strip()
    company_name = str((raw.get("company") or {}).get("display_name") or "Unknown company").strip()
    location = str((raw.get("location") or {}).get("display_name") or "India").strip()
    description = str(raw.get("description") or "").strip()
    redirect_url = str(raw.get("redirect_url") or "").strip()
    external_id = str(raw.get("id") or f"{company_name}-{title}").strip()

    return {
        "source": "adzuna",
        "external_id": external_id,
        "title": title,
        "company": company_name,
        "location": location,
        "salary": salary,
        "skills_required": [],
        "raw_jd_text": description,
        "apply_url": redirect_url,
    }


async def search_adzuna_jobs(query: str, location: str, page: int, app_id: str, app_key: str) -> dict[str, Any]:
    q = quote_plus(query.strip() or "software engineer")
    where = quote_plus(location.strip() or "india")
    url = (
        f"{BASE_URL}/{page}"
        f"?app_id={quote_plus(app_id)}&app_key={quote_plus(app_key)}"
        f"&results_per_page=20&what={q}&where={where}&content-type=application/json"
    )

    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(url)
        response.raise_for_status()
        payload = response.json()

    results = payload.get("results", [])
    normalized = [_to_job_row(row) for row in results if isinstance(row, dict)]

    return {
        "source": "adzuna",
        "total": int(payload.get("count", len(normalized)) or len(normalized)),
        "page": page,
        "page_size": 20,
        "results": normalized,
    }
