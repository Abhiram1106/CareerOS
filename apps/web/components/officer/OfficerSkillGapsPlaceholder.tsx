"use client";

const TOP_GAPS = [
  { skill: "SQL / Databases", count: 312, pct: 72 },
  { skill: "REST API Design", count: 268, pct: 62 },
  { skill: "Git & Version Control", count: 241, pct: 56 },
  { skill: "OOP Principles", count: 198, pct: 46 },
  { skill: "System Design basics", count: 167, pct: 39 },
];

/** Cohort skill gaps — aggregated from scorecards in a follow-up read model. */
export function OfficerSkillGapsPlaceholder() {
  return (
    <div className="content-card">
      <div className="content-card-header">
        <h2 className="content-card-title">Top Skill Gaps</h2>
        <span className="chip chip-mono">Demo</span>
      </div>
      <div className="content-card-body">
        {TOP_GAPS.map((g) => (
          <div key={g.skill} style={{ marginBottom: 14 }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 5 }}>
              <span style={{ fontSize: "0.86rem", fontWeight: 600, color: "#191c1e" }}>{g.skill}</span>
              <span style={{ fontFamily: "var(--font-mono)", fontSize: "0.72rem", color: "#ba1a1a" }}>
                {g.count} missing
              </span>
            </div>
            <div className="prog-bar">
              <div className="prog-bar-fill" style={{ width: `${g.pct}%`, background: "#ba1a1a" }} />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
