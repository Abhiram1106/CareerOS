"use client";

// Intel Performance Lab — benchmark results panel.
// Week 5 deliverable: numbers below are PLACEHOLDERS until real harness runs.
// Replace with actual services/intel-bench/run.py output before demo day.

const PLACEHOLDER_NOTE =
  "⚠ Benchmark numbers are placeholders. Run `python services/intel-bench/run.py --workload all --size medium` on target hardware and update this table with measured values.";

const BENCHMARKS = [
  {
    workload: "Sentence-transformer inference",
    tool: "OpenVINO FP16",
    baseline_ms: "—",
    intel_ms: "—",
    speedup: "~2–4×",
    accuracy_delta: "< 0.5%",
    note: "Not yet measured",
  },
  {
    workload: "TF-IDF + cosine similarity",
    tool: "sklearnex patch",
    baseline_ms: "—",
    intel_ms: "—",
    speedup: "~1.5–3×",
    accuracy_delta: "0%",
    note: "Not yet measured",
  },
  {
    workload: "KMeans cohort clustering",
    tool: "sklearnex patch",
    baseline_ms: "—",
    intel_ms: "—",
    speedup: "~2–8×",
    accuracy_delta: "0%",
    note: "Not yet measured",
  },
  {
    workload: "End-to-end score pipeline (5K resumes)",
    tool: "OpenVINO + sklearnex",
    baseline_ms: "—",
    intel_ms: "—",
    speedup: "compound",
    accuracy_delta: "< 1%",
    note: "Not yet measured",
  },
];

const METHODOLOGY = [
  { label: "Baseline", value: "Stock PyTorch + sklearn (no patches)" },
  { label: "Intel path", value: "OpenVINO IR (FP16) + sklearnex.patch_sklearn()" },
  { label: "Dataset sizes", value: "500 · 5,000 · 20,000 synthetic resumes" },
  { label: "Metrics", value: "p50 latency · p95 latency · throughput (RPH) · accuracy delta · memory MB" },
  { label: "Hardware", value: "Run on bootcamp machine — record exact CPU model + RAM" },
  { label: "Accuracy guard", value: "If accuracy_delta > 1% → stay at FP16, never INT8" },
];

