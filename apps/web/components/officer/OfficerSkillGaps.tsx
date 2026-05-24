"use client";

import type { OfficerSkillGapItem } from "../../lib/api";

type OfficerSkillGapsProps = {
  items: OfficerSkillGapItem[];
};

export function OfficerSkillGaps({ items }: OfficerSkillGapsProps) {
  const max = items[0]?.student_count ?? 1;

  return (
    <div className="content-card">
      <div className="content-card-header">
        <h2 className="content-card-title">Top skill gaps</h2>
        <span className="chip chip-mono">From scorecards</span>
      </div>
      <div className="content-card-body">
        {items.length === 0 ? (
          <p style={{ fontFamily: "var(--font-mono)", fontSize: "0.8rem", color: "#717783" }}>
            No missing-skill signals yet.
          </p>
        ) : (
          <ul style={{ listStyle: "none", margin: 0, padding: 0, display: "flex", flexDirection: "column", gap: 10 }}>
            {items.map((item) => (
              <li key={item.skill}>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4, fontSize: "0.82rem" }}>
                  <span style={{ fontWeight: 600 }}>{item.skill}</span>
                  <span className="chip chip-mono">{item.student_count} students</span>
                </div>
                <div
                  style={{
                    height: 6,
                    borderRadius: 4,
                    background: "rgba(192,199,211,0.35)",
                    overflow: "hidden",
                  }}
                >
                  <div
                    style={{
                      width: `${Math.max(8, (item.student_count / max) * 100)}%`,
                      height: "100%",
                      background: "linear-gradient(90deg, #0071c5, #4a9eff)",
                    }}
                  />
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
