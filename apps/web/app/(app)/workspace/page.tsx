"use client";

import { useSearchParams } from "next/navigation";
import { Suspense, useMemo, useState } from "react";

import { AgentProgress } from "../../../components/workspace/AgentProgress";
import { AssistantPanel } from "../../../components/workspace/AssistantPanel";
import { BuilderWizard } from "../../../components/workspace/BuilderWizard";
import { JobCard } from "../../../components/workspace/JobCard";
import { RewriteDiffPanel } from "../../../components/workspace/RewriteDiffPanel";
import { ScoreBreakdown } from "../../../components/workspace/ScoreBreakdown";
import { ResumeDropzone } from "../../../components/workspace/ResumeDropzone";
import {
  parseWorkspaceTab,
  usePlacementWorkspace,
  type WorkspaceTab,
} from "../../../hooks/usePlacementWorkspace";
import { SCORE_COMPONENTS, TEMPLATE_OPTIONS, readinessBucket } from "../../../lib/placement";

const TABS: ReadonlyArray<[WorkspaceTab, string]> = [
  ["resume", "Document Intelligence"],
  ["scan", "JD Match Scan"],
  ["readiness", "Readiness Snapshot"],
  ["rewrite", "Proof-Linked Rewrite"],
  ["jobs", "Jobs Feed"],
  ["builder", "Builder Wizard"],
  ["assistant", "Student Assistant"],
];

function ScoreBarsInline({
  barScores,
  overallScore,
  scoreBucket,
}: {
  barScores: Record<string, number>;
  overallScore: number;
  scoreBucket: string | null;
}) {
  const bucket = readinessBucket(overallScore);
  return (
    <div>
      {SCORE_COMPONENTS.map((sc) => {
        const val = barScores[sc.key] ?? 0;
        return (
          <div key={sc.key} className="score-inline-row">
            <span className="score-inline-label">
              {sc.label} <span className="score-inline-weight">({sc.weight})</span>
            </span>
            <div className="score-inline-track">
              <div className="score-inline-fill" style={{ width: `${val}%`, background: sc.color }} />
            </div>
            <span className="score-inline-value" style={{ color: sc.color }}>
              {Math.round(val)}
            </span>
          </div>
        );
      })}
      <div className="score-inline-total">
        <span>Placement Readiness</span>
        <div className="score-inline-total-end">
          <span className="score-inline-total-num">{overallScore}</span>
          <span className={`bucket-badge ${bucket.cls}`}>{scoreBucket ?? bucket.label}</span>
        </div>
      </div>
    </div>
  );
}

function SkillLists({ matched, missing }: { matched: string[]; missing: string[] }) {
  if (matched.length === 0 && missing.length === 0) return null;
  return (
    <div className="skill-lists">
      {matched.length > 0 && (
        <p>
          <strong>Matched skills:</strong> {matched.join(", ")}
        </p>
      )}
      {missing.length > 0 && (
        <p className="skill-lists-missing">
          <strong>Missing required:</strong> {missing.join(", ")}
        </p>
      )}
    </div>
  );
}

