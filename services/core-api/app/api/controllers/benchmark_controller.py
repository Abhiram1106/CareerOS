from __future__ import annotations

from fastapi import APIRouter

from ...modules.benchmark.query.benchmark_query_service import BenchmarkQueryService

router = APIRouter(prefix="/benchmarks", tags=["benchmarks"])


@router.get("")
def get_benchmark_panel():
    """Public read-only aggregate for Intel Performance Lab UI."""
    return BenchmarkQueryService().get_panel().model_dump()
