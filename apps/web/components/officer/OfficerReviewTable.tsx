"use client";

import { bucketPresentation } from "../../modules/officer/lib/bucketLabels";
import type { OfficerReviewItem } from "../../modules/officer/types/officer.types";

type OfficerReviewTableProps = {
  items: OfficerReviewItem[];
};

export function OfficerReviewTable({ items }: OfficerReviewTableProps) {
  const highRisk = items.filter((q) => q.bucket === "risk" || q.bucket === "high-risk").length;

  return (
    <div className="content-card">
      <div className="content-card-header">
        <h2 className="content-card-title">Proof-linked approval queue</h2>
        {highRisk > 0 && <span className="chip chip-warn">{highRisk} high-risk need review</span>}
      </div>
      <div className="content-card-body" style={{ padding: "0 0 4px" }}>
        {items.length === 0 ? (
          <p style={{ padding: 16, fontFamily: "var(--font-mono)", fontSize: "0.8rem", color: "#717783" }}>
            No students in the queue yet.
          </p>
        ) : (
          <table className="stitch-table">
            <thead>
              <tr>
                <th>Student</th>
                <th>Target role</th>
                <th>Score</th>
                <th>Bucket</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {items.map((s) => {
                const b = bucketPresentation(s.bucket);
                return (
                  <tr key={s.scorecard_id}>
                    <td style={{ fontWeight: 600 }}>{s.student_name}</td>
                    <td style={{ color: "#414752" }}>{s.target_role}</td>
                    <td>
                      <span style={{ fontFamily: "var(--font-display)", fontWeight: 700 }}>{s.overall_score}</span>
                    </td>
                    <td>
                      <span className={`bucket-badge ${b.className}`}>{b.label}</span>
                    </td>
                    <td>
                      <div style={{ display: "flex", gap: 6 }}>
                        <button
                          type="button"
                          style={{
                            padding: "5px 12px",
                            borderRadius: 6,
                            background: "#dcfce7",
                            border: "1px solid rgba(22,163,74,0.2)",
                            color: "#15803d",
                            fontWeight: 600,
                            cursor: "pointer",
                            fontSize: "0.78rem",
                          }}
                        >
                          Approve
                        </button>
                        <button
                          type="button"
                          style={{
                            padding: "5px 12px",
                            borderRadius: 6,
                            background: "#ffdad6",
                            border: "1px solid rgba(186,26,26,0.2)",
                            color: "#93000a",
                            fontWeight: 600,
                            cursor: "pointer",
                            fontSize: "0.78rem",
                          }}
                        >
                          Return
                        </button>
                      </div>
                    </td>
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
