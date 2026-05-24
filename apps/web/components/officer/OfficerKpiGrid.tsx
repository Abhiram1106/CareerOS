"use client";

import type { OfficerKpis } from "../../modules/officer/types/officer.types";

type OfficerKpiGridProps = {
  kpis: OfficerKpis;
};

export function OfficerKpiGrid({ kpis }: OfficerKpiGridProps) {
  const cards = [
    {
      label: "Students Scored",
      value: String(kpis.students_scored),
      trend: kpis.students_scored > 0 ? "From latest scorecards" : undefined,
    },
    {
      label: "Avg Readiness Score",
      value: String(kpis.avg_readiness),
      suffix: "/100",
      color: "blue" as const,
    },
    {
      label: "Parse-safe Rate",
      value: `${kpis.parse_safe_rate}%`,
      pct: kpis.parse_safe_rate,
    },
    {
      label: "Ready (≥70)",
      value: String(kpis.ready_count),
      note: "Strong + ready buckets",
      color: "blue" as const,
    },
  ];

  return (
    <div className="kpi-grid">
      {cards.map((k) => (
        <div key={k.label} className="kpi-card">
          <div className="kpi-card-header">
            <span className="kpi-label">{k.label}</span>
            <div className="kpi-icon">
              <svg
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
              </svg>
            </div>
          </div>
          <div className={`kpi-value${k.color ? ` ${k.color}` : ""}`}>
            {k.value}
            {k.suffix && (
              <span style={{ fontSize: "1rem", fontWeight: 400, color: "#717783" }}>{k.suffix}</span>
            )}
          </div>
          {k.trend && <div className="kpi-trend">{k.trend}</div>}
          {k.pct !== undefined && (
            <div className="prog-bar" style={{ marginTop: 8 }}>
              <div className="prog-bar-fill" style={{ width: `${Math.min(k.pct, 100)}%` }} />
            </div>
          )}
          {k.note && (
            <p style={{ fontFamily: "var(--font-mono)", fontSize: "0.7rem", color: "#717783", marginTop: 6 }}>
              {k.note}
            </p>
          )}
        </div>
      ))}
    </div>
  );
}
