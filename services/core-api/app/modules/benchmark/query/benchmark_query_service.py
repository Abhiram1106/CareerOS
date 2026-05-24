from __future__ import annotations

from ....adapter.db.persistence.benchmark.intel_bench_artifact_view import IntelBenchArtifactView
from ..dto.benchmark_dto import (
    BenchmarkHardwareDto,
    BenchmarkMethodologyDto,
    BenchmarkPanelResponse,
    BenchmarkWorkloadDto,
)


class BenchmarkQueryService:
    def __init__(self, view: IntelBenchArtifactView | None = None) -> None:
        self._view = view or IntelBenchArtifactView()

    def get_panel(self) -> BenchmarkPanelResponse:
        raw = self._view.load_artifact()
        if not raw:
            return BenchmarkPanelResponse(
                generated_at="",
                hardware=BenchmarkHardwareDto(
                    platform="unknown",
                    processor="unknown",
                    python="unknown",
                ),
                methodology=BenchmarkMethodologyDto(
                    baseline="Stock sklearn",
                    intel_path="sklearnex + OpenVINO",
                    accuracy_guard="accuracy_delta must stay <= 1%",
                ),
                workloads=[],
            )

        workloads = [BenchmarkWorkloadDto.model_validate(w) for w in raw.get("workloads", [])]
        return BenchmarkPanelResponse(
            generated_at=raw.get("generated_at", ""),
            hardware=BenchmarkHardwareDto.model_validate(
                raw.get(
                    "hardware",
                    {"platform": "unknown", "processor": "unknown", "python": "unknown"},
                )
            ),
            methodology=BenchmarkMethodologyDto.model_validate(
                raw.get(
                    "methodology",
                    {
                        "baseline": "Stock sklearn",
                        "intel_path": "sklearnex",
                        "accuracy_guard": "<=1% accuracy delta",
                    },
                )
            ),
            workloads=workloads,
        )
