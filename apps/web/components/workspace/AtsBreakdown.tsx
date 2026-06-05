import type { ATSCheck, ATSIssue } from "../../lib/api";

type Props = {
  score: number;
  bucket: string | null;
  checks: ATSCheck[];
  issues: ATSIssue[];
};

const STATUS_COLOR: Record<string, string> = {
  excellent: "#16a34a",
  good: "#0071c5",
  fair: "#d97706",
  poor: "#dc2626",
};

const SEVERITY_COLOR: Record<string, string> = {
  high: "#dc2626",
  medium: "#d97706",
  low: "#717783",
};

export function AtsBreakdown({ score, bucket, checks, issues }: Props) {
  if (checks.length === 0) return null;

  return (
    <div className="content-card">
      <div className="content-card-header">
        <h2 className="content-card-title">ATS Parse-Safety Analysis</h2>
        <span
          className="chip chip-mono"
          style={{ color: STATUS_COLOR[bucket ?? "fair"] ?? "#414752" }}
        >
          {Math.round(score)} · {(bucket ?? "").toUpperCase()}
        </span>
      </div>
      <div className="content-card-body">
        <p style={{ fontSize: "0.82rem", color: "var(--muted)", marginBottom: 14, lineHeight: 1.55 }}>
          Seven weighted checks read the actual extracted text — contact reachability, section
          structure, formatting safety, date consistency, content density, bullet impact, and parse
          cleanliness.
        </p>

        <ul className="score-bars" aria-label="ATS dimension scores" style={{ marginBottom: 18 }}>
          {checks.map((c) => {
            const color = STATUS_COLOR[c.status] ?? "#414752";
            return (
              <li key={c.key} className="score-bar-row">
                <div className="score-bar-meta">
                  <span>{c.label}</span>
                  <span className="score-bar-weight">{Math.round(c.weight * 100)}%</span>
                </div>
                <div className="score-bar-track" role="presentation">
                  <div
                    className="score-bar-fill"
                    style={{ width: `${Math.min(100, Math.max(0, c.score))}%`, background: color }}
                  />
                </div>
                <span className="score-bar-value" style={{ color }}>
                  {Math.round(c.score)}
                </span>
              </li>
            );
          })}
        </ul>

        {issues.length > 0 ? (
          <>
            <p className="section-list-heading">
              Fix these to raise your ATS score ({issues.length})
            </p>
            <ul style={{ listStyle: "none", padding: 0, margin: 0, display: "grid", gap: 10 }}>
              {issues.map((issue) => (
                <li
                  key={`${issue.dimension}-${issue.id}`}
                  style={{
                    border: "1px solid rgba(192,199,211,0.4)",
                    borderLeft: `3px solid ${SEVERITY_COLOR[issue.severity] ?? "var(--muted)"}`,
                    borderRadius: 8,
                    padding: "10px 12px",
                    background: "var(--surface-soft)",
                  }}
                >
                  <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 4 }}>
                    <span
                      style={{
                        fontFamily: "var(--font-mono)",
                        fontSize: "0.66rem",
                        textTransform: "uppercase",
                        letterSpacing: "0.06em",
                        color: SEVERITY_COLOR[issue.severity] ?? "var(--muted)",
                      }}
                    >
                      {issue.severity}
                    </span>
                    <span style={{ fontSize: "0.85rem", color: "var(--ink)", fontWeight: 600 }}>
                      {issue.message}
                    </span>
                  </div>
                  <p style={{ fontSize: "0.82rem", color: "var(--muted)", margin: 0, lineHeight: 1.5 }}>
                    → {issue.fix}
                  </p>
                </li>
              ))}
            </ul>
          </>
        ) : (
          <p style={{ fontSize: "0.85rem", color: "#16a34a", margin: 0 }}>
            No ATS parse-safety issues detected. Your resume is well-structured for automated screening.
          </p>
        )}
      </div>
    </div>
  );
}
