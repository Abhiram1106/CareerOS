from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class BenchmarkHardwareDto(BaseModel):
    model_config = ConfigDict(extra="forbid")

    platform: str
    processor: str
    python: str


class BenchmarkMethodologyDto(BaseModel):
    model_config = ConfigDict(extra="forbid")

    baseline: str
    intel_path: str
    accuracy_guard: str


class BenchmarkWorkloadDto(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    name: str
    tool: str
    status: str
    note: str = ""
    baseline_p50_ms: float | None = None
    intel_p50_ms: float | None = None
    baseline_p95_ms: float | None = None
    intel_p95_ms: float | None = None
    speedup: float | None = None
    accuracy_delta_pct: float | None = None
    throughput_baseline_rph: float | None = None
    throughput_intel_rph: float | None = None
    dataset: dict = {}


class BenchmarkPanelResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    generated_at: str
    hardware: BenchmarkHardwareDto
    methodology: BenchmarkMethodologyDto
    workloads: list[BenchmarkWorkloadDto]
