"use client";

import { useState, useCallback, useEffect } from "react";
import Link from "next/link";
import { usePlacementWorkspace } from "../../../../hooks/usePlacementWorkspace";
import { ScoreBreakdown } from "../../../../components/workspace/ScoreBreakdown";
import { RewriteDiffPanel } from "../../../../components/workspace/RewriteDiffPanel";
import type { QualityClassInfo } from "../../../../lib/api";
import { api } from "../../../../lib/api";
import { getStoredAuth } from "../../../../lib/auth";

// ── Role-based success patterns (CARE-RAG Layer 3 stub — rule-based for MVP) ─

type RolePattern = {
  role: string;
  keywords: string[];
  bullet_example: string;
  typical_scores: { evidence: number; completeness: number; jd_match: number };
};

const ROLE_PATTERNS: Record<string, RolePattern> = {
  backend: {
    role: "Backend Engineer",
    keywords: ["REST API", "Docker", "SQL", "microservices", "Python/Java/Go"],
    bullet_example: "Built a payment service in Python + FastAPI, reducing p95 latency by 40% and serving 2M requests/day.",
    typical_scores: { evidence: 72, completeness: 85, jd_match: 68 },
  },
  frontend: {
    role: "Frontend Developer",
    keywords: ["React", "TypeScript", "REST API", "responsive design", "state management"],
    bullet_example: "Built a dashboard in React + TypeScript, improving load time by 35% and supporting 50K daily active users.",
    typical_scores: { evidence: 68, completeness: 80, jd_match: 65 },
  },
  data: {
    role: "Data Analyst / Data Scientist",
    keywords: ["Python", "SQL", "Pandas", "dashboard", "Power BI / Tableau", "business metrics"],
    bullet_example: "Analyzed 50M order rows in SQL, built a Tableau dashboard used by 12 stakeholders, and cut report latency by 25%.",
    typical_scores: { evidence: 70, completeness: 82, jd_match: 66 },
  },
  devops: {
    role: "DevOps / Cloud Engineer",
    keywords: ["Docker", "Kubernetes", "CI/CD", "AWS/GCP/Azure", "Terraform", "monitoring"],
    bullet_example: "Set up a GitHub Actions CI/CD pipeline, reducing deploy time from 45 min to 8 min across 3 microservices.",
    typical_scores: { evidence: 74, completeness: 80, jd_match: 70 },
  },
  default: {
    role: "Software Engineer",
    keywords: ["problem solving", "APIs", "databases", "version control", "testing"],
    bullet_example: "Designed and deployed a service that reduced manual processing by 60%, saving 8 hours/week across the team.",
    typical_scores: { evidence: 68, completeness: 80, jd_match: 64 },
  },
};

function detectRole(targetRole: string, matchedSkills: string[]): RolePattern {
  const combined = `${targetRole} ${matchedSkills.join(" ")}`.toLowerCase();
  if (/front|react|vue|angular|ui|ux|css|html/.test(combined)) return ROLE_PATTERNS.frontend;
  if (/data|analyst|scientist|ml|machine|pandas|tableau|power bi/.test(combined)) return ROLE_PATTERNS.data;
  if (/devops|cloud|infra|kubernetes|terraform|aws|gcp|azure|ci.cd/.test(combined)) return ROLE_PATTERNS.devops;
  if (/backend|server|api|django|fastapi|spring|node|java/.test(combined)) return ROLE_PATTERNS.backend;
  return ROLE_PATTERNS.default;
}

// ── Score gap analysis → recommendations ─────────────────────────────────────

type Recommendation = {
  id: string;
  priority: number;
  title: string;
  detail: string;
  estimated_delta: number;
  action: "rewrite" | "add_content" | "fix_format" | "add_keywords";
  section?: string;
};

