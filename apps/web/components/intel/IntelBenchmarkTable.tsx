"use client";

import type { BenchmarkWorkload } from "../../modules/intel/types";

type IntelBenchmarkTableProps = {
  workloads: BenchmarkWorkload[];
};

function formatMs(value: number | null): string {
  return value == null ? "—" : String(value);
}

function formatSpeedup(value: number | null): string {
  if (value == null) return "—";
  return `${value.toFixed(3)}×`;
}

export function IntelBenchmarkTable({ workloads }: IntelBenchmarkTableProps) {
  return (
    <div className="intel-panel" style={{ marginBottom: 24 }}>
      <div className="intel-panel-header">
        <p className="intel-panel-sub">Intel-optimized pipeline</p>
        <h2 className="intel-panel-title">Latency &amp; throughput results</h2>
      </div>
      <div className="intel-panel-body" style={{ padding: 0 }}>
        {workloads.length === 0 ? (
          <p style={{ padding: 16, fontFamily: "var(--font-mono)", fontSize: "0.82rem", color: "#717783" }}>
            No benchmark artifact yet. Run{" "}
            <code>python services/intel-bench/run.py --workload all --size medium</code>.
          </p>
        ) : (
          <table className="stitch-table" style={{ margin: 0 }}>
            <thead>
              <tr>
                <th>Workload</th>
                <th>Intel tool</th>
                <th>Baseline p50 (ms)</th>
                <th>Intel p50 (ms)</th>
                <th>Speedup</th>
                <th>Accuracy Δ</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {workloads.map((row) => (
                <tr key={row.id}>
                  <td style={{ fontWeight: 600, maxWidth: 220 }}>{row.name}</td>
                  <td>
                    <span className="chip chip-primary" style={{ fontFamily: "var(--font-mono)", fontSize: "0.7rem" }}>
                      {row.tool}
                    </span>
                  </td>
                  <td style={{ fontFamily: "var(--font-mono)", color: "#717783" }}>{formatMs(row.baseline_p50_ms)}</td>
                  <td style={{ fontFamily: "var(--font-mono)", color: "#717783" }}>{formatMs(row.intel_p50_ms)}</td>
                  <td style={{ fontFamily: "var(--font-mono)", fontWeight: 700, color: "#0071c5" }}>
                    {formatSpeedup(row.speedup)}
                  </td>
                  <td>
                    <span className="chip chip-success" style={{ fontFamily: "var(--font-mono)", fontSize: "0.7rem" }}>
                      {row.accuracy_delta_pct == null ? "—" : `${row.accuracy_delta_pct}%`}
                    </span>
                  </td>
                  <td>
                    <span className={`chip ${row.status === "measured" ? "chip-success" : "chip-warn"}`}>
                      {row.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
