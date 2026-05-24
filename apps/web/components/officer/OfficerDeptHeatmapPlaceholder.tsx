"use client";

const DEPT_DATA = [
  { name: "Computer Science (CSE)", risk: 24, borderline: 112, ready: 184, strong: 62 },
  { name: "Electronics (ECE)", risk: 41, borderline: 98, ready: 86, strong: 14 },
  { name: "Mechanical", risk: 65, borderline: 120, ready: 42, strong: 5 },
  { name: "Civil", risk: 52, borderline: 88, ready: 31, strong: 3 },
];

/** Department matrix — API-backed heatmap ships with college_id scoping (Phase 4). */
export function OfficerDeptHeatmapPlaceholder() {
  return (
    <div className="content-card">
      <div className="content-card-header">
        <h2 className="content-card-title">Department Readiness</h2>
        <span className="chip chip-mono">Demo matrix</span>
      </div>
      <div className="content-card-body" style={{ padding: "0 0 4px" }}>
        <table className="stitch-table">
          <thead>
            <tr>
              <th>Department</th>
              <th style={{ textAlign: "center", color: "#ba1a1a" }}>High Risk</th>
              <th style={{ textAlign: "center", color: "#d97706" }}>Borderline</th>
              <th style={{ textAlign: "center", color: "#16a34a" }}>Ready</th>
              <th style={{ textAlign: "center", color: "#0071c5" }}>Strong</th>
            </tr>
          </thead>
          <tbody>
            {DEPT_DATA.map((d) => {
              const total = d.risk + d.borderline + d.ready + d.strong;
              const riskPct = total > 0 ? (d.risk / total) * 100 : 0;
              return (
                <tr key={d.name}>
                  <td style={{ fontWeight: 600 }}>{d.name}</td>
                  <td style={{ textAlign: "center" }}>
                    <span
                      style={{
                        display: "block",
                        background: `rgba(186,26,26,${Math.min(0.1 + riskPct * 0.008, 0.5)})`,
                        color: "#ba1a1a",
                        borderRadius: 4,
                        padding: "3px 8px",
                        fontFamily: "var(--font-mono)",
                        fontSize: "0.78rem",
                      }}
                    >
                      {d.risk}
                    </span>
                  </td>
                  <td style={{ textAlign: "center", fontFamily: "var(--font-mono)", fontSize: "0.78rem" }}>
                    {d.borderline}
                  </td>
                  <td style={{ textAlign: "center", fontFamily: "var(--font-mono)", fontSize: "0.78rem" }}>
                    {d.ready}
                  </td>
                  <td style={{ textAlign: "center", fontFamily: "var(--font-mono)", fontSize: "0.78rem" }}>
                    {d.strong}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
