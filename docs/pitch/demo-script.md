# CareerOS Student-First Demo Script (<= 3 minutes)

## Goal

Show one deterministic flow: **resume + job → score + rewrite + export** with no fabricated claims.

## Script

1. **Open Builder Wizard**
   - Route: `/workspace` tab **Builder Wizard** (or `/workspace/builder`)
   - Say: "This mode automates the whole placement-readiness loop."

2. **Find a Job**
   - Use Jobs Feed query: `software engineer`, location `India`
   - Say: "We fetch real-time jobs with a local seed fallback for reliability."

3. **Run Deterministic Agent**
   - Click `Run agent on this job`
   - Say: "The agent runs ATS parse-safety, JD matching, scoring, proof-linked rewrite, and queues PDF export."

4. **Show Agent Progress**
   - Highlight run id, current step, and completed status in Agent Progress panel.
   - Say: "Every step is persisted in `agent_runs` so failures can be resumed."

5. **Show Rewrite Safety**
   - Open Rewrite panel output.
   - Say: "Unsupported claims are listed separately and never inserted into rewrites."

6. **Show Benchmark Credibility**
   - Open `docs/benchmarks/match-engine-sklearnex.md`
   - Mention measured result (50x50 workload):
     - p50: 20.878 ms -> 18.381 ms
     - p95: 29.978 ms -> 25.968 ms
     - Throughput: +23.96%

## Closing line

"CareerOS now delivers a student-first, deterministic, no-fabrication readiness workflow while reusing the original service architecture with measured Intel acceleration."

