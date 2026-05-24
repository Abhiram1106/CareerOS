"use client";

import { useState } from "react";

import { getStoredAuth } from "../../lib/auth";
import { downloadOfficerReadinessReport } from "../../modules/officer/services/officerService";

export function OfficerReportDownload() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleDownload() {
    const auth = getStoredAuth();
    if (!auth?.token) {
      setError("Sign in as placement officer to export.");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const blob = await downloadOfficerReadinessReport(auth.token);
      const url = URL.createObjectURL(blob);
      const anchor = document.createElement("a");
      anchor.href = url;
      anchor.download = "cohort-readiness-report.pdf";
      anchor.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Download failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        gap: 12,
        flexWrap: "wrap",
        padding: "12px 14px",
        borderRadius: 10,
        border: "1px solid rgba(0,113,197,0.2)",
        background: "rgba(0,113,197,0.04)",
      }}
    >
      <div style={{ flex: 1, minWidth: 200 }}>
        <p style={{ margin: 0, fontWeight: 600, fontSize: "0.9rem" }}>TPO readiness report</p>
        <p style={{ margin: "4px 0 0", fontSize: "0.78rem", color: "#717783" }}>
          PDF with KPIs, department heatmap, and top skill gaps from live cohort data.
        </p>
      </div>
      <button type="button" className="btn-primary" disabled={loading} onClick={() => void handleDownload()}>
        {loading ? "Generating…" : "Download PDF"}
      </button>
      {error ? (
        <p style={{ width: "100%", margin: 0, fontSize: "0.78rem", color: "#ba1a1a" }} role="alert">
          {error}
        </p>
      ) : null}
    </div>
  );
}
