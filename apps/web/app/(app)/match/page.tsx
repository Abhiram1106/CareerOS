"use client";

import type { GraphGapItem, QualityClassInfo } from "../../../lib/api";
import { AtsBreakdown } from "../../../components/workspace/AtsBreakdown";
import { ScoreBreakdown } from "../../../components/workspace/ScoreBreakdown";
import { ScoreBarsInline, SkillLists } from "../../../components/workspace/ScoreBarsInline";
import { usePlacementWorkspace } from "../../../hooks/usePlacementWorkspace";

// CARE-RAG Layer 2 colour palette per quality class
const QC_STYLES: Record<string, { bg: string; border: string; badge: string; icon: string }> = {
  ats_broken:                  { bg: "#fef2f2", border: "#fca5a5", badge: "#dc2626", icon: "⛔" },
  structurally_weak:           { bg: "#fff7ed", border: "#fcd34d", badge: "#d97706", icon: "⚠️" },
  keyword_weak:                { bg: "#fffbeb", border: "#fde68a", badge: "#b45309", icon: "🔍" },
  impact_weak:                 { bg: "#f0f9ff", border: "#7dd3fc", badge: "#0284c7", icon: "📉" },
  role_misaligned:             { bg: "#f5f3ff", border: "#c4b5fd", badge: "#7c3aed", icon: "🎯" },
  high_potential_underwritten: { bg: "#fdf4ff", border: "#e9d5ff", badge: "#9333ea", icon: "💎" },
  interview_ready:             { bg: "#f0fdf4", border: "#86efac", badge: "#16a34a", icon: "✅" },
};

function QualityClassBanner({ qc }: { qc: QualityClassInfo }) {
  const s = QC_STYLES[qc.key] ?? QC_STYLES.impact_weak;
  return (
    <div style={{
      background: s.bg, border: `1.5px solid ${s.border}`, borderRadius: 12,
      padding: "16px 20px", display: "flex", gap: 14, alignItems: "flex-start",
    }}>
      <span style={{ fontSize: "1.4rem", lineHeight: 1, flexShrink: 0 }}>{s.icon}</span>
      <div style={{ flex: 1 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 6 }}>
          <span style={{
            fontSize: "0.72rem", fontWeight: 800, letterSpacing: "0.06em",
            textTransform: "uppercase", color: "#fff",
            background: s.badge, borderRadius: 9999, padding: "2px 10px",
          }}>
            {qc.label}
          </span>
          <span style={{ fontSize: "0.75rem", color: "#717783", fontFamily: "var(--font-mono)" }}>
            CARE-RAG diagnosis
          </span>
        </div>
        <p style={{ fontSize: "0.87rem", color: "#1a1c20", lineHeight: 1.6, margin: 0 }}>
          {qc.guidance}
        </p>
      </div>
    </div>
  );
}

