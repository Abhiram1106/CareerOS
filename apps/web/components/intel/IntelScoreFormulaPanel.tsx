"use client";

export function IntelScoreFormulaPanel() {
  return (
    <div className="content-card" style={{ marginTop: 20 }}>
      <div className="content-card-header">
        <h2 className="content-card-title">PlacementReadinessScore formula</h2>
        <span className="chip chip-primary">packages/scoring/ — single source of truth</span>
      </div>
      <div className="content-card-body">
        <pre
          style={{
            fontSize: "0.82rem",
            background: "#f2f4f7",
            border: "1px solid rgba(192,199,211,0.3)",
            borderRadius: 8,
            padding: "16px 20px",
            lineHeight: 1.9,
            overflowX: "auto",
          }}
        >
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
  );
}
