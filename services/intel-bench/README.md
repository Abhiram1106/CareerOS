# Intel benchmark harness

Measured workloads for the bootcamp Intel panel (`GET /benchmarks`).

## Supported Python versions

| Version | sklearnex KMeans | OpenVINO probe |
|---------|------------------|----------------|
| 3.11    | Yes              | Yes (if `openvino` installed) |
| 3.12    | Yes              | Yes |
| 3.13+   | KMeans may skip  | Often skipped — use 3.11/3.12 for full matrix |

## Re-run on Python 3.11 or 3.12

**Windows host with only Python 3.13:** start Docker Desktop, then:

```powershell
.\scripts\run-intel-bench-py312.ps1
```

Native venv:

```bash
cd services/intel-bench
python3.11 -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt
pip install scikit-learn-intelex openvino  # optional OpenVINO

python run.py --export-docs
```

Artifacts:

- `services/intel-bench/results/benchmark_runs.json`
- `docs/benchmarks/benchmark_runs.json` (when `--export-docs`)

## OpenVINO embedding probe

```bash
python -m workloads.openvino_probe
```

If OpenVINO is unavailable, the harness records `status: skipped` with an honest note — never fabricate speedup numbers.