export default function MatchPage() {
  const ws = usePlacementWorkspace("scan");

  return (
    <div className="page-canvas">
      <div className="page-title-row">
        <div>
          <h1 className="page-title">JD Match</h1>
          <p className="page-subtitle">Score your resume against target jobs and inspect weighted readiness output.</p>
        </div>
      </div>

      <div className="readiness-stack">
        <div className="content-card">
          <div className="content-card-header">
            <h2 className="content-card-title">Scan Against Job Description</h2>
          </div>
          <div className="content-card-body">
            <div className="scan-grid">
              <div>
                <p className="scan-intro">Paste a JD with role requirements to compute your placement readiness score.</p>
                {!ws.parseResult && (
                  <div className="scan-hint-banner">Upload your resume first on the Resume page.</div>
                )}
                <textarea
                  className="jd-textarea"
                  value={ws.jdText}
                  onChange={(e) => ws.setJdText(e.target.value)}
                  placeholder="Paste JD here..."
                  rows={10}
                />
                <div className="scan-meta-row">
                  <span className="scan-meta-small">{ws.jdText.trim().length} characters</span>
                  <span className="scan-meta-small">Minimum recommended: 120</span>
                </div>
                <button
                  type="button"
                  className="btn-primary"
                  disabled={!ws.canScan || ws.scanning}
                  onClick={() => void ws.runPlacementScore()}
                >
                  {ws.scanning ? "Scoring..." : "Run Placement Score"}
                </button>
                {ws.scanError ? (
                  <p className="workspace-error" role="alert">
                    {ws.scanError}
                  </p>
                ) : null}
              </div>

              <div>
                <p className="section-list-heading">Quick diagnostics</p>
                {ws.hasScore && ws.barScores && ws.overallScore !== null ? (
                  <>
                    <ScoreBarsInline
                      barScores={ws.barScores}
                      overallScore={ws.overallScore}
                      scoreBucket={ws.scoreBucket}
                    />
                    <SkillLists matched={ws.matchedSkills} missing={ws.missingSkills} />
                  </>
                ) : (
                  <p className="scan-empty">Your score summary appears here after scanning.</p>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* ── CARE-RAG: Quality class diagnostic banner ──────────── */}
        {ws.qualityClass ? (
          <QualityClassBanner qc={ws.qualityClass} />
        ) : null}

        <div className="content-card">
          <div className="content-card-header">
            <h2 className="content-card-title">Readiness Breakdown</h2>
          </div>
          <div className="content-card-body">
            {ws.hasScore && ws.barScores && ws.overallScore !== null ? (
              <ScoreBreakdown
                barScores={ws.barScores}
                overallScore={ws.overallScore}
                scoreBucket={ws.scoreBucket}
                semanticMethod={ws.semanticMethod}
              />
            ) : (
              <div className="scan-empty-state">
                <p>Run a JD scan to unlock your full readiness breakdown.</p>
              </div>
            )}
          </div>
        </div>

        {ws.hasScore ? (
          <AtsBreakdown
            score={ws.barScores?.ats_safety ?? 0}
            bucket={ws.atsBucket}
            checks={ws.atsChecks}
            issues={ws.atsIssues}
          />
        ) : null}

        {/* ── Vendor simulation ──────────────────────────────────── */}
        {ws.vendorSimulation ? (
          <div className="content-card">
            <div className="content-card-header">
              <h2 className="content-card-title">ATS Vendor Simulation</h2>
              <span className="chip chip-primary">
                Composite {ws.vendorSimulation.composite_score}/100
              </span>
            </div>
            <div className="content-card-body">
              <p style={{ fontSize: "0.82rem", color: "#5c6570", marginBottom: 14 }}>
                How your resume scores across 7 ATS systems weighted by Indian market prevalence.
              </p>
              <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                {ws.vendorSimulation.vendors.map((v) => {
                  const pct = Math.round(v.score);
                  const color = pct >= 70 ? "#16a34a" : pct >= 50 ? "#d97706" : "#dc2626";
                  return (
                    <div key={v.id} style={{ display: "grid", gridTemplateColumns: "160px 1fr 48px", gap: 10, alignItems: "center" }}>
                      <span style={{ fontSize: "0.82rem", fontWeight: 500, color: "#1a1c20" }}>{v.name}</span>
                      <div style={{ height: 8, background: "#e8ecf2", borderRadius: 9999, overflow: "hidden" }}>
                        <div style={{ height: "100%", width: `${pct}%`, background: color, borderRadius: 9999, transition: "width 0.4s" }} />
                      </div>
                      <span style={{ fontSize: "0.8rem", fontWeight: 700, color, textAlign: "right" }}>{pct}</span>
                    </div>
                  );
                })}
              </div>
              <p style={{ fontSize: "0.75rem", color: "#8a95a2", marginTop: 12 }}>
                Weights: Taleo 18% · Workday 16% · Naukri RMS 15% · Greenhouse 12% · PeopleStrong 10% · Darwinbox 9% · Lever 8%
              </p>
            </div>
          </div>
        ) : null}

        {/* ── M7: JD Intelligence Heatmap ───────────────────────── */}
        {ws.keywordGap && ws.keywordGap.total_jd_keywords > 0 ? (
          <div className="content-card">
            <div className="content-card-header">
              <h2 className="content-card-title">JD Intelligence Heatmap</h2>
              <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
                <span className="chip chip-mono">{ws.keywordGap.match_rate}% covered</span>
                <span className="chip" style={{ background: "#f4f6f9", color: "#5c6570" }}>
                  {ws.keywordGap.total_jd_keywords} JD keywords
                </span>
              </div>
            </div>
            <div className="content-card-body">
              {/* Match rate bar */}
              <div style={{ marginBottom: 18 }}>
                <div style={{ height: 6, background: "#e8ecf2", borderRadius: 9999, overflow: "hidden" }}>
                  <div style={{
                    height: "100%",
                    width: `${ws.keywordGap.match_rate}%`,
                    background: ws.keywordGap.match_rate >= 70 ? "#16a34a" : ws.keywordGap.match_rate >= 40 ? "#d97706" : "#dc2626",
                    borderRadius: 9999, transition: "width 0.5s",
                  }} />
                </div>
                <div style={{ display: "flex", justifyContent: "space-between", marginTop: 4 }}>
                  <span style={{ fontSize: "0.72rem", color: "#dc2626" }}>0%</span>
                  <span style={{ fontSize: "0.72rem", color: "#d97706" }}>50%</span>
                  <span style={{ fontSize: "0.72rem", color: "#16a34a" }}>100%</span>
                </div>
              </div>

              {/* Missing keywords — colour by importance + size by frequency + graph distance */}
              {ws.keywordGap.missing.length > 0 && (
                <div style={{ marginBottom: 20 }}>
                  <p style={{ fontSize: "0.82rem", fontWeight: 700, color: "#93000a", marginBottom: 10 }}>
                    ❌ Missing from your resume ({ws.keywordGap.missing.length})
                  </p>
                  <div style={{ display: "flex", flexWrap: "wrap", gap: 7 }}>
                    {ws.keywordGap.missing.map((kw) => {
                      const freq = kw.frequency ?? 1;
                      const size = freq >= 4 ? "0.88rem" : freq >= 2 ? "0.8rem" : "0.74rem";
                      const bg = kw.importance === "high" ? "#fef2f2" : kw.importance === "medium" ? "#fff7ed" : "#f9fafb";
                      const border = kw.importance === "high" ? "#fca5a5" : kw.importance === "medium" ? "#fcd34d" : "#e5e7eb";
                      const color = kw.importance === "high" ? "#dc2626" : kw.importance === "medium" ? "#d97706" : "#6b7280";
                      // Graph enrichment: find this keyword in graphGap
                      const graphInfo = ws.graphGap?.find((g: GraphGapItem) => g.skill.toLowerCase() === kw.keyword.toLowerCase());
                      const tooltipParts = [`Appears ${freq}× in JD · ${kw.importance} priority`];
                      if (graphInfo?.reachable && graphInfo.nearest_known) {
                        tooltipParts.push(`${graphInfo.distance} hop${graphInfo.distance !== 1 ? "s" : ""} from your ${graphInfo.nearest_known}`);
                      }
                      return (
                        <span key={kw.keyword} title={tooltipParts.join(" · ")}
                          style={{ padding: "4px 10px", borderRadius: 9999, fontSize: size, fontWeight: 600, background: bg, border: `1.5px solid ${border}`, color, cursor: "default", display: "inline-flex", alignItems: "center", gap: 4 }}>
                          {kw.keyword}
                          {freq > 1 && (
                            <span style={{ fontSize: "0.66rem", opacity: 0.75, fontWeight: 800 }}>×{freq}</span>
                          )}
                          {graphInfo?.reachable && (
                            <span style={{ fontSize: "0.62rem", background: "rgba(0,113,197,0.12)", color: "#0071c5", borderRadius: 4, padding: "0 4px", fontWeight: 700 }}>
                              d{graphInfo.distance}
                            </span>
                          )}
                        </span>
                      );
                    })}
                  </div>
                  <p style={{ fontSize: "0.72rem", color: "#8a95a2", marginTop: 8 }}>
                    Chip size = JD frequency. Colour = priority. <strong style={{ color: "#0071c5" }}>d1/d2</strong> = reachable from skills you already have.
                  </p>
                </div>
              )}

              {/* Present keywords */}
              {ws.keywordGap.matched.length > 0 && (
                <div>
                  <p style={{ fontSize: "0.82rem", fontWeight: 700, color: "#15803d", marginBottom: 10 }}>
                    ✓ Found in your resume ({ws.keywordGap.matched.length})
                  </p>
                  <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
                    {ws.keywordGap.matched.slice(0, 25).map((kw) => {
                      const freq = kw.frequency ?? 1;
                      return (
                        <span key={kw.keyword} title={`Appears ${freq}× in JD`}
                          style={{ padding: "3px 10px", borderRadius: 9999, fontSize: "0.76rem", fontWeight: 500, background: "#f0fdf4", border: "1px solid #86efac", color: "#15803d" }}>
                          {kw.keyword}
                          {freq > 1 && (
                            <span style={{ marginLeft: 4, fontSize: "0.64rem", opacity: 0.7, fontWeight: 700 }}>×{freq}</span>
                          )}
                        </span>
                      );
                    })}
                  </div>
                </div>
              )}
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
}
