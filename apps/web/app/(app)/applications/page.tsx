"use client";

import { useCallback, useEffect, useState } from "react";
import type { JobApplication } from "../../../lib/api";
import { api } from "../../../lib/api";
import { getStoredAuth } from "../../../lib/auth";
import { toErrorMessage } from "../../../lib/errors";

const STATUSES: { value: JobApplication["status"]; label: string; color: string; bg: string }[] = [
  { value: "saved",      label: "Saved",      color: "#5c6570", bg: "#f4f6f9" },
  { value: "applied",    label: "Applied",    color: "#0071c5", bg: "#e0f0ff" },
  { value: "screening",  label: "Screening",  color: "#7c3aed", bg: "#f3f0ff" },
  { value: "interview",  label: "Interview",  color: "#d97706", bg: "#fffbeb" },
  { value: "offer",      label: "Offer",      color: "#16a34a", bg: "#f0fdf4" },
  { value: "rejected",   label: "Rejected",   color: "#dc2626", bg: "#fef2f2" },
];

function StatusBadge({ status }: { status: JobApplication["status"] }) {
  const s = STATUSES.find((x) => x.value === status) ?? STATUSES[0];
  return (
    <span style={{
      fontSize: "0.72rem", fontWeight: 700, padding: "2px 9px",
      borderRadius: 9999, color: s.color, background: s.bg,
      border: `1px solid ${s.color}33`,
    }}>
      {s.label}
    </span>
  );
}

function AppCard({
  app,
  onStatusChange,
  onDelete,
}: {
  app: JobApplication;
  onStatusChange: (id: number, status: JobApplication["status"]) => Promise<void>;
  onDelete: (id: number) => Promise<void>;
}) {
  const [updating, setUpdating] = useState(false);

  async function handleStatus(e: React.ChangeEvent<HTMLSelectElement>) {
    setUpdating(true);
    await onStatusChange(app.id, e.target.value as JobApplication["status"]);
    setUpdating(false);
  }

  return (
    <div className="content-card" style={{ marginBottom: 12 }}>
      <div className="content-card-header">
        <div style={{ flex: 1 }}>
          <p style={{ fontWeight: 700, fontSize: "0.92rem", color: "#1a1c20", marginBottom: 2 }}>
            {app.job_title || "Untitled role"}
          </p>
          <p style={{ fontSize: "0.8rem", color: "#5c6570" }}>
            {app.company || "Unknown company"}
            {app.applied_at ? ` · Applied ${new Date(app.applied_at).toLocaleDateString("en-IN")}` : ""}
          </p>
        </div>
        <StatusBadge status={app.status} />
      </div>
      <div className="content-card-body" style={{ paddingTop: 10 }}>
        <div style={{ display: "flex", gap: 10, flexWrap: "wrap", alignItems: "center" }}>
          <div className="auth-field" style={{ margin: 0, flex: "0 0 auto" }}>
            <label className="auth-label" style={{ marginBottom: 4 }} htmlFor={`status-${app.id}`}>
              Update status
            </label>
            <select
              id={`status-${app.id}`}
              className="auth-input workspace-select"
              style={{ minWidth: 140 }}
              value={app.status}
              onChange={handleStatus}
              disabled={updating}
            >
              {STATUSES.map((s) => (
                <option key={s.value} value={s.value}>{s.label}</option>
              ))}
            </select>
          </div>

          {app.apply_url && (
            <a
              href={app.apply_url}
              target="_blank"
              rel="noreferrer"
              className="btn-secondary"
              style={{ fontSize: "0.8rem", textDecoration: "none", alignSelf: "flex-end" }}
            >
              Apply ↗
            </a>
          )}

          <button
            type="button"
            className="btn-secondary"
            style={{ fontSize: "0.78rem", color: "#dc2626", borderColor: "#fca5a5", alignSelf: "flex-end" }}
            onClick={() => void onDelete(app.id)}
          >
            Remove
          </button>
        </div>
      </div>
    </div>
  );
}

