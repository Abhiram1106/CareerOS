"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { ArrowRight, CheckCircle2, Circle, Target } from "lucide-react";
import { api } from "../../../lib/api";
import { getStoredAuth } from "../../../lib/auth";
import { toErrorMessage } from "../../../lib/errors";

type DashboardData = {
  best_ats_score: number;
  total_resumes: number;
  scans_performed: number;
  profile_completeness: number;
};

type StoredSnapshot = {
  score_snapshot: {
    overall_score: number;
    score_bucket: string | null;
    missing_skills: string[];
  } | null;
};

function ProgressRing({ value }: { value: number }) {
  const clamped = Math.max(0, Math.min(100, value));
  const r = 28;
  const c = 2 * Math.PI * r;
  const d = c - (clamped / 100) * c;
  return (
    <svg width="70" height="70" viewBox="0 0 70 70" aria-label={`Profile completeness ${clamped}%`}>
      <circle cx="35" cy="35" r={r} fill="none" stroke="#e8ecf2" strokeWidth="7" />
      <circle
        cx="35"
        cy="35"
        r={r}
        fill="none"
        stroke="#0071c5"
        strokeWidth="7"
        strokeLinecap="round"
        strokeDasharray={c}
        strokeDashoffset={d}
        transform="rotate(-90 35 35)"
      />
      <text x="35" y="39" textAnchor="middle" fontSize="13" fontWeight="700" fill="#00589c">
        {clamped}%
      </text>
    </svg>
  );
}

export default function DashboardPage() {
  const token = getStoredAuth()?.token ?? "";
  const name = getStoredAuth()?.full_name?.split(" ")[0] ?? "there";

  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [snapshot, setSnapshot] = useState<StoredSnapshot["score_snapshot"]>(null);

  useEffect(() => {
    if (!token) return;
    setLoading(true);
    void api
      .dashboard(token)
      .then((res) => setData(res as DashboardData))
      .catch((err) => setError(toErrorMessage(err, "Could not load dashboard")))
      .finally(() => setLoading(false));
  }, [token]);

  useEffect(() => {
    try {
      const raw = localStorage.getItem("cos_workspace_state_v1");
      if (!raw) return;
      const parsed = JSON.parse(raw) as StoredSnapshot;
      setSnapshot(parsed.score_snapshot);
    } catch {
      setSnapshot(null);
    }
  }, []);

  const checklist = useMemo(() => {
    const hasResume = (data?.total_resumes ?? 0) > 0;
    const hasScan = (data?.scans_performed ?? 0) > 0;
    const hasRewrite = Boolean(snapshot?.overall_score && snapshot.overall_score > 0);
    // Export done = a completed export job exists in localStorage state
    let hasExport = false;
    try {
      const raw = localStorage.getItem("cos_workspace_state_v1");
      if (raw) {
        const s = JSON.parse(raw) as { export_status?: string };
        hasExport = s.export_status === "done";
      }
    } catch { /* ignore */ }
    return [
      { label: "Upload Resume", done: hasResume, href: "/resume" },
      { label: "Run JD Match", done: hasScan, href: "/match" },
      { label: "Generate Rewrite", done: hasRewrite, href: "/rewrite" },
      { label: "Export ATS-safe PDF", done: hasExport, href: "/resume" },
    ];
  }, [data?.total_resumes, data?.scans_performed, snapshot?.overall_score]);

  const topGap = snapshot?.missing_skills?.[0];

  return (
    <div className="page-canvas">
      <div className="page-title-row">
        <div>
          <h1 className="page-title">Dashboard</h1>
          <p className="page-subtitle">Welcome back, {name}. Here is your placement readiness command center.</p>
        </div>
      </div>

      {loading ? (
        <div className="content-card">
          <div className="content-card-body">Loading your dashboard...</div>
        </div>
      ) : error ? (
        <div className="content-card">
          <div className="content-card-body" style={{ color: "#93000a" }}>
            {error}
          </div>
        </div>
      ) : (
        <div className="dashboard-layout">
          <section className="content-card">
            <div className="content-card-header">
              <h2 className="content-card-title">Readiness Snapshot</h2>
            </div>
            <div className="content-card-body">
              <div className="dashboard-hero-row">
                <div>
                  <p className="dashboard-score-label">Latest Readiness Score</p>
                  <p className="dashboard-score-value">{snapshot?.overall_score ?? Math.round(data?.best_ats_score ?? 0)}</p>
                  <p className="dashboard-score-sub">{snapshot?.score_bucket ?? "Run a JD scan to generate your first score"}</p>
                </div>
                <ProgressRing value={data?.profile_completeness ?? 0} />
              </div>

              <div className="dashboard-metrics-grid">
                <div className="dashboard-metric">
                  <p>Resumes</p>
                  <strong>{data?.total_resumes ?? 0}</strong>
                </div>
                <div className="dashboard-metric">
                  <p>Scans</p>
                  <strong>{data?.scans_performed ?? 0}</strong>
                </div>
                <div className="dashboard-metric">
                  <p>Completeness</p>
                  <strong>{data?.profile_completeness ?? 0}%</strong>
                </div>
              </div>

              {topGap ? (
                <div className="dashboard-gap-callout">
                  <Target size={16} />
                  <p>
                    Top skill gap: <strong>{topGap}</strong>. Improve it with a proof-linked rewrite.
                  </p>
                  <Link href="/rewrite" className="dashboard-inline-link">
                    Fix now <ArrowRight size={14} />
                  </Link>
                </div>
              ) : null}
            </div>
          </section>

          <section className="content-card">
            <div className="content-card-header">
              <h2 className="content-card-title">Onboarding Checklist</h2>
            </div>
            <div className="content-card-body">
              <div className="dashboard-checklist">
                {checklist.map((item) => (
                  <Link key={item.label} href={item.href} className="dashboard-check-item">
                    {item.done ? (
                      <CheckCircle2 size={16} color="#16a34a" />
                    ) : (
                      <Circle size={16} color="#717783" />
                    )}
                    <span>{item.label}</span>
                  </Link>
                ))}
              </div>
              <div className="dashboard-actions">
                <Link href="/resume" className="btn-primary dashboard-action-link">
                  Continue journey
                </Link>
                <Link href="/assistant" className="btn-secondary dashboard-action-link">
                  Ask assistant
                </Link>
              </div>
            </div>
          </section>
        </div>
      )}
    </div>
  );
}
