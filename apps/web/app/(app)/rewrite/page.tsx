"use client";

import Link from "next/link";
import { RewriteDiffPanel } from "../../../components/workspace/RewriteDiffPanel";
import { usePlacementWorkspace } from "../../../hooks/usePlacementWorkspace";

export default function RewritePage() {
  const ws = usePlacementWorkspace("rewrite");

  return (
    <div className="page-canvas">
      <div className="page-title-row">
        <div>
          <h1 className="page-title">Proof-Linked Rewrite</h1>
          <p className="page-subtitle">Improve bullets without fabrication, with section-level evidence anchors.</p>
        </div>
      </div>

      <div className="content-card">
        <div className="content-card-header">
          <h2 className="content-card-title">Rewrite Suggestions</h2>
          {ws.lastScorecardId ? <span className="chip chip-mono">Scorecard #{ws.lastScorecardId}</span> : null}
        </div>
        <div className="content-card-body">
          {!ws.lastScorecardId ? (
            <div className="scan-empty-state">
              <p>Run a JD match scan first to generate rewrite recommendations.</p>
              <Link href="/match" className="btn-primary dashboard-action-link">
                Go to JD Match
              </Link>
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
    </div>
  );
}