function buildRecommendations(
  barScores: Record<string, number>,
  qualityClass: QualityClassInfo,
  missingSkills: string[],
): Recommendation[] {
  const recs: Recommendation[] = [];

  if ((barScores.evidence ?? 100) < 55) {
    recs.push({
      id: "evidence",
      priority: 1,
      title: "Add metrics to your bullets",
      detail: "Replace vague bullets like 'Built X' with 'Built X, reducing Y by Z%'. Quantified bullets are the single biggest score driver.",
      estimated_delta: Math.round((55 - (barScores.evidence ?? 55)) * 0.20),
      action: "rewrite",
      section: "experience",
    });
  }

  if ((barScores.jd_match ?? 100) < 55 && missingSkills.length > 0) {
    recs.push({
      id: "keywords",
      priority: 2,
      title: `Add ${missingSkills.slice(0, 3).join(", ")} to your resume`,
      detail: `These JD keywords are missing. Add them to your Skills section and mention them naturally in relevant bullets.`,
      estimated_delta: Math.round((55 - (barScores.jd_match ?? 55)) * 0.35),
      action: "add_keywords",
    });
  }

  if ((barScores.completeness ?? 100) < 60) {
    recs.push({
      id: "completeness",
      priority: 3,
      title: "Fill in incomplete profile sections",
      detail: "Your resume is missing key sections. Go to Profile → Settings to add Education, Projects, and a Professional Summary.",
      estimated_delta: Math.round((60 - (barScores.completeness ?? 60)) * 0.10),
      action: "add_content",
    });
  }

  if ((barScores.ats_safety ?? 100) < 60) {
    recs.push({
      id: "ats",
      priority: 4,
      title: "Fix ATS formatting issues",
      detail: "Your resume has structural issues that prevent ATS systems from reading it. Export as a clean single-column PDF — no tables or images.",
      estimated_delta: Math.round((60 - (barScores.ats_safety ?? 60)) * 0.20),
      action: "fix_format",
    });
  }

  if ((barScores.hygiene ?? 100) < 55) {
    recs.push({
      id: "hygiene",
      priority: 5,
      title: "Add missing contact info and remove filler phrases",
      detail: "Add your LinkedIn, GitHub, and phone number. Remove generic phrases like 'team player' or 'quick learner' — they dilute your signal.",
      estimated_delta: Math.round((55 - (barScores.hygiene ?? 55)) * 0.05),
      action: "add_content",
    });
  }

  return recs.sort((a, b) => b.estimated_delta - a.estimated_delta).slice(0, 4);
}

// ── Step components ───────────────────────────────────────────────────────────

const QC_ICON: Record<string, string> = {
  ats_broken: "⛔", structurally_weak: "⚠️", keyword_weak: "🔍",
  impact_weak: "📉", role_misaligned: "🎯", high_potential_underwritten: "💎",
  interview_ready: "✅",
};
const QC_COLOR: Record<string, string> = {
  ats_broken: "#dc2626", structurally_weak: "#d97706", keyword_weak: "#b45309",
  impact_weak: "#0284c7", role_misaligned: "#7c3aed", high_potential_underwritten: "#9333ea",
  interview_ready: "#16a34a",
};

