"use client";

import type { OfficerBuckets } from "../../modules/officer/types/officer.types";

type OfficerBucketSummaryProps = {
  buckets: OfficerBuckets;
};

const ROWS: Array<{ key: keyof OfficerBuckets; label: string; color: string }> = [
  { key: "risk", label: "High Risk", color: "#ba1a1a" },
  { key: "borderline", label: "Borderline", color: "#d97706" },
  { key: "ready", label: "Ready", color: "#16a34a" },
  { key: "strong", label: "Strong", color: "#0071c5" },
];

export function OfficerBucketSummary({ buckets }: OfficerBucketSummaryProps) {
  const total = buckets.risk + buckets.borderline + buckets.ready + buckets.strong;

  return (
    <div className="content-card">
      <div className="content-card-header">
        <h2 className="content-card-title">Readiness buckets</h2>
      </div>
      <div className="content-card-body">
        {total === 0 ? (
          <p style={{ fontFamily: "var(--font-mono)", fontSize: "0.8rem", color: "#717783" }}>
            No scored students yet. Students need at least one JD scorecard.
          </p>
        ) : (
          <table className="stitch-table">
            <thead>
              <tr>
                <th>Bucket</th>
                <th style={{ textAlign: "center" }}>Count</th>
                <th style={{ textAlign: "center" }}>Share</th>
              </tr>
            </thead>
            <tbody>
              {ROWS.map((row) => {
                const count = buckets[row.key];
                const pct = total > 0 ? Math.round((count / total) * 100) : 0;
                return (
                  <tr key={row.key}>
                    <td style={{ fontWeight: 600, color: row.color }}>{row.label}</td>
                    <td style={{ textAlign: "center", fontFamily: "var(--font-mono)" }}>{count}</td>
                    <td style={{ textAlign: "center", fontFamily: "var(--font-mono)" }}>{pct}%</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
