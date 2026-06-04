import { useState } from "react";
import type { JobApplication, JobSearchItem } from "../../lib/api";
import { api } from "../../lib/api";
import { getStoredAuth } from "../../lib/auth";

type Props = {
  job: JobSearchItem;
  onRunAgent: (jobId: number) => void;
  busy?: boolean;
  savedApplication?: JobApplication | null;
  onSaved?: (app: JobApplication) => void;
};

export function JobCard({ job, onRunAgent, busy = false, savedApplication, onSaved }: Props) {
  const token = getStoredAuth()?.token ?? "";
  const [saving, setSaving] = useState(false);
  const [app, setApp] = useState<JobApplication | null>(savedApplication ?? null);

  async function handleSave() {
    if (!token || app) return;
    setSaving(true);
    try {
      const saved = await api.saveApplication(token, {
        job_external_id: job.external_id,
        job_title: job.title,
        company: job.company,
        apply_url: job.apply_url ?? "",
      });
      setApp(saved);
      onSaved?.(saved);
    } catch {
      // noop — button just stays unsaved
    } finally {
      setSaving(false);
    }
  }

  const statusColor: Record<string, string> = {
    saved: "#5c6570",
    applied: "#0071c5",
    screening: "#7c3aed",
    interview: "#16a34a",
    offer: "#15803d",
    rejected: "#dc2626",
  };
  const statusLabel = app?.status
    ? app.status.charAt(0).toUpperCase() + app.status.slice(1)
    : null;

  return (
    <article className="content-card">
      <div className="content-card-header">
        <div style={{ flex: 1 }}>
          <h3 className="content-card-title">{job.title}</h3>
          <p style={{ fontSize: "0.82rem", color: "#5c6570", marginTop: 2 }}>
            <strong>{job.company}</strong> · {job.location}
          </p>
        </div>
        <div style={{ display: "flex", gap: 8, alignItems: "center", flexShrink: 0 }}>
          {statusLabel ? (
            <span
              style={{
                fontSize: "0.72rem", fontWeight: 700, padding: "3px 10px",
                borderRadius: 9999, border: "1px solid",
                color: statusColor[app!.status] ?? "#5c6570",
                borderColor: statusColor[app!.status] ?? "#5c6570",
                background: "transparent",
              }}
            >
              {statusLabel}
            </span>
          ) : null}
          <button
            type="button"
            className={app ? "btn-secondary" : "btn-primary"}
            style={{ fontSize: "0.78rem", padding: "5px 12px" }}
            disabled={saving || !!app}
            onClick={handleSave}
          >
            {saving ? "Saving…" : app ? "✓ Saved" : "Save job"}
          </button>
        </div>
      </div>

      <div className="content-card-body">
        {job.skills_required.length > 0 && (
          <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginBottom: 10 }}>
            {job.skills_required.map((s) => (
              <span key={s} className="chip" style={{ fontSize: "0.75rem" }}>{s}</span>
            ))}
          </div>
        )}
        <p className="scan-intro" style={{ marginBottom: 12, fontSize: "0.83rem", color: "#414752" }}>
          {job.raw_jd_text.length > 200 ? `${job.raw_jd_text.slice(0, 200)}…` : job.raw_jd_text}
        </p>
        <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
          <button type="button" className="btn-secondary" disabled={busy} onClick={() => onRunAgent(job.id)}
            style={{ fontSize: "0.82rem" }}>
            {busy ? "Scoring…" : "Score me against this job"}
          </button>
          {job.apply_url && (
            <a
              href={job.apply_url}
              target="_blank"
              rel="noreferrer"
              className="btn-secondary"
              style={{ fontSize: "0.82rem", textDecoration: "none" }}
            >
              Apply ↗
            </a>
          )}
        </div>
      </div>
    </article>
  );
}
