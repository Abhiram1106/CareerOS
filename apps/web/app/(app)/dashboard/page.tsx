"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { ArrowRight, CheckCircle2, Circle, FileText, Target, Rocket, Sparkles, ShieldCheck } from "lucide-react";
import { api } from "../../../lib/api";
import { getStoredAuth } from "../../../lib/auth";
import { toErrorMessage } from "../../../lib/errors";
import { AnimatedCounter } from "../../../components/ui/AnimatedCounter";
import { TiltCard } from "../../../components/ui/TiltCard";

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
  const color = lastScore >= 70 ? "var(--success)" : lastScore >= 50 ? "var(--warn)" : "var(--accent)";

  return (
    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} aria-label="Score trend sparkline" style={{ overflow: "visible" }}>
      <polyline points={polyline} fill="none" stroke={color} strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
      {scores.map((s, i) => {
        const [x, y] = pts[i].split(",");
        return <circle key={i} cx={x} cy={y} r="3.5" fill="#fff" stroke={color} strokeWidth="2" />;
      })}
      <text x={Number(lastPt[0]) + 8} y={Number(lastPt[1]) + 4} fontSize="12" fontWeight="800" fill={color} style={{ fontFamily: "var(--font-mono)" }}>
        {Math.round(lastScore)}
      </text>
    </svg>
  );
}

const QC_COLOR: Record<string, string> = {
  ats_broken: "var(--danger)", structurally_weak: "var(--warn)", keyword_weak: "#b45309",
  impact_weak: "var(--accent)", role_misaligned: "#7c3aed", high_potential_underwritten: "#9333ea",
  interview_ready: "var(--success)",
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
    <div style={{ marginTop: 24 }}>
      <p style={{ fontSize: "0.74rem", fontWeight: 800, color: "var(--muted-2)", textTransform: "uppercase", letterSpacing: "0.06em", marginBottom: 16 }}>
        Resume Evolution
      </p>
      <div className="evo-track">
        {history.map((h, i) => {
          const color = QC_COLOR[h.quality_class] ?? "var(--muted)";
          const icon = QC_ICON[h.quality_class] ?? "•";
          const label = QC_LABEL[h.quality_class] ?? h.quality_class;
          const isLast = i === history.length - 1;
          return (
            <div key={h.version} style={{ display: "flex", alignItems: "flex-start" }}>
              <div className="evo-node">
                <div 
                  className="evo-circle"
                  title={`v${h.version}: ${label} (${h.overall_score})`}
                  style={{ background: `${color}12`, border: `1.5px solid ${color}`, color }}
                >
                  {icon}
                </div>
                <p className="evo-score" style={{ color }}>
                  {Math.round(h.overall_score)}
                </p>
                <p className="evo-version">v{h.version}</p>
              </div>
              {!isLast && <div className="evo-connector" />}
            </div>
          );
        })}
      </div>
    </div>
  );
}

