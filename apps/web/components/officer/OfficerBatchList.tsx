"use client";

import type { OfficerBatchItem } from "../../modules/officer/types/officer.types";

type OfficerBatchListProps = {
  batches: OfficerBatchItem[];
};

export function OfficerBatchList({ batches }: OfficerBatchListProps) {
  return (
    <div className="content-card">
      <div className="content-card-header">
        <h2 className="content-card-title">Campus batches</h2>
        <span className="chip chip-mono">{batches.length} total</span>
      </div>
      <div className="content-card-body" style={{ padding: "0 0 4px" }}>
        {batches.length === 0 ? (
          <p style={{ padding: 16, fontFamily: "var(--font-mono)", fontSize: "0.8rem", color: "#717783" }}>
            No batches created yet. Batch upload lands in Phase 4.
          </p>
        ) : (
          <table className="stitch-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Grad year</th>
                <th>Created</th>
              </tr>
            </thead>
            <tbody>
              {batches.map((b) => (
                <tr key={b.id}>
                  <td style={{ fontWeight: 600 }}>{b.name}</td>
                  <td>
                    <span className="chip chip-mono">{b.grad_year}</span>
                  </td>
                  <td style={{ fontFamily: "var(--font-mono)", fontSize: "0.78rem", color: "#717783" }}>
                    {new Date(b.created_at).toLocaleDateString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
