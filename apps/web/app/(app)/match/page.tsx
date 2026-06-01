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
      </div>
    </div>
  );
}