function ProgressRing({ value }: { value: number }) {
  const clamped = Math.max(0, Math.min(100, value));
  const r = 24;
  const c = 2 * Math.PI * r;
  const d = c - (clamped / 100) * c;
  return (
    <div className="glass-intel" style={{ padding: 12, borderRadius: "50%", display: "flex", alignItems: "center", justifyContent: "center", width: 72, height: 72 }}>
      <svg width="60" height="60" viewBox="0 0 60 60" aria-label={`Profile completeness ${clamped}%`}>
        <circle cx="30" cy="30" r={r} fill="none" stroke="var(--line)" strokeWidth="5" />
        <circle
          cx="30"
          cy="30"
          r={r}
          fill="none"
          stroke="var(--accent)"
          strokeWidth="5"
          strokeLinecap="round"
          strokeDasharray={c}
          strokeDashoffset={d}
          style={{ transition: "stroke-dashoffset 0.8s cubic-bezier(0.22, 1, 0.36, 1)" }}
          transform="rotate(-90 30 30)"
        />
        <text x="30" y="34" textAnchor="middle" fontSize="11" fontWeight="800" fill="var(--accent-ink)" style={{ fontFamily: "var(--font-mono)" }}>
          {clamped}%
        </text>
      </svg>
    </div>
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
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    if (!token) return;
    setLoading(true);
    void api
      .dashboard(token)
      .then((res) => setData(res as DashboardData))
      .catch((err) => setError(toErrorMessage(err, "Could not load dashboard")))
      .finally(() => {
        setLoading(false);
        setTimeout(() => setIsReady(true), 50);
      });
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
    let hasExport = false;
    try {
      const raw = localStorage.getItem("cos_workspace_state_v1");
      if (raw) {
        const s = JSON.parse(raw) as { export_status?: string };
        hasExport = s.export_status === "done";
      }
    } catch { /* ignore */ }
    return [
      { label: "Upload Resume", done: hasResume, href: "/resume", icon: <FileText size={14} /> },
      { label: "Run JD Match", done: hasScan, href: "/match", icon: <Sparkles size={14} /> },
      { label: "Generate Rewrite", done: hasRewrite, href: "/rewrite", icon: <Rocket size={14} /> },
      { label: "Export ATS-safe PDF", done: hasExport, href: "/resume", icon: <ShieldCheck size={14} /> },
    ];
  }, [data?.total_resumes, data?.scans_performed, snapshot?.overall_score]);

  const topGap = snapshot?.missing_skills?.[0];

  if (loading) {
    return (
      <div className="page-canvas">
        <div className="content-card">
          <div className="content-card-body">Loading your dashboard...</div>
        </div>
      </div>
    );
  }

  return (
    <div className={`page-canvas stagger-entry ${isReady ? "stagger-entry-active" : ""}`}>
      <div className="page-title-row delay-1">
        <div>
          <h1 className="page-title">Command Center</h1>
          <p className="page-subtitle">Welcome back, {name}. Your placement readiness at a glance.</p>
        </div>
      </div>

      <div className="bento-grid">
        {/* ── Main Snapshot ── */}
        <TiltCard className="span-3 delay-2" maxTilt={5}>
          <div className="dashboard-hero-row">
            <div>
              <p className="dashboard-score-label">Placement Readiness Score</p>
              <div className="dashboard-score-value" style={{ display: "flex", alignItems: "baseline", gap: 8 }}>
                <AnimatedCounter end={snapshot?.overall_score ?? Math.round(data?.best_ats_score ?? 0)} className="gradient-text score-overall-value" />
                <span style={{ fontSize: "1.2rem", color: "var(--muted-2)", fontWeight: 500 }}>/ 100</span>
              </div>
              <p className={`dashboard-score-sub bucket-badge bucket-${snapshot?.score_bucket === "strong" ? "ready" : snapshot?.score_bucket === "ready" ? "ready" : "risk"}`}>
                {snapshot?.score_bucket?.toUpperCase() ?? "NO DATA"}
              </p>
            </div>
            <ProgressRing value={data?.profile_completeness ?? 0} />
          </div>

          <div className="dashboard-metrics-grid">
            <div className="metric">
              <p>Resumes</p>
              <strong>{data?.total_resumes ?? 0}</strong>
            </div>
            <div className="metric">
              <p>Total Scans</p>
              <strong>{data?.scans_performed ?? 0}</strong>
            </div>
            <div className="metric">
              <p>Data Depth</p>
              <strong>{data?.profile_completeness ?? 0}%</strong>
            </div>
          </div>

          {topGap && (
            <div className="dashboard-gap-callout glass-intel" style={{ marginTop: 24, padding: "16px 20px" }}>
              <Target size={18} color="var(--accent)" />
              <p style={{ fontWeight: 600 }}>
                Top skill gap: <span className="gradient-text">{topGap}</span>
              </p>
              <Link href="/rewrite" className="dashboard-inline-link" style={{ background: "var(--surface)", padding: "6px 12px", borderRadius: 8, boxShadow: "var(--shadow-sm)" }}>
                Fix now <ArrowRight size={14} />
              </Link>
            </div>
          )}
        </TiltCard>

        {/* ── Onboarding ── */}
        <div className="bento-card delay-3">
          <h3 className="section-heading" style={{ fontSize: "1rem", marginBottom: 16 }}>Onboarding</h3>
          <div className="dashboard-checklist">
            {checklist.map((item) => (
              <Link key={item.label} href={item.href} className="dashboard-check-item" style={{ transition: "all 0.2s ease" }}>
                {item.done ? (
                  <CheckCircle2 size={16} color="var(--success)" />
                ) : (
                  <Circle size={16} color="var(--line-strong)" />
                )}
                <span style={{ flex: 1 }}>{item.label}</span>
                <span style={{ opacity: 0.4 }}>{item.icon}</span>
              </Link>
            ))}
          </div>
          <div className="dashboard-actions" style={{ marginTop: 20 }}>
            <Link href="/resume" className="btn-primary btn-block dashboard-action-link" style={{ background: "var(--accent)" }}>
              Continue Journey
            </Link>
          </div>
        </div>

        {/* ── Evolution ── */}
        <div className="bento-card span-2 delay-4">
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 20 }}>
            <h3 className="section-heading" style={{ fontSize: "1rem", margin: 0 }}>Progress Analytics</h3>
            {historyDelta !== null && (
              <span className={`badge badge-${historyDelta >= 0 ? "success" : "danger"}`}>
                {historyDelta >= 0 ? "↑" : "↓"}{Math.abs(historyDelta)} pts
              </span>
            )}
          </div>
          
          {history.length >= 2 ? (
            <>
              <ScoreSparkline history={history} />
              <EvolutionTimeline history={history} />
            </>
          ) : (
            <div className="scan-empty-state" style={{ padding: "40px 0", background: "var(--surface-soft)", borderRadius: 12 }}>
              <p style={{ fontSize: "0.88rem", color: "var(--muted)" }}>Compare resume versions to see your progress.</p>
              <Link href="/match" className="btn-secondary btn-sm" style={{ marginTop: 12 }}>Run another scan</Link>
            </div>
          )}
        </div>

        {/* ── Quick Links ── */}
        <div className="bento-card delay-5" style={{ background: "var(--accent-ink)", color: "#fff" }}>
          <h3 style={{ color: "#fff", fontSize: "1rem", marginBottom: 12 }}>AI Assistant</h3>
          <p style={{ fontSize: "0.86rem", opacity: 0.8, marginBottom: 20, lineHeight: 1.5 }}>
            Need help with your resume or a specific job? Talk to our AI placement advisor.
          </p>
          <Link href="/assistant" className="btn-glass btn-block" style={{ textAlign: "center", color: "#fff" }}>
            Chat Now
          </Link>
        </div>
      </div>
    </div>
  );
}
