"use client";

import { IntelBenchmarkTable } from "../../../../components/intel/IntelBenchmarkTable";
import { IntelHardwareMeta } from "../../../../components/intel/IntelHardwareMeta";
import { IntelIntegrationSnippet } from "../../../../components/intel/IntelIntegrationSnippet";
import { IntelMethodologyPanel } from "../../../../components/intel/IntelMethodologyPanel";
import { IntelScoreFormulaPanel } from "../../../../components/intel/IntelScoreFormulaPanel";
import { useIntelBenchmarkPanel } from "../../../../modules/intel/useIntelBenchmarkPanel";

export default function IntelLabPage() {
  const { data, loading, error } = useIntelBenchmarkPanel();
  const hasMeasured = data?.workloads.some((w) => w.status === "measured") ?? false;

  return (
    <div className="page-canvas">
      <div className="page-title-row">
        <div>
          <h1 className="page-title">Intel Performance Lab</h1>
          <p className="page-subtitle">Measured OpenVINO + sklearnex benchmarks for bootcamp judges.</p>
        </div>
        <span
          className={`chip ${hasMeasured ? "chip-success" : "chip-warn"}`}
          style={{ fontFamily: "var(--font-mono)", fontSize: "0.72rem" }}
        >
          {hasMeasured ? "Live measurements" : "Awaiting harness run"}
        </span>
      </div>

      {loading && (
        <div className="content-card">
          <div className="content-card-body">Loading Intel benchmark panel...</div>
        </div>
      )}
      {!loading && error && (
        <div className="content-card">
          <div className="content-card-body" style={{ color: "#8f2c2c" }}>{error}</div>
        </div>
      )}

      {!loading && !error && data && (
        <>
          <IntelHardwareMeta hardware={data.hardware} generatedAt={data.generated_at} />
          <IntelBenchmarkTable workloads={data.workloads} />
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }}>
            <IntelMethodologyPanel methodology={data.methodology} />
            <IntelIntegrationSnippet />
          </div>
          <IntelScoreFormulaPanel />
        </>
      )}
    </div>
  );
}