function StepDiagnose({ qc, barScores, overallScore, recs }: {
  qc: QualityClassInfo;
  barScores: Record<string, number>;
  overallScore: number;
  recs: Recommendation[];
}) {
  const color = QC_COLOR[qc.key] ?? "#0071c5";
  const topGaps = Object.entries(barScores)
    .filter(([k]) => ["evidence", "jd_match", "completeness", "ats_safety"].includes(k))
    .sort(([, a], [, b]) => a - b)
    .slice(0, 3);

  return (
    <div>
      <div style={{ background: `${color}10`, border: `1.5px solid ${color}33`, borderRadius: 12, padding: "18px 20px", marginBottom: 20 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 8 }}>
          <span style={{ fontSize: "1.5rem" }}>{QC_ICON[qc.key]}</span>
          <span style={{ fontWeight: 800, fontSize: "1rem", color }}>{qc.label}</span>
          <span style={{ marginLeft: "auto", fontFamily: "var(--font-mono)", fontSize: "0.8rem", color: "#5c6570" }}>
            Score: {overallScore}/100
          </span>
        </div>
        <p style={{ fontSize: "0.88rem", color: "#1a1c20", lineHeight: 1.65, margin: 0 }}>{qc.guidance}</p>
      </div>

      <p style={{ fontSize: "0.85rem", fontWeight: 700, color: "#414752", marginBottom: 10 }}>Top 3 score gaps</p>
      <div style={{ display: "flex", flexDirection: "column", gap: 8, marginBottom: 20 }}>
        {topGaps.map(([key, val]) => {
          const label: Record<string, string> = {
            evidence: "Evidence Quality", jd_match: "JD Match",
            completeness: "Profile Completeness", ats_safety: "ATS Safety",
          };
          const gapColor = val < 40 ? "#dc2626" : val < 60 ? "#d97706" : "#16a34a";
          return (
            <div key={key} style={{ display: "grid", gridTemplateColumns: "180px 1fr 42px", gap: 10, alignItems: "center" }}>
              <span style={{ fontSize: "0.82rem", color: "#1a1c20" }}>{label[key]}</span>
              <div style={{ height: 7, background: "#e8ecf2", borderRadius: 9999, overflow: "hidden" }}>
                <div style={{ height: "100%", width: `${val}%`, background: gapColor, borderRadius: 9999 }} />
              </div>
              <span style={{ fontSize: "0.78rem", fontWeight: 700, color: gapColor }}>{Math.round(val)}</span>
            </div>
          );
        })}
      </div>

      <p style={{ fontSize: "0.85rem", fontWeight: 700, color: "#414752", marginBottom: 8 }}>
        Biggest opportunities ({recs.length} fixes identified)
      </p>
      {recs.map((r) => (
        <div key={r.id} style={{ display: "flex", alignItems: "center", gap: 10, padding: "8px 12px", borderRadius: 8, background: "#f4f6f9", marginBottom: 6 }}>
          <span style={{ fontSize: "0.82rem", flex: 1, color: "#1a1c20" }}>{r.title}</span>
          <span style={{ fontSize: "0.72rem", fontWeight: 700, color: "#16a34a", whiteSpace: "nowrap" }}>
            +{r.estimated_delta} pts
          </span>
        </div>
      ))}
    </div>
  );
}

type RetrievedPattern = {
  text: string;
  similarity: number;
  overall_score: number;
  evidence_score: number;
  role_family: string;
};

