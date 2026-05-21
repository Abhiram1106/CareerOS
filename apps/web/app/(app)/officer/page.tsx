"use client";

import { useState } from "react";

const DEPT_DATA = [
  { name: "Computer Science (CSE)", risk: 24, borderline: 112, ready: 184, strong: 62 },
  { name: "Electronics (ECE)",      risk: 41, borderline: 98,  ready: 86,  strong: 14 },
  { name: "Mechanical",             risk: 65, borderline: 120, ready: 42,  strong: 5  },
  { name: "Civil",                  risk: 52, borderline: 88,  ready: 31,  strong: 3  },
];

const TOP_GAPS = [
  { skill: "SQL / Databases",       count: 312, pct: 72 },
  { skill: "REST API Design",        count: 268, pct: 62 },
  { skill: "Git & Version Control", count: 241, pct: 56 },
  { skill: "OOP Principles",        count: 198, pct: 46 },
  { skill: "System Design basics",  count: 167, pct: 39 },
];

const QUEUE = [
  { name: "Priya Sharma",     dept: "CSE",  score: 48, bucket: "risk",       flags: 2, jd: "Accenture ASE" },
  { name: "Arjun Mehta",      dept: "ECE",  score: 62, bucket: "borderline", flags: 1, jd: "TCS Ninja" },
  { name: "Sunita Rao",       dept: "CSE",  score: 78, bucket: "ready",      flags: 0, jd: "Infosys SP" },
  { name: "Rohan Kumar",      dept: "Mech", score: 34, bucket: "risk",       flags: 3, jd: "L&T ECC" },
  { name: "Divya Pillai",     dept: "CSE",  score: 91, bucket: "strong",     flags: 0, jd: "Google STEP" },
];

const BUCKET_MAP: Record<string, { label: string; cls: string }> = {
  strong:     { label: "Strong",     cls: "bucket-strong" },
  ready:      { label: "Ready",      cls: "bucket-ready" },
  borderline: { label: "Borderline", cls: "bucket-borderline" },
  risk:       { label: "High Risk",  cls: "bucket-risk" },
};

const KPIs = [
  { label: "Students Scanned", value: "1,248", trend: "+12% this week", color: undefined },
  { label: "Avg Readiness Score", value: "64", suffix: "/100", color: "blue" },
  { label: "Parse-safe Rate", value: "72%", pct: 72, color: undefined },
  { label: "Ready (≥70)", value: "342", note: "Target: 500", color: "blue" },
];

