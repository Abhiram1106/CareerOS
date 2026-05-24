"use client";

import type { BenchmarkPanelResult } from "../../modules/intel/types";

type IntelHardwareMetaProps = {
  hardware: BenchmarkPanelResult["hardware"];
  generatedAt: string;
};

export function IntelHardwareMeta({ hardware, generatedAt }: IntelHardwareMetaProps) {
  return (
    <div className="content-card" style={{ marginBottom: 20 }}>
      <div className="content-card-header">
        <h2 className="content-card-title">Measurement environment</h2>
        {generatedAt ? (
          <span className="chip chip-mono">{new Date(generatedAt).toLocaleString()}</span>
        ) : null}
      </div>
      <div className="content-card-body">
        <p style={{ fontFamily: "var(--font-mono)", fontSize: "0.78rem", color: "#414752", margin: 0 }}>
          {hardware.platform} · {hardware.processor} · Python {hardware.python}
        </p>
      </div>
    </div>
  );
}