function StepCompare({
  pattern,
  barScores,
  retrievedPatterns,
  patternsLoading,
}: {
  pattern: RolePattern;
  barScores: Record<string, number>;
  retrievedPatterns: RetrievedPattern[];
  patternsLoading: boolean;
}) {
  const hasReal = retrievedPatterns.length > 0;
  // Compute "typical" from retrieved patterns when available, else use static
  const typicalEvidence = hasReal
    ? Math.round(retrievedPatterns.reduce((s, p) => s + p.evidence_score, 0) / retrievedPatterns.length)
    : pattern.typical_scores.evidence;
  const typicalScore = hasReal
    ? Math.round(retrievedPatterns.reduce((s, p) => s + p.overall_score, 0) / retrievedPatterns.length)
    : 74;

  const gaps = [
    { label: "Evidence Quality", yours: barScores.evidence ?? 0, typical: typicalEvidence },
    { label: "JD Match", yours: barScores.jd_match ?? 0, typical: pattern.typical_scores.jd_match },
    { label: "Profile Completeness", yours: barScores.completeness ?? 0, typical: pattern.typical_scores.completeness },
  ];

  return (
    <div>
      {/* Source badge */}
      <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 14 }}>
        <span style={{
          fontSize: "0.72rem", fontWeight: 700, padding: "2px 10px", borderRadius: 9999,
          background: hasReal ? "#f0fdf4" : "#f4f6f9",
          border: `1px solid ${hasReal ? "#86efac" : "#e8ecf2"}`,
          color: hasReal ? "#15803d" : "#8a95a2",
        }}>
          {patternsLoading ? "Loading knowledge base…" : hasReal
            ? `✓ ${retrievedPatterns.length} real Interview Ready ${pattern.role} resume${retrievedPatterns.length > 1 ? "s" : ""} retrieved`
            : "Using reference patterns (knowledge base not yet populated)"}
        </span>
      </div>

      <p style={{ fontSize: "0.87rem", color: "#414752", lineHeight: 1.65, marginBottom: 18 }}>
        {hasReal
          ? <>Here is how <strong>{retrievedPatterns.length} Interview Ready {pattern.role} resume{retrievedPatterns.length > 1 ? "s" : ""}</strong> in the CARE-RAG knowledge base compare to yours. These are real resumes from students who reached the Interview Ready threshold.</>
          : <>Here is how <strong>Interview Ready {pattern.role} resumes</strong> typically look. These are reference patterns — the knowledge base will show real examples as more students reach Interview Ready status.</>
        }
      </p>

      {/* Gap bars */}
      <div style={{ display: "flex", flexDirection: "column", gap: 14, marginBottom: 24 }}>
        {gaps.map((g) => (
          <div key={g.label}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 5 }}>
              <span style={{ fontSize: "0.82rem", fontWeight: 600, color: "#1a1c20" }}>{g.label}</span>
              <span style={{ fontSize: "0.75rem", color: "#5c6570" }}>
                You: <strong>{Math.round(g.yours)}</strong> · {hasReal ? "KB avg" : "Typical"}: <strong>{g.typical}</strong>
              </span>
            </div>
            <div style={{ height: 8, background: "#e8ecf2", borderRadius: 9999, overflow: "hidden", position: "relative" }}>
              <div style={{ height: "100%", width: `${g.typical}%`, background: "#e2e8f0", borderRadius: 9999 }} />
              <div style={{ position: "absolute", top: 0, left: 0, height: "100%", width: `${g.yours}%`, background: g.yours >= g.typical ? "#16a34a" : "#0071c5", borderRadius: 9999 }} />
            </div>
          </div>
        ))}
      </div>

      {/* Real retrieved excerpts */}
      {hasReal ? (
        <div style={{ display: "flex", flexDirection: "column", gap: 10, marginBottom: 16 }}>
          <p style={{ fontSize: "0.8rem", fontWeight: 700, color: "#414752", marginBottom: 4 }}>
            Excerpts from retrieved Interview Ready resumes (avg score: {typicalScore}/100):
          </p>
          {retrievedPatterns.slice(0, 3).map((p, i) => (
            <div key={i} style={{ background: "#f0fdf4", border: "1px solid #86efac", borderRadius: 10, padding: "12px 14px" }}>
              <div style={{ display: "flex", gap: 8, alignItems: "center", marginBottom: 6 }}>
                <span style={{ fontSize: "0.7rem", fontWeight: 700, color: "#15803d", background: "#dcfce7", borderRadius: 9999, padding: "1px 8px" }}>
                  {Math.round(p.similarity)}% similar · score {Math.round(p.overall_score)}
                </span>
              </div>
              <p style={{ fontSize: "0.82rem", color: "#1a1c20", lineHeight: 1.6, margin: 0, fontStyle: "italic" }}>
                "{p.text.slice(0, 220)}{p.text.length > 220 ? "…" : ""}"
              </p>
            </div>
          ))}
        </div>
      ) : (
        /* Static fallback */
        <div style={{ background: "#f4f6f9", borderRadius: 10, padding: "14px 16px", marginBottom: 16 }}>
          <p style={{ fontSize: "0.8rem", fontWeight: 700, color: "#414752", marginBottom: 6 }}>
            Example bullet from a strong {pattern.role} resume:
          </p>
          <p style={{ fontSize: "0.84rem", color: "#1a1c20", lineHeight: 1.6, fontStyle: "italic", margin: 0 }}>
            "{pattern.bullet_example}"
          </p>
        </div>
      )}

      {/* Keywords */}
      <div>
        <p style={{ fontSize: "0.8rem", fontWeight: 700, color: "#414752", marginBottom: 8 }}>
          Keywords strong {pattern.role} resumes typically include:
        </p>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
          {pattern.keywords.map((kw) => (
            <span key={kw} style={{ padding: "3px 10px", borderRadius: 9999, fontSize: "0.78rem", background: "#e0f0ff", border: "1px solid #7dd3fc", color: "#0284c7" }}>
              {kw}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}

function StepRecommend({ recs, onSelectAction }: {
  recs: Recommendation[];
  onSelectAction: (action: string) => void;
}) {
  const total_delta = recs.reduce((s, r) => s + r.estimated_delta, 0);
  return (
    <div>
      <div style={{ background: "#f0fdf4", border: "1px solid #86efac", borderRadius: 10, padding: "12px 16px", marginBottom: 20, display: "flex", gap: 12, alignItems: "center" }}>
        <span style={{ fontSize: "1.3rem" }}>🎯</span>
        <p style={{ fontSize: "0.87rem", color: "#15803d", margin: 0 }}>
          Implementing all {recs.length} fixes could add approximately <strong>+{total_delta} points</strong> to your overall score.
        </p>
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
        {recs.map((r, i) => (
          <div key={r.id} style={{ border: "1px solid rgba(192,199,211,0.4)", borderRadius: 10, padding: "14px 16px", background: "#fafbfc" }}>
            <div style={{ display: "flex", alignItems: "flex-start", gap: 12 }}>
              <span style={{ fontFamily: "var(--font-mono)", fontWeight: 800, fontSize: "0.78rem", color: "#0071c5", background: "#e0f0ff", borderRadius: "50%", width: 22, height: 22, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0, marginTop: 2 }}>
                {i + 1}
              </span>
              <div style={{ flex: 1 }}>
                <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 6 }}>
                  <span style={{ fontSize: "0.88rem", fontWeight: 700, color: "#1a1c20" }}>{r.title}</span>
                  <span style={{ fontSize: "0.72rem", fontWeight: 800, color: "#16a34a", background: "#f0fdf4", border: "1px solid #86efac", borderRadius: 9999, padding: "1px 8px" }}>
                    +{r.estimated_delta} pts
                  </span>
                </div>
                <p style={{ fontSize: "0.82rem", color: "#414752", lineHeight: 1.6, margin: 0 }}>{r.detail}</p>
              </div>
            </div>
            {r.action === "rewrite" && (
              <button
                type="button"
                className="btn-primary"
                style={{ marginTop: 10, fontSize: "0.8rem", padding: "6px 14px" }}
                onClick={() => onSelectAction("rewrite")}
              >
                Apply proof-linked rewrite →
              </button>
            )}
            {r.action === "add_content" && (
              <Link href="/settings" className="btn-secondary" style={{ marginTop: 10, fontSize: "0.8rem", padding: "6px 14px", display: "inline-block", textDecoration: "none" }}>
                Go to Profile →
              </Link>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

function StepRewrite({ ws }: { ws: ReturnType<typeof usePlacementWorkspace> }) {
  return (
    <div>
      <p style={{ fontSize: "0.87rem", color: "#414752", lineHeight: 1.65, marginBottom: 16 }}>
        The proof-linked rewriter will strengthen your experience bullets using STAR structure.
        It only rewrites what exists — it never fabricates. Unsupported claims are flagged, not changed.
      </p>
      {!ws.rewriteBundle && !ws.rewriting ? (
        <button
          type="button"
          className="btn-primary btn-block"
          disabled={!ws.canRewrite}
          onClick={() => void ws.runProofRewrite()}
        >
          {ws.canRewrite ? "Run Proof-Linked Rewrite" : "Run a JD scan first to unlock rewrites"}
        </button>
      ) : (
        <RewriteDiffPanel
          bundle={ws.rewriteBundle ? {
            top_issues: ws.rewriteBundle.top_issues,
            section_rewrites: ws.rewriteBundle.section_rewrites,
            unsupported_claims: ws.rewriteBundle.unsupported_claims,
            requires_confirmation: ws.rewriteBundle.requires_confirmation,
          } : null}
          loading={ws.rewriting}
          error={ws.rewriteError}
          canRun={ws.canRewrite}
          source="manual"
          onRunRewrite={() => void ws.runProofRewrite()}
        />
      )}
    </div>
  );
}

function StepVerify({ ws, prevScore }: {
  ws: ReturnType<typeof usePlacementWorkspace>;
  prevScore: number;
}) {
  const currentScore = ws.overallScore ?? 0;
  const delta = currentScore - prevScore;

  return (
    <div>
      <p style={{ fontSize: "0.87rem", color: "#414752", lineHeight: 1.65, marginBottom: 16 }}>
        Re-scan your resume against the same JD to see how your changes improved your score.
      </p>

      {delta !== 0 && (
        <div style={{
          background: delta > 0 ? "#f0fdf4" : "#fef2f2",
          border: `1px solid ${delta > 0 ? "#86efac" : "#fca5a5"}`,
          borderRadius: 10, padding: "14px 16px", marginBottom: 20,
          display: "flex", gap: 12, alignItems: "center",
        }}>
          <span style={{ fontSize: "1.4rem" }}>{delta > 0 ? "📈" : "📊"}</span>
          <p style={{ fontSize: "0.9rem", fontWeight: 600, color: delta > 0 ? "#15803d" : "#dc2626", margin: 0 }}>
            {delta > 0
              ? `Score improved from ${prevScore} → ${currentScore} (+${delta} points)`
              : `Score: ${prevScore} → ${currentScore} (${delta} points). Try applying more fixes.`}
          </p>
        </div>
      )}

      {ws.hasScore && ws.barScores && ws.overallScore !== null ? (
        <ScoreBreakdown
          barScores={ws.barScores}
          overallScore={ws.overallScore}
          scoreBucket={ws.scoreBucket}
          semanticMethod={ws.semanticMethod}
        />
      ) : (
        <div>
          <p style={{ fontSize: "0.85rem", color: "#5c6570", marginBottom: 12 }}>
            Re-run the JD scan to see your updated score.
          </p>
          <Link href="/match" className="btn-primary" style={{ textDecoration: "none", display: "inline-block" }}>
            Go to JD Match →
          </Link>
        </div>
      )}
    </div>
  );
}

// ── Wizard page ───────────────────────────────────────────────────────────────

const STEPS = [
  { id: 1, label: "Diagnose", icon: "🔬" },
  { id: 2, label: "Compare", icon: "📊" },
  { id: 3, label: "Recommend", icon: "💡" },
  { id: 4, label: "Rewrite", icon: "✍️" },
  { id: 5, label: "Verify", icon: "✅" },
] as const;

export default function ResumeWizardPage() {
  const ws = usePlacementWorkspace("readiness");
  const token = getStoredAuth()?.token ?? "";
  const [step, setStep] = useState(1);
  const [prevScore] = useState(ws.overallScore ?? 0);
  const [retrievedPatterns, setRetrievedPatterns] = useState<RetrievedPattern[]>([]);
  const [patternsLoading, setPatternsLoading] = useState(false);

  const hasScoreData = ws.hasScore && ws.barScores && ws.overallScore !== null;

  const pattern = detectRole(
    ws.parseResult ? "" : "",
    ws.matchedSkills,
  );

  // Fetch real patterns from CARE-RAG knowledge base when wizard loads
  useEffect(() => {
    if (!token || !hasScoreData) return;
    setPatternsLoading(true);
    void api.similarResumes(token, pattern.role.split(" ")[0].toLowerCase(), 5)
      .then((res) => setRetrievedPatterns(res.patterns ?? []))
      .catch(() => setRetrievedPatterns([]))
      .finally(() => setPatternsLoading(false));
  }, [token, hasScoreData, pattern.role]);

  const recs = hasScoreData && ws.qualityClass
    ? buildRecommendations(ws.barScores!, ws.qualityClass, ws.missingSkills)
    : [];

  const handleSelectAction = useCallback((action: string) => {
    if (action === "rewrite") setStep(4);
  }, []);

  if (!hasScoreData || !ws.qualityClass) {
    return (
      <div className="page-canvas">
        <div className="page-title-row">
          <div>
            <h1 className="page-title">Resume Wizard</h1>
            <p className="page-subtitle">Guided 5-step improvement flow.</p>
          </div>
        </div>
        <div className="content-card">
          <div className="content-card-body scan-empty-state">
            <p style={{ fontSize: "0.95rem", color: "#414752", marginBottom: 16 }}>
              Run a JD Match scan first to unlock the wizard. The wizard uses your scorecard to diagnose issues and guide you through fixing them.
            </p>
            <div style={{ display: "flex", gap: 10, flexWrap: "wrap", justifyContent: "center" }}>
              <Link href="/resume" className="btn-secondary" style={{ textDecoration: "none" }}>
                Upload Resume
              </Link>
              <Link href="/match" className="btn-primary" style={{ textDecoration: "none" }}>
                Run JD Match →
              </Link>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="page-canvas">
      <div className="page-title-row">
        <div>
          <h1 className="page-title">Resume Wizard</h1>
          <p className="page-subtitle">
            {ws.qualityClass.label} · Score {ws.overallScore}/100 · {recs.length} fix{recs.length !== 1 ? "es" : ""} identified
          </p>
        </div>
        <Link href="/match" className="btn-secondary" style={{ alignSelf: "center", textDecoration: "none", fontSize: "0.82rem" }}>
          ← Back to JD Match
        </Link>
      </div>

      {/* Step progress bar */}
      <div style={{ display: "flex", gap: 0, marginBottom: 28, overflowX: "auto" }}>
        {STEPS.map((s, i) => {
          const done = step > s.id;
          const active = step === s.id;
          return (
            <button
              key={s.id}
              type="button"
              onClick={() => setStep(s.id)}
              style={{
                flex: 1, display: "flex", flexDirection: "column", alignItems: "center",
                padding: "10px 4px", border: "none", cursor: "pointer",
                background: active ? "#e0f0ff" : done ? "#f0fdf4" : "#f4f6f9",
                borderBottom: `3px solid ${active ? "#0071c5" : done ? "#16a34a" : "#e8ecf2"}`,
                transition: "background 0.15s",
                minWidth: 80,
              }}
            >
              <span style={{ fontSize: "1.1rem", marginBottom: 3 }}>{done ? "✓" : s.icon}</span>
              <span style={{ fontSize: "0.72rem", fontWeight: active ? 700 : 500, color: active ? "#0071c5" : done ? "#15803d" : "#717783" }}>
                {s.label}
              </span>
            </button>
          );
        })}
      </div>

      {/* Step content */}
      <div className="content-card">
        <div className="content-card-header">
          <h2 className="content-card-title">
            {STEPS[step - 1].icon} Step {step}: {STEPS[step - 1].label}
          </h2>
          <span className="chip chip-mono">{step}/5</span>
        </div>
        <div className="content-card-body">
          {step === 1 && (
            <StepDiagnose
              qc={ws.qualityClass}
              barScores={ws.barScores!}
              overallScore={ws.overallScore!}
              recs={recs}
            />
          )}
          {step === 2 && (
            <StepCompare
              pattern={pattern}
              barScores={ws.barScores!}
              retrievedPatterns={retrievedPatterns}
              patternsLoading={patternsLoading}
            />
          )}
          {step === 3 && <StepRecommend recs={recs} onSelectAction={handleSelectAction} />}
          {step === 4 && <StepRewrite ws={ws} />}
          {step === 5 && <StepVerify ws={ws} prevScore={prevScore} />}
        </div>
      </div>

      {/* Navigation */}
      <div style={{ display: "flex", gap: 12, justifyContent: "space-between", marginTop: 16 }}>
        <button
          type="button"
          className="btn-secondary"
          disabled={step === 1}
          onClick={() => setStep((s) => Math.max(1, s - 1))}
        >
          ← Previous
        </button>
        <span style={{ fontSize: "0.8rem", color: "#717783", alignSelf: "center" }}>
          {step === 5 ? "Wizard complete" : `${5 - step} step${5 - step !== 1 ? "s" : ""} remaining`}
        </span>
        {step < 5 ? (
          <button
            type="button"
            className="btn-primary"
            onClick={() => setStep((s) => Math.min(5, s + 1))}
          >
            Next →
          </button>
        ) : (
          <Link href="/resume" className="btn-primary" style={{ textDecoration: "none" }}>
            Export Resume →
          </Link>
        )}
      </div>
    </div>
  );
}
