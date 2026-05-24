"use client";

export function IntelIntegrationSnippet() {
  return (
    <div className="content-card">
      <div className="content-card-header">
        <h2 className="content-card-title">Intel integration pattern</h2>
        <span className="chip chip-mono">services/match-engine/</span>
      </div>
      <div className="content-card-body">
        <p
          style={{
            fontFamily: "var(--font-mono)",
            fontSize: "0.7rem",
            fontWeight: 600,
            color: "#0071c5",
            textTransform: "uppercase",
            letterSpacing: "0.08em",
            marginBottom: 8,
          }}
        >
          sklearnex — must be first import
        </p>
        <pre
          style={{
            fontSize: "0.78rem",
            background: "#f2f4f7",
            border: "1px solid rgba(192,199,211,0.3)",
            borderRadius: 8,
            padding: "12px 16px",
            lineHeight: 1.7,
            overflowX: "auto",
          }}
        >
          {`from sklearnex import patch_sklearn
patch_sklearn()  # BEFORE all sklearn imports
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity`}
        </pre>

        <p
          style={{
            fontFamily: "var(--font-mono)",
            fontSize: "0.7rem",
            fontWeight: 600,
            color: "#0071c5",
            textTransform: "uppercase",
            letterSpacing: "0.08em",
            marginBottom: 8,
            marginTop: 16,
          }}
        >
          OpenVINO — embedding inference
        </p>
        <pre
          style={{
            fontSize: "0.78rem",
            background: "#f2f4f7",
            border: "1px solid rgba(192,199,211,0.3)",
            borderRadius: 8,
            padding: "12px 16px",
            lineHeight: 1.7,
            overflowX: "auto",
          }}
        >
          {`from openvino.runtime import Core

core = Core()
model = core.read_model("model/embedding.xml")
compiled = core.compile_model(model, "CPU")
# If accuracy_delta > 0.01 → stay FP16, not INT8`}
        </pre>

        <div
          style={{
            marginTop: 14,
            padding: "10px 14px",
            background: "#d3e4ff",
            borderRadius: 8,
            fontSize: "0.82rem",
            color: "#001c38",
            lineHeight: 1.5,
          }}
        >
          <strong>Score formula:</strong> Always imported from{" "}
          <code style={{ fontFamily: "var(--font-mono)", fontSize: "0.78rem" }}>packages/scoring/</code>. Never inline
          or duplicate.
        </div>
      </div>
    </div>
  );
}