function WorkspacePageContent() {
  const searchParams = useSearchParams();
  const initialTab = parseWorkspaceTab(searchParams.get("tab"));
  const ws = usePlacementWorkspace(initialTab);
  const [jobsQuery, setJobsQuery] = useState("software engineer");
  const [jobsLoc, setJobsLoc] = useState("India");
  const wizardSteps = useMemo(
    () => [
      {
        id: "resume",
        title: "1. Document Intelligence",
        description: "Upload and parse your resume sections.",
        done: !!ws.parseResult,
      },
      {
        id: "scan",
        title: "2. JD Match Scan",
        description: "Generate scorecard and weighted readiness output.",
        done: !!ws.lastScorecardId,
      },
      {
        id: "readiness",
        title: "3. Readiness Snapshot",
        description: "Inspect readiness bars, bucket, and missing skills.",
        done: !!ws.lastScorecardId,
      },
      {
        id: "rewrite",
        title: "4. Proof-Linked Rewrite",
        description: "Generate evidence-linked rewrites and export-ready output.",
        done: ws.agentRun?.status === "completed" || !!ws.rewriteBundle,
      },
    ],
    [ws.parseResult, ws.lastScorecardId, ws.agentRun?.status, ws.rewriteBundle]
  );

  return (
    <div className="page-canvas">
      <div className="page-title-row">
        <div>
          <h1 className="page-title">Resume & ATS Engine</h1>
          <p className="page-subtitle">Optimize and validate your profile against global ATS standards.</p>
        </div>
        {ws.lastScorecardId ? (
          <span className="chip chip-mono">Scorecard #{ws.lastScorecardId}</span>
        ) : null}
      </div>

      <div className="workspace-tabs" role="tablist">
        {TABS.map(([t, label]) => (
          <button
            key={t}
            type="button"
            role="tab"
            className={`workspace-tab${ws.tab === t ? " workspace-tab--active" : ""}`}
            onClick={() => ws.setTab(t)}
          >
            {label}
          </button>
        ))}
      </div>

      {ws.tab === "resume" && (
        <div className="workspace-grid">
          <div className="content-card">
            <div className="content-card-header">
              <h2 className="content-card-title">Document Intelligence</h2>
              {ws.parseResult ? (
                <span className="chip chip-mono">
                  {ws.parseResult.char_count.toLocaleString()} chars · {ws.parseResult.sections.length} sections
                </span>
              ) : null}
            </div>
            <div className="content-card-body">
              {!ws.parseResult ? (
                <ResumeDropzone
                  disabled={!ws.canUpload}
                  uploading={ws.uploading}
                  error={ws.uploadError}
                  onFile={(file) => void ws.uploadResume(file)}
                />
              ) : (
                <div>
                  {ws.parseResult.ats_flags.length > 0 && (
                    <div className="ats-warning-panel">
                      <p className="ats-warning-title">
                        Structural ATS Warnings ({ws.parseResult.ats_flags.length})
                      </p>
                      <ul className="ats-warning-list">
                        {ws.parseResult.ats_flags.map((f) => (
                          <li key={f}>
                            <span>{f}</span>
                            <span className="ats-flag-badge">HIGH RISK</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  <p className="section-list-heading">Extracted Taxonomy</p>
                  <div className="section-list">
                    {ws.parseResult.sections.map((s) => (
                      <div key={s.section_name} className="section-list-item">
                        <div>
                          <p className="section-list-name">{s.section_name}</p>
                          {typeof s.content_json.cgpa === "string" && (
                            <p className="section-list-meta">CGPA: {s.content_json.cgpa}</p>
                          )}
                        </div>
                        <span className="section-conf-badge">{Math.round(s.confidence * 100)}% CONF</span>
                      </div>
                    ))}
                  </div>

                  <button type="button" className="btn-secondary" onClick={ws.replaceResume}>
                    Replace resume
                  </button>
                </div>
              )}
            </div>
          </div>

          <div className="content-card">
            <div className="content-card-header">
              <h2 className="content-card-title">Generation Matrix</h2>
            </div>
            <div className="content-card-body">
              <label className="auth-label" htmlFor="template-select">
                Template Architecture
              </label>
              <select
                id="template-select"
                className="auth-input workspace-select"
                value={ws.template}
                onChange={(e) => ws.setTemplate(e.target.value as typeof ws.template)}
              >
                {TEMPLATE_OPTIONS.map((opt) => (
                  <option key={opt.value} value={opt.value}>
                    {opt.label}
                  </option>
                ))}
              </select>
              <pre className="resume-preview-snippet">{ws.resumePreview}</pre>
              <button
                type="button"
                className="btn-primary btn-block"
                disabled={!ws.canGenerate || ws.generating}
                onClick={() => void ws.generateResume()}
              >
                {ws.generating ? "Generating…" : "Generate Document"}
              </button>
              <div className="export-actions">
                <button
                  type="button"
                  className="btn-secondary btn-flex"
                  disabled={!ws.canExport}
                  onClick={() => void ws.queueExport()}
                >
                  Queue ATS-safe PDF
                </button>
                <button
                  type="button"
                  className="btn-icon"
                  title="Refresh export status"
                  disabled={!ws.exportJobId}
                  onClick={() => void ws.refreshExportStatus()}
                >
                  ↻
                </button>
                {ws.exportReady && (
                  <button type="button" className="btn-secondary btn-flex" onClick={() => void ws.downloadExport()}>
                    Download PDF
                  </button>
                )}
              </div>
              {ws.exportJobId ? (
                <p className="export-status-line">
                  Export job #{ws.exportJobId}: <strong>{ws.exportStatus || "queued"}</strong>
                </p>
              ) : null}
              {ws.actionError ? (
                <p className="workspace-error" role="alert">
                  {ws.actionError}
                </p>
              ) : null}
            </div>
          </div>
        </div>
      )}

      {ws.tab === "scan" && (
        <div className="content-card">
          <div className="content-card-header">
            <h2 className="content-card-title">Job Description Match</h2>
          </div>
          <div className="content-card-body">
            <div className="scan-grid">
              <div>
                <p className="scan-intro">
                  Paste the target Job Description to score placement readiness via match-engine + scoring
                  package.
                </p>
                {!ws.parseResult && (
                  <div className="scan-hint-banner">Upload your resume first on the Document Intelligence tab.</div>
                )}
                <textarea
                  className="jd-textarea"
                  value={ws.jdText}
                  onChange={(e) => ws.setJdText(e.target.value)}
                  placeholder="Paste JD here…"
                  rows={8}
                />
                <button
                  type="button"
                  className="btn-primary"
                  disabled={!ws.canScan || ws.scanning}
                  onClick={() => void ws.runPlacementScore()}
                >
                  {ws.scanning ? "Scoring…" : "Run Placement Score"}
                </button>
                {ws.scanError ? (
                  <p className="workspace-error" role="alert">
                    {ws.scanError}
                  </p>
                ) : null}
              </div>

              <div>
                <p className="section-list-heading">Diagnostic Results</p>
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
                  <p className="scan-empty">Score will appear here after you run placement scoring.</p>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {ws.tab === "readiness" && (
        <div>
          {!ws.parseResult ? (
            <div className="content-card">
              <div className="content-card-body scan-empty-state">
                <p>Upload your resume to see your readiness snapshot.</p>
                <button type="button" className="btn-primary" onClick={() => ws.setTab("resume")}>
                  Go to Document Intelligence
                </button>
              </div>
            </div>
          ) : (
            <div className="readiness-stack">
              <div className="intel-panel">
                <div className="intel-panel-header">
                  <p className="intel-panel-sub">Placement Readiness · packages/scoring formula</p>
                  <h2 className="intel-panel-title">Readiness Snapshot</h2>
                </div>
                <div className="intel-panel-body">
                  {ws.hasScore && ws.barScores && ws.overallScore !== null ? (
                    <ScoreBreakdown
                      barScores={ws.barScores}
                      overallScore={ws.overallScore}
                      scoreBucket={ws.scoreBucket}
                      semanticMethod={ws.semanticMethod}
                    />
                  ) : (
                    <div className="intel-panel-cta">
                      <p>Run JD Match Scan to compute your full placement readiness score.</p>
                      <button type="button" className="btn-glass" onClick={() => ws.setTab("scan")}>
                        Go to JD Match Scan
                      </button>
                    </div>
                  )}
                  {ws.hasScore && ws.canRewrite ? (
                    <div className="intel-panel-cta" style={{ marginTop: 16 }}>
                      <button type="button" className="btn-primary" onClick={() => void ws.runProofRewrite()}>
                        Generate proof-linked rewrite
                      </button>
                    </div>
                  ) : null}
                </div>
              </div>

              <div className="content-card">
                <div className="content-card-header">
                  <h2 className="content-card-title">Extracted Profile Summary</h2>
                  <span className="chip chip-success">{ws.parseResult.sections.length} sections extracted</span>
                </div>
                <div className="content-card-body">
                  <div className="profile-summary-grid">
                    {ws.parseResult.sections.map((s) => (
                      <div key={s.section_name} className="profile-summary-card">
                        <p className="profile-summary-name">{s.section_name}</p>
                        <p className="profile-summary-conf">{Math.round(s.confidence * 100)}% confidence</p>
                      </div>
                    ))}
                  </div>
                  {ws.parseResult.ats_flags.length > 0 && (
                    <div className="ats-warning-panel ats-warning-panel--compact">
                      <p className="ats-warning-title">ATS Risk Flags</p>
                      <ul className="ats-warning-bullets">
                        {ws.parseResult.ats_flags.map((f) => (
                          <li key={f}>{f}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {ws.tab === "rewrite" && (
        <div className="content-card">
          <div className="content-card-header">
            <h2 className="content-card-title">Proof-Linked Rewrite</h2>
            {ws.lastScorecardId ? (
              <span className="chip chip-mono">Scorecard #{ws.lastScorecardId}</span>
            ) : null}
          </div>
          <div className="content-card-body">
            {!ws.lastScorecardId ? (
              <div className="scan-empty-state">
                <p>Complete JD Match Scan first to unlock proof-linked rewrites.</p>
                <button type="button" className="btn-primary" onClick={() => ws.setTab("scan")}>
                  Go to JD Match Scan
                </button>
              </div>
            ) : (
              <RewriteDiffPanel
                bundle={
                  ws.rewriteBundle
                    ? {
                        top_issues: ws.rewriteBundle.top_issues,
                        section_rewrites: ws.rewriteBundle.section_rewrites,
                        unsupported_claims: ws.rewriteBundle.unsupported_claims,
                        requires_confirmation: ws.rewriteBundle.requires_confirmation,
                      }
                    : null
                }
                loading={ws.rewriting}
                error={ws.rewriteError}
                canRun={ws.canRewrite}
                source="manual"
                onRunRewrite={() => void ws.runProofRewrite()}
              />
            )}
          </div>
        </div>
      )}

      {ws.tab === "jobs" && (
        <div className="readiness-stack">
          <div className="content-card">
            <div className="content-card-header">
              <h2 className="content-card-title">Real-time Jobs Search</h2>
            </div>
            <div className="content-card-body">
              <div className="scan-grid">
                <input
                  className="auth-input"
                  value={jobsQuery}
                  onChange={(e) => setJobsQuery(e.target.value)}
                  placeholder="Role keyword"
                />
                <input
                  className="auth-input"
                  value={jobsLoc}
                  onChange={(e) => setJobsLoc(e.target.value)}
                  placeholder="Location"
                />
              </div>
              <button
                type="button"
                className="btn-primary"
                disabled={ws.jobsLoading}
                onClick={() => void ws.searchJobs(jobsQuery, jobsLoc, 1)}
              >
                {ws.jobsLoading ? "Searching..." : "Search jobs"}
              </button>
              {ws.jobsError ? (
                <p className="workspace-error" role="alert">
                  {ws.jobsError}
                </p>
              ) : null}
            </div>
          </div>
          {ws.jobs.map((job) => (
            <JobCard
              key={job.id}
              job={job}
              busy={false}
              onRunAgent={(jobId) => void ws.runAgent({ job_id: jobId })}
            />
          ))}
        </div>
      )}

      {ws.tab === "builder" && (
        <div className="readiness-stack">
          <BuilderWizard steps={wizardSteps} />
          <div className="content-card">
            <div className="content-card-header">
              <h2 className="content-card-title">Auto Mode</h2>
            </div>
            <div className="content-card-body">
              <p className="scan-intro">
                Auto mode runs parse-safety, JD match, scoring, proof-linked rewrite, and PDF export in one flow.
              </p>
              <button
                type="button"
                className="btn-primary"
                disabled={!ws.canRunAgent}
                onClick={() => void ws.runAgent({ job_query: jobsQuery, location: jobsLoc })}
              >
                Run deterministic agent
              </button>
              {ws.agentError ? (
                <p className="workspace-error" role="alert">
                  {ws.agentError}
                </p>
              ) : null}
            </div>
          </div>
          <AgentProgress run={ws.agentRun} polling={ws.agentPolling} onRefresh={() => void ws.refreshAgentRun()} />
          {ws.rewriteBundle ? (
            <RewriteDiffPanel
              bundle={{
                top_issues: ws.rewriteBundle.top_issues,
                section_rewrites: ws.rewriteBundle.section_rewrites,
                unsupported_claims: ws.rewriteBundle.unsupported_claims,
                requires_confirmation: ws.rewriteBundle.requires_confirmation,
              }}
              loading={ws.rewriting}
              error={ws.rewriteError}
              canRun={ws.canRewrite}
              source="agent"
              onRunRewrite={() => void ws.runProofRewrite()}
            />
          ) : null}
        </div>
      )}

      {ws.tab === "assistant" && (
        <div className="readiness-stack">
          <AssistantPanel />
        </div>
      )}
    </div>
  );
}

export default function WorkspacePage() {
  return (
    <Suspense
      fallback={
        <p style={{ fontFamily: "var(--font-mono)", fontSize: "0.82rem", color: "#717783" }}>Loading workspace…</p>
      }
    >
      <WorkspacePageContent />
    </Suspense>
  );
}
