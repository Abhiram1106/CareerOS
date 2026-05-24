"use client";

import type { BenchmarkPanelResult } from "../../modules/intel/types/intel.types";

type IntelMethodologyPanelProps = {
  methodology: BenchmarkPanelResult["methodology"];
};

export function IntelMethodologyPanel({ methodology }: IntelMethodologyPanelProps) {
  const rows = [
    { label: "Baseline", value: methodology.baseline },
    { label: "Intel path", value: methodology.intel_path },
    { label: "Accuracy guard", value: methodology.accuracy_guard },
  ];

  return (
    <div className="content-card">
      <div className="content-card-header">
        <h2 className="content-card-title">Measurement methodology</h2>
      </div>
      <div className="content-card-body">
        {rows.map((row) => (
          <p key={row.label} style={{ fontSize: "0.86rem", color: "#414752", marginBottom: 10 }}>
            <strong>{row.label}:</strong> {row.value}
          </p>
        ))}
        <div
          style={{
            background: "#ffdad6",
            border: "1px solid rgba(186,26,26,0.2)",
            borderRadius: 8,
            padding: "10px 14px",
            fontSize: "0.82rem",
            color: "#93000a",
            lineHeight: 1.5,
          }}
        >
          Never use vendor headline numbers. Only report values from{" "}
          <code>services/intel-bench/run.py</code> on target hardware.
        </div>
      </div>
    </div>
  );
}
