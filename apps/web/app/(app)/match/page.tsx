"use client";

import { AtsBreakdown } from "../../../components/workspace/AtsBreakdown";
import { ScoreBreakdown } from "../../../components/workspace/ScoreBreakdown";
import { ScoreBarsInline, SkillLists } from "../../../components/workspace/ScoreBarsInline";
import { usePlacementWorkspace } from "../../../hooks/usePlacementWorkspace";

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

        {/* ── Keyword gap ────────────────────────────────────────── */}
        {ws.keywordGap && ws.keywordGap.total_jd_keywords > 0 ? (
          <div className="content-card">
            <div className="content-card-header">
              <h2 className="content-card-title">Keyword Gap Analysis</h2>
              <span className="chip chip-mono">
                {ws.keywordGap.match_rate}% match · {ws.keywordGap.total_jd_keywords} JD keywords
              </span>
            </div>
            <div className="content-card-body">
              {ws.keywordGap.missing.length > 0 && (
                <div style={{ marginBottom: 18 }}>
                  <p style={{ fontSize: "0.85rem", fontWeight: 700, color: "#93000a", marginBottom: 8 }}>
                    Missing from your resume ({ws.keywordGap.missing.length})
                  </p>
                  <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
                    {ws.keywordGap.missing.map((kw) => (
                      <span
                        key={kw.keyword}
                        style={{
                          padding: "3px 10px",
                          borderRadius: 9999,
                          fontSize: "0.78rem",
                          fontWeight: 600,
                          background: kw.importance === "high" ? "#fef2f2" : kw.importance === "medium" ? "#fff7ed" : "#f9fafb",
                          border: `1px solid ${kw.importance === "high" ? "#fca5a5" : kw.importance === "medium" ? "#fcd34d" : "#e5e7eb"}`,
                          color: kw.importance === "high" ? "#dc2626" : kw.importance === "medium" ? "#d97706" : "#6b7280",
                        }}
                      >
                        {kw.keyword}
                        <span style={{ marginLeft: 4, fontSize: "0.68rem", opacity: 0.7 }}>{kw.importance}</span>
                      </span>
                    ))}
                  </div>
                </div>
              )}
              {ws.keywordGap.matched.length > 0 && (
                <div>
                  <p style={{ fontSize: "0.85rem", fontWeight: 700, color: "#15803d", marginBottom: 8 }}>
                    Found in your resume ({ws.keywordGap.matched.length})
                  </p>
                  <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
                    {ws.keywordGap.matched.slice(0, 20).map((kw) => (
                      <span
                        key={kw.keyword}
                        style={{
                          padding: "3px 10px", borderRadius: 9999, fontSize: "0.78rem",
                          fontWeight: 500, background: "#f0fdf4",
                          border: "1px solid #86efac", color: "#15803d",
                        }}
                      >
                        {kw.keyword}
                      </span>
                    ))}
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