export default function LabPage() {
  return (
    <div className="page-canvas">
      {/* Header */}
      <div className="page-title-row">
        <div>
          <h1 className="page-title">Intel Performance Lab</h1>
          <p className="page-subtitle">OpenVINO + sklearnex benchmark panel — Week 5 deliverable.</p>
        </div>
        <span className="chip chip-warn" style={{ fontFamily: "var(--font-mono)", fontSize: "0.72rem" }}>Pending measurement</span>
      </div>

      {/* Placeholder warning */}
      <div style={{ background: "#fef3c7", border: "1px solid rgba(217,119,6,0.3)", borderRadius: 10, padding: "14px 18px", marginBottom: 24, display: "flex", gap: 10, alignItems: "flex-start" }}>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#d97706" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ flexShrink: 0, marginTop: 1 }}>
          <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" /><line x1="12" y1="9" x2="12" y2="13" /><line x1="12" y1="17" x2="12.01" y2="17" />
        </svg>
        <p style={{ fontSize: "0.84rem", color: "#92400e", lineHeight: 1.6, margin: 0 }}>{PLACEHOLDER_NOTE}</p>
      </div>

      {/* Benchmark table */}
      <div className="intel-panel" style={{ marginBottom: 24 }}>
        <div className="intel-panel-header">
          <p className="intel-panel-sub">Week 5 · Intel-optimized pipeline</p>
          <h2 className="intel-panel-title">Latency & Throughput Results</h2>
        </div>
        <div className="intel-panel-body" style={{ padding: 0 }}>
          <table className="stitch-table" style={{ margin: 0 }}>
            <thead>
              <tr>
                <th>Workload</th>
                <th>Intel Tool</th>
                <th>Baseline p50 (ms)</th>
                <th>Intel p50 (ms)</th>
                <th>Speedup</th>
                <th>Accuracy Δ</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {BENCHMARKS.map(b => (
                <tr key={b.workload}>
                  <td style={{ fontWeight: 600, maxWidth: 200 }}>{b.workload}</td>
                  <td><span className="chip chip-primary" style={{ fontFamily: "var(--font-mono)", fontSize: "0.7rem" }}>{b.tool}</span></td>
                  <td style={{ fontFamily: "var(--font-mono)", color: "#717783" }}>{b.baseline_ms}</td>
                  <td style={{ fontFamily: "var(--font-mono)", color: "#717783" }}>{b.intel_ms}</td>
                  <td style={{ fontFamily: "var(--font-mono)", fontWeight: 700, color: "#0071c5" }}>{b.speedup}</td>
                  <td><span className="chip chip-success" style={{ fontFamily: "var(--font-mono)", fontSize: "0.7rem" }}>{b.accuracy_delta}</span></td>
                  <td><span className="chip chip-warn">{b.note}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Two-column: methodology + code */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }}>
        {/* Methodology */}
        <div className="content-card">
          <div className="content-card-header">
            <h2 className="content-card-title">Measurement Methodology</h2>
          </div>
          <div className="content-card-body">
            {METHODOLOGY.map(m => (
              <div key={m.label} style={{ display: "flex", gap: 12, marginBottom: 12, paddingBottom: 12, borderBottom: "1px solid rgba(192,199,211,0.2)" }}>
                <span style={{ fontFamily: "var(--font-mono)", fontSize: "0.72rem", fontWeight: 600, color: "#0071c5", width: 110, flexShrink: 0, paddingTop: 1 }}>{m.label}</span>
                <span style={{ fontSize: "0.86rem", color: "#414752", lineHeight: 1.55 }}>{m.value}</span>
              </div>
            ))}
            <div style={{ background: "#ffdad6", border: "1px solid rgba(186,26,26,0.2)", borderRadius: 8, padding: "10px 14px", fontSize: "0.82rem", color: "#93000a", lineHeight: 1.5 }}>
              <strong>Never use vendor headline numbers.</strong> Only report measured values from actual hardware. If judges ask — show the raw JSON output file.
            </div>
          </div>
        </div>

        {/* Code pattern */}
        <div className="content-card">
          <div className="content-card-header">
            <h2 className="content-card-title">Intel Integration Pattern</h2>
            <span className="chip chip-mono">services/match-engine/</span>
          </div>
          <div className="content-card-body">
            <p style={{ fontFamily: "var(--font-mono)", fontSize: "0.7rem", fontWeight: 600, color: "#0071c5", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: 8 }}>
              sklearnex — must be FIRST import
            </p>
            <pre style={{ fontSize: "0.78rem", background: "#f2f4f7", border: "1px solid rgba(192,199,211,0.3)", borderRadius: 8, padding: "12px 16px", lineHeight: 1.7, overflowX: "auto" }}>
{`from sklearnex import patch_sklearn
patch_sklearn()  # BEFORE all sklearn imports
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity`}
            </pre>

            <p style={{ fontFamily: "var(--font-mono)", fontSize: "0.7rem", fontWeight: 600, color: "#0071c5", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: 8, marginTop: 16 }}>
              OpenVINO — embedding inference
            </p>
            <pre style={{ fontSize: "0.78rem", background: "#f2f4f7", border: "1px solid rgba(192,199,211,0.3)", borderRadius: 8, padding: "12px 16px", lineHeight: 1.7, overflowX: "auto" }}>
{`from openvino.runtime import Core

core = Core()
model = core.read_model("model/embedding.xml")
compiled = core.compile_model(model, "CPU")
# If accuracy_delta > 0.01 → stay FP16, not INT8`}
            </pre>

            <div style={{ marginTop: 14, padding: "10px 14px", background: "#d3e4ff", borderRadius: 8, fontSize: "0.82rem", color: "#001c38", lineHeight: 1.5 }}>
              <strong>Score formula:</strong> Always imported from <code style={{ fontFamily: "var(--font-mono)", fontSize: "0.78rem" }}>packages/scoring/</code>. Never inline or duplicate.
            </div>
          </div>
        </div>
      </div>

      {/* PlacementReadinessScore formula */}
      <div className="content-card" style={{ marginTop: 20 }}>
        <div className="content-card-header">
          <h2 className="content-card-title">PlacementReadinessScore Formula</h2>
          <span className="chip chip-primary">packages/scoring/ — single source of truth</span>
        </div>
        <div className="content-card-body">
          <pre style={{ fontSize: "0.82rem", background: "#f2f4f7", border: "1px solid rgba(192,199,211,0.3)", borderRadius: 8, padding: "16px 20px", lineHeight: 1.9, overflowX: "auto" }}>
{`PlacementReadinessScore =
  0.35 × JD_Match
+ 0.20 × ATS_Parse_Safety
+ 0.20 × Evidence_Quality
+ 0.10 × Profile_Completeness
+ 0.10 × Interview_Readiness
+ 0.05 × Placement_Hygiene

JD_Match =
  0.35 × TFIDF_Cosine           (lexical keyword overlap)
+ 0.35 × Embedding_Cosine       (semantic — OpenVINO-accelerated)
+ 0.20 × Required_Skill_Recall  (fraction of JD required skills found)
+ 0.10 × Eligibility_Rule_Score (CGPA, branch, backlogs, grad year)

Buckets:  0–49 🔴 High Risk  |  50–69 🟡 Borderline  |  70–84 🟢 Ready  |  85–100 🏆 Strong`}
          </pre>
        </div>
      </div>
    </div>
  );
}