export default function OfficerDashboard() {
  const [tab, setTab] = useState<"dashboard" | "queue">("dashboard");

  return (
    <div className="page-canvas">
      {/* Header */}
      <div className="page-title-row">
        <div>
          <h1 className="page-title">Cohort Readiness</h1>
          <p className="page-subtitle">Real-time placement intelligence & AI diagnostics.</p>
        </div>
        <div style={{ display: "flex", gap: 8 }}>
          <span style={{ background: "#001c38", color: "#fff", borderRadius: 9999, padding: "5px 12px", fontFamily: "var(--font-mono)", fontSize: "0.72rem", fontWeight: 500, display: "flex", alignItems: "center", gap: 6 }}>
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <rect x="3" y="4" width="18" height="18" rx="2" /><line x1="16" y1="2" x2="16" y2="6" /><line x1="8" y1="2" x2="8" y2="6" /><line x1="3" y1="10" x2="21" y2="10" />
            </svg>
            Week 4
          </span>
          <span style={{ background: "#f2f4f7", border: "1px solid rgba(192,199,211,0.3)", borderRadius: 9999, padding: "5px 12px", fontFamily: "var(--font-mono)", fontSize: "0.72rem", fontWeight: 500, color: "#16a34a", display: "flex", alignItems: "center", gap: 6 }}>
            <span style={{ width: 7, height: 7, borderRadius: "50%", background: "#16a34a", display: "inline-block" }} className="icon-shimmer" />
            Live
          </span>
        </div>
      </div>

      {/* Tabs */}
      <div style={{ display: "flex", gap: 2, borderBottom: "1px solid rgba(192,199,211,0.4)", marginBottom: 24 }} role="tablist">
        {([["dashboard", "Cohort Intelligence"], ["queue", "Review Queue"]] as const).map(([t, label]) => (
          <button key={t} type="button" role="tab" aria-selected={tab === t} onClick={() => setTab(t)} style={{
            padding: "10px 18px", border: "none", borderBottom: tab === t ? "2px solid #0071c5" : "2px solid transparent",
            background: "transparent", color: tab === t ? "#0071c5" : "#414752", fontWeight: 600, fontSize: "0.88rem", cursor: "pointer", borderRadius: 0,
          }}>
            {label}
          </button>
        ))}
      </div>

      {tab === "dashboard" && (
        <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
          {/* KPI grid */}
          <div className="kpi-grid">
            {KPIs.map(k => (
              <div key={k.label} className="kpi-card">
                <div className="kpi-card-header">
                  <span className="kpi-label">{k.label}</span>
                  <div className="kpi-icon">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
                    </svg>
                  </div>
                </div>
                <div className={`kpi-value${k.color ? ` ${k.color}` : ""}`}>
                  {k.value}{k.suffix && <span style={{ fontSize: "1rem", fontWeight: 400, color: "#717783" }}>{k.suffix}</span>}
                </div>
                {k.trend && <div className="kpi-trend">↑ {k.trend}</div>}
                {k.pct !== undefined && (
                  <div className="prog-bar" style={{ marginTop: 8 }}>
                    <div className="prog-bar-fill" style={{ width: `${k.pct}%` }} />
                  </div>
                )}
                {k.note && <p style={{ fontFamily: "var(--font-mono)", fontSize: "0.7rem", color: "#717783", marginTop: 6 }}>{k.note}</p>}
              </div>
            ))}
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr", gap: 20 }}>
            {/* Dept heatmap */}
            <div className="content-card">
              <div className="content-card-header">
                <h2 className="content-card-title">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0071c5" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <rect x="3" y="3" width="7" height="7" /><rect x="14" y="3" width="7" height="7" /><rect x="14" y="14" width="7" height="7" /><rect x="3" y="14" width="7" height="7" />
                  </svg>
                  Department Readiness
                </h2>
                <button type="button" style={{ fontSize: "0.82rem", color: "#0071c5", fontWeight: 600, background: "none", border: "none", cursor: "pointer" }}>View Full Matrix →</button>
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
                    {DEPT_DATA.map(d => {
                      const total = d.risk + d.borderline + d.ready + d.strong;
                      const riskPct = (d.risk / total) * 100;
                      return (
                        <tr key={d.name}>
                          <td style={{ fontWeight: 600 }}>{d.name}</td>
                          <td style={{ textAlign: "center" }}>
                            <span style={{ display: "block", background: `rgba(186,26,26,${Math.min(0.1 + riskPct * 0.008, 0.5)})`, color: "#ba1a1a", borderRadius: 4, padding: "3px 8px", fontFamily: "var(--font-mono)", fontSize: "0.78rem", border: "1px solid rgba(186,26,26,0.1)" }}>{d.risk}</span>
                          </td>
                          <td style={{ textAlign: "center" }}>
                            <span style={{ display: "block", background: "rgba(236,238,241,0.6)", color: "#414752", borderRadius: 4, padding: "3px 8px", fontFamily: "var(--font-mono)", fontSize: "0.78rem", border: "1px solid rgba(192,199,211,0.2)" }}>{d.borderline}</span>
                          </td>
                          <td style={{ textAlign: "center" }}>
                            <span style={{ display: "block", background: "rgba(0,93,127,0.08)", color: "#005d7f", borderRadius: 4, padding: "3px 8px", fontFamily: "var(--font-mono)", fontSize: "0.78rem", border: "1px solid rgba(0,93,127,0.1)" }}>{d.ready}</span>
                          </td>
                          <td style={{ textAlign: "center" }}>
                            <span style={{ display: "block", background: "#d3e4ff", color: "#00589c", borderRadius: 4, padding: "3px 8px", fontFamily: "var(--font-mono)", fontSize: "0.78rem", border: "1px solid rgba(0,88,156,0.2)" }}>{d.strong}</span>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Top skill gaps */}
            <div className="content-card">
              <div className="content-card-header">
                <h2 className="content-card-title">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0071c5" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <line x1="12" y1="20" x2="12" y2="10" /><line x1="18" y1="20" x2="18" y2="4" /><line x1="6" y1="20" x2="6" y2="16" />
                  </svg>
                  Top Skill Gaps
                </h2>
              </div>
              <div className="content-card-body">
                {TOP_GAPS.map(g => (
                  <div key={g.skill} style={{ marginBottom: 14 }}>
                    <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 5 }}>
                      <span style={{ fontSize: "0.86rem", fontWeight: 600, color: "#191c1e" }}>{g.skill}</span>
                      <span style={{ fontFamily: "var(--font-mono)", fontSize: "0.72rem", color: "#ba1a1a" }}>{g.count} missing</span>
                    </div>
                    <div className="prog-bar">
                      <div className="prog-bar-fill" style={{ width: `${g.pct}%`, background: "#ba1a1a" }} />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {tab === "queue" && (
        <div className="content-card">
          <div className="content-card-header">
            <h2 className="content-card-title">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0071c5" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M9 11l3 3L22 4" /><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11" />
              </svg>
              Proof-linked Approval Queue
            </h2>
            <span className="chip chip-warn">{QUEUE.filter(q => q.bucket === "risk").length} high-risk need review</span>
          </div>
          <div className="content-card-body" style={{ padding: "0 0 4px" }}>
            <table className="stitch-table">
              <thead>
                <tr>
                  <th>Student</th>
                  <th>Dept</th>
                  <th>Target JD</th>
                  <th>Score</th>
                  <th>ATS Flags</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {QUEUE.map(s => {
                  const b = BUCKET_MAP[s.bucket];
                  return (
                    <tr key={s.name}>
                      <td style={{ fontWeight: 600 }}>{s.name}</td>
                      <td><span className="chip chip-mono">{s.dept}</span></td>
                      <td style={{ color: "#414752" }}>{s.jd}</td>
                      <td>
                        <span style={{ fontFamily: "var(--font-display)", fontWeight: 700, color: "#191c1e" }}>{s.score}</span>
                        <span className={`bucket-badge ${b.cls}`} style={{ marginLeft: 8 }}>{b.label}</span>
                      </td>
                      <td>
                        {s.flags > 0
                          ? <span className="chip chip-danger">{s.flags} flag{s.flags > 1 ? "s" : ""}</span>
                          : <span className="chip chip-success">Clean</span>}
                      </td>
                      <td>
                        <div style={{ display: "flex", gap: 6 }}>
                          <button type="button" style={{ padding: "5px 12px", borderRadius: 6, background: "#dcfce7", border: "1px solid rgba(22,163,74,0.2)", color: "#15803d", fontWeight: 600, cursor: "pointer", fontSize: "0.78rem" }}>
                            Approve
                          </button>
                          <button type="button" style={{ padding: "5px 12px", borderRadius: 6, background: "#ffdad6", border: "1px solid rgba(186,26,26,0.2)", color: "#93000a", fontWeight: 600, cursor: "pointer", fontSize: "0.78rem" }}>
                            Return
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
