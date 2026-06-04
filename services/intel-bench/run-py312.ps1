# Run intel-bench on Python 3.12 via Docker (host only has 3.13).
# Usage: .\scripts\run-intel-bench-py312.ps1

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
$BenchDir = Join-Path $RepoRoot "services\intel-bench"

Write-Host "Running intel-bench in python:3.12 container..."
docker run --rm `
  -v "${BenchDir}:/bench" `
  -w /bench `
  python:3.12-slim `
  bash -c "pip install -q -r requirements.txt scikit-learn-intelex openvino 2>/dev/null; python run.py --export-docs"

Write-Host "Results: services/intel-bench/results/benchmark_runs.json"
Write-Host "Docs copy: docs/benchmarks/benchmark_runs.json (if export succeeded)"