function Column({
  status,
  apps,
  onStatusChange,
  onDelete,
}: {
  status: typeof STATUSES[0];
  apps: JobApplication[];
  onStatusChange: (id: number, status: JobApplication["status"]) => Promise<void>;
  onDelete: (id: number) => Promise<void>;
}) {
  return (
    <div style={{
      flex: "1 1 200px", minWidth: 200,
      background: status.bg,
      borderRadius: 12, padding: "14px 12px",
      border: `1px solid ${status.color}22`,
    }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
        <span style={{ fontWeight: 700, fontSize: "0.82rem", color: status.color }}>{status.label}</span>
        <span style={{
          background: status.color, color: "#fff", borderRadius: 9999,
          fontSize: "0.7rem", fontWeight: 700, padding: "1px 7px",
        }}>
          {apps.length}
        </span>
      </div>
      {apps.length === 0 ? (
        <p style={{ fontSize: "0.78rem", color: "#a0a8b0", textAlign: "center", padding: "12px 0" }}>
          None yet
        </p>
      ) : (
        apps.map((app) => (
          <AppCard key={app.id} app={app} onStatusChange={onStatusChange} onDelete={onDelete} />
        ))
      )}
    </div>
  );
}

export default function ApplicationsPage() {
  const token = getStoredAuth()?.token ?? "";
  const [apps, setApps] = useState<JobApplication[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [view, setView] = useState<"kanban" | "list">("kanban");

  const load = useCallback(async () => {
    if (!token) return;
    try {
      const res = await api.listApplications(token);
      setApps(res.applications);
    } catch (err) {
      setError(toErrorMessage(err, "Could not load applications"));
    } finally {
      setLoading(false);
    }
  }, [token]);

  useEffect(() => { void load(); }, [load]);

  const handleStatusChange = useCallback(async (id: number, status: JobApplication["status"]) => {
    try {
      const updated = await api.updateApplication(token, id, { status });
      setApps((prev) => prev.map((a) => a.id === id ? { ...a, ...updated } : a));
    } catch (err) {
      setError(toErrorMessage(err, "Could not update status"));
    }
  }, [token]);

  const handleDelete = useCallback(async (id: number) => {
    try {
      await api.deleteApplication(token, id);
      setApps((prev) => prev.filter((a) => a.id !== id));
    } catch (err) {
      setError(toErrorMessage(err, "Could not remove application"));
    }
  }, [token]);

  const byStatus = (status: string) => apps.filter((a) => a.status === status);
  const total = apps.length;
  const active = apps.filter((a) => !["rejected"].includes(a.status)).length;

  if (loading) {
    return (
      <div className="page-canvas">
        <div className="content-card"><div className="content-card-body">Loading applications…</div></div>
      </div>
    );
  }

  return (
    <div className="page-canvas">
      <div className="page-title-row">
        <div>
          <h1 className="page-title">My Applications</h1>
          <p className="page-subtitle">
            {total} saved · {active} active
          </p>
        </div>
        <div style={{ display: "flex", gap: 8, alignSelf: "center" }}>
          <button
            type="button"
            className={view === "kanban" ? "btn-primary" : "btn-secondary"}
            style={{ fontSize: "0.8rem", padding: "6px 14px" }}
            onClick={() => setView("kanban")}
          >
            Kanban
          </button>
          <button
            type="button"
            className={view === "list" ? "btn-primary" : "btn-secondary"}
            style={{ fontSize: "0.8rem", padding: "6px 14px" }}
            onClick={() => setView("list")}
          >
            List
          </button>
        </div>
      </div>

      {error && (
        <div className="content-card" style={{ marginBottom: 16 }}>
          <div className="content-card-body" style={{ color: "#93000a" }}>{error}</div>
        </div>
      )}

      {total === 0 ? (
        <div className="content-card">
          <div className="content-card-body scan-empty-state">
            <p>No applications saved yet.</p>
            <a href="/jobs" className="btn-primary" style={{ display: "inline-block", textDecoration: "none", marginTop: 12 }}>
              Browse jobs
            </a>
          </div>
        </div>
      ) : view === "kanban" ? (
        <div style={{ display: "flex", gap: 14, overflowX: "auto", paddingBottom: 8, alignItems: "flex-start" }}>
          {STATUSES.map((s) => (
            <Column
              key={s.value}
              status={s}
              apps={byStatus(s.value)}
              onStatusChange={handleStatusChange}
              onDelete={handleDelete}
            />
          ))}
        </div>
      ) : (
        /* List view */
        <div>
          {apps.map((app) => (
            <AppCard key={app.id} app={app} onStatusChange={handleStatusChange} onDelete={handleDelete} />
          ))}
        </div>
      )}
    </div>
  );
}
