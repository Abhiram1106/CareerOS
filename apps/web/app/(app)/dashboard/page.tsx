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

function ScoreSparkline({ history }: { history: { overall_score: number; date: string }[] }) {
  if (history.length < 2) return null;
  const W = 280, H = 56, PAD = 6;
  const scores = history.map((h) => h.overall_score);
  const min = Math.max(0, Math.min(...scores) - 5);
  const max = Math.min(100, Math.max(...scores) + 5);
  const range = max - min || 1;
  const xStep = (W - PAD * 2) / (scores.length - 1);

  const pts = scores.map((s, i) => {
    const x = PAD + i * xStep;
    const y = H - PAD - ((s - min) / range) * (H - PAD * 2);
    return `${x},${y}`;
  });
  const polyline = pts.join(" ");
  const lastPt = pts[pts.length - 1].split(",");
  const lastScore = scores[scores.length - 1];
  const color = lastScore >= 70 ? "#16a34a" : lastScore >= 50 ? "#d97706" : "#0071c5";

  return (
    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} aria-label="Score trend sparkline" style={{ overflow: "visible" }}>
      <polyline points={polyline} fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      {scores.map((s, i) => {
        const [x, y] = pts[i].split(",");
        return <circle key={i} cx={x} cy={y} r="3" fill={color} />;
      })}
      <text x={Number(lastPt[0]) + 6} y={Number(lastPt[1]) + 4} fontSize="11" fontWeight="700" fill={color}>
        {Math.round(lastScore)}
      </text>
    </svg>
  );
}

// CARE-RAG M12: Resume Evolution Timeline
const QC_COLOR: Record<string, string> = {
  ats_broken: "#dc2626", structurally_weak: "#d97706", keyword_weak: "#b45309",
  impact_weak: "#0284c7", role_misaligned: "#7c3aed", high_potential_underwritten: "#9333ea",
  interview_ready: "#16a34a",
};
const QC_ICON: Record<string, string> = {
  ats_broken: "⛔", structurally_weak: "⚠️", keyword_weak: "🔍",
  impact_weak: "📉", role_misaligned: "🎯", high_potential_underwritten: "💎",
  interview_ready: "✅",
};
const QC_LABEL: Record<string, string> = {
  ats_broken: "ATS Broken", structurally_weak: "Structurally Weak",
  keyword_weak: "Keyword Weak", impact_weak: "Impact Weak",
  role_misaligned: "Role Misaligned", high_potential_underwritten: "High Potential",
  interview_ready: "Interview Ready",
};

function EvolutionTimeline({ history }: {
  history: { version: number; overall_score: number; quality_class: string; date: string }[];
}) {
  if (history.length < 2) return null;
  return (
    <div style={{ marginTop: 20 }}>
      <p style={{ fontSize: "0.82rem", fontWeight: 700, color: "#414752", marginBottom: 12 }}>
        Resume evolution ({history.length} versions)
      </p>
      <div style={{ display: "flex", alignItems: "flex-start", gap: 0, overflowX: "auto", paddingBottom: 4 }}>
        {history.map((h, i) => {
          const color = QC_COLOR[h.quality_class] ?? "#5c6570";
          const icon = QC_ICON[h.quality_class] ?? "•";
          const label = QC_LABEL[h.quality_class] ?? h.quality_class;
          const isLast = i === history.length - 1;
          return (
            <div key={h.version} style={{ display: "flex", alignItems: "flex-start", minWidth: 0 }}>
              <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
                <div title={`v${h.version}: ${label} (${h.overall_score})`}
                  style={{ width: 32, height: 32, borderRadius: "50%", background: `${color}18`, border: `2px solid ${color}`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: "0.9rem", flexShrink: 0 }}>
                  {icon}
                </div>
                <p style={{ fontSize: "0.68rem", color, fontWeight: 700, margin: "4px 0 0", textAlign: "center", whiteSpace: "nowrap" }}>
                  {Math.round(h.overall_score)}
                </p>
                <p style={{ fontSize: "0.62rem", color: "#8a95a2", margin: 0, textAlign: "center", whiteSpace: "nowrap" }}>
                  v{h.version}
                </p>
              </div>
              {!isLast && (
                <div style={{ height: 2, background: "#e8ecf2", flex: 1, marginTop: 15, minWidth: 20, maxWidth: 40 }} />
              )}
            </div>
          );
        })}
      </div>
      {history[history.length - 1].quality_class === "interview_ready" && (
        <p style={{ fontSize: "0.75rem", color: "#16a34a", fontWeight: 700, marginTop: 8 }}>
          🏆 You reached Interview Ready status!
        </p>
      )}
    </div>
  );
}

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
  const [history, setHistory] = useState<{ scorecard_id: number; version: number; overall_score: number; bucket: string; quality_class: string; date: string }[]>([]);
  const [historyDelta, setHistoryDelta] = useState<number | null>(null);

  useEffect(() => {
    if (!token) return;
    setLoading(true);
    void api
      .dashboard(token)
      .then((res) => setData(res as DashboardData))
      .catch((err) => setError(toErrorMessage(err, "Could not load dashboard")))
      .finally(() => setLoading(false));
    void api
      .scoreHistory(token)
      .then((res) => {
        setHistory(res.history);
        setHistoryDelta(res.delta);
      })
      .catch(() => { /* non-blocking */ });
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

              {/* ── Score trend sparkline ── */}
              {history.length >= 2 ? (
                <div style={{ marginTop: 16 }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 6 }}>
                    <p style={{ fontSize: "0.8rem", fontWeight: 600, color: "#414752" }}>Score trend ({history.length} scans)</p>
                    {historyDelta !== null && (
                      <span style={{
                        fontSize: "0.78rem", fontWeight: 700, padding: "2px 8px", borderRadius: 9999,
                        color: historyDelta >= 0 ? "#16a34a" : "#dc2626",
                        background: historyDelta >= 0 ? "#f0fdf4" : "#fef2f2",
                      }}>
                        {historyDelta >= 0 ? "↑" : "↓"}{Math.abs(historyDelta)} pts overall
                      </span>
                    )}
                  </div>
                  <ScoreSparkline history={history} />
                </div>
              ) : null}

              {/* CARE-RAG M12: Resume Evolution Timeline */}
              <EvolutionTimeline history={history} />
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
