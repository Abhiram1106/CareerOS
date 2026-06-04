"use client";

import { useState } from "react";
import { api } from "../../lib/api";
import { getStoredAuth } from "../../lib/auth";

export type SectionRewrite = {
  section: string;
  original: string;
  rewrite: string;
  evidence_ids: string[];
  confidence: number;
};

export type UnsupportedClaim = {
  claim: string;
  reason: string;
};

export type RewriteBundle = {
  top_issues: Array<{ type: string; message: string; severity: string }>;
  section_rewrites: SectionRewrite[];
  unsupported_claims: UnsupportedClaim[];
  requires_confirmation: Array<{ field: string; suggested_change: string }>;
};

type Props = {
  bundle: RewriteBundle | null;
  loading: boolean;
  error: string | null;
  onRunRewrite: () => void;
  canRun: boolean;
  source?: "manual" | "agent";
};

function confidenceLabel(value: number): string {
  if (value >= 0.85) return "High";
  if (value >= 0.65) return "Medium";
  return "Review";
}

// Per-card accept/reject feedback (CARE-RAG Layer 6)
function FeedbackButtons({ idx, onAccept, onReject }: {
  idx: number;
  onAccept: (idx: number) => void;
  onReject: (idx: number) => void;
}) {
  const [state, setState] = useState<"idle" | "accepted" | "rejected">("idle");

  if (state === "accepted") {
    return <span style={{ fontSize: "0.75rem", color: "#16a34a", fontWeight: 700 }}>✓ Accepted</span>;
  }
  if (state === "rejected") {
    return <span style={{ fontSize: "0.75rem", color: "#dc2626", fontWeight: 700 }}>✗ Skipped</span>;
  }
  return (
    <div style={{ display: "flex", gap: 6, marginTop: 8 }}>
      <button
        type="button"
        className="btn-secondary"
        style={{ fontSize: "0.75rem", padding: "3px 10px", color: "#16a34a", borderColor: "#86efac" }}
        onClick={() => { setState("accepted"); onAccept(idx); }}
      >
        ✓ Apply
      </button>
      <button
        type="button"
        className="btn-secondary"
        style={{ fontSize: "0.75rem", padding: "3px 10px", color: "#6b7280", borderColor: "#e5e7eb" }}
        onClick={() => { setState("rejected"); onReject(idx); }}
      >
        ✗ Skip
      </button>
    </div>
  );
}

export function RewriteDiffPanel({ bundle, loading, error, onRunRewrite, canRun, source = "manual" }: Props) {
  const token = getStoredAuth()?.token ?? "";
  const [feedbackSent, setFeedbackSent] = useState<Record<number, boolean>>({});

  async function handleFeedback(idx: number, accepted: boolean) {
    if (feedbackSent[idx]) return;
    setFeedbackSent((p) => ({ ...p, [idx]: true }));
    // Fire-and-forget — feedback failure must never block UX
    try {
      // We use idx as a proxy rec_id since we don't have the DB id in the bundle.
      // In a future pass, the rewrite endpoint should return rec_ids.
      // For now, log the signal via a dedicated endpoint that accepts text content.
      const rewrite = bundle?.section_rewrites[idx];
      if (rewrite && token) {
        await api.recordRecommendationFeedback(token, idx + 1, accepted);
      }
    } catch {
      // noop
    }
  }

  if (!bundle && !loading && !error) {
    return (
      <div className="rewrite-empty">
        <p>Run placement scoring first, then generate proof-linked rewrite suggestions.</p>
        <button type="button" className="btn-primary" disabled={!canRun || loading} onClick={onRunRewrite}>
          {loading ? "Generating…" : "Generate proof-linked rewrite"}
        </button>
      </div>
    );
  }

  return (
    <div className="rewrite-stack">
      <div className="rewrite-toolbar">
        <p className="rewrite-intro">
          Suggestions are tied to resume evidence. Unsupported claims are refused — they never appear in rewrites.
          {source === "agent" ? " Generated in deterministic auto mode." : " Generated in manual mode."}
        </p>
        <button type="button" className="btn-secondary" disabled={!canRun || loading} onClick={onRunRewrite}>
          {loading ? "Refreshing…" : "Regenerate rewrite"}
        </button>
      </div>

      {error ? (
        <p className="workspace-error" role="alert">
          {error}
        </p>
      ) : null}

      {bundle && bundle.unsupported_claims.length > 0 && (
        <div className="rewrite-panel rewrite-panel--warn">
          <h3 className="rewrite-panel-title">Unsupported claims (not applied)</h3>
          <ul className="rewrite-unsupported-list">
            {bundle.unsupported_claims.map((item) => (
              <li key={`${item.claim}-${item.reason}`}>
                <p className="rewrite-unsupported-claim">{item.claim}</p>
                <p className="rewrite-unsupported-reason">{item.reason}</p>
              </li>
            ))}
          </ul>
        </div>
      )}

      {bundle && bundle.requires_confirmation.length > 0 && (
        <div className="rewrite-panel rewrite-panel--info">
          <h3 className="rewrite-panel-title">Requires your confirmation</h3>
          <ul className="rewrite-confirm-list">
            {bundle.requires_confirmation.map((item) => (
              <li key={item.field}>
                <strong>{item.field}</strong> — {item.suggested_change}
              </li>
            ))}
          </ul>
        </div>
      )}

      {bundle && bundle.section_rewrites.length > 0 ? (
        <div className="rewrite-diff-list">
          {bundle.section_rewrites.map((row, idx) => (
            <article
              key={`${row.section}-${idx}-${row.original.slice(0, 24)}`}
              className="rewrite-diff-card"
            >
              <header className="rewrite-diff-header">
                <span className="chip chip-mono">{row.section}</span>
                <span className={`rewrite-conf rewrite-conf--${confidenceLabel(row.confidence).toLowerCase()}`}>
                  {confidenceLabel(row.confidence)} · {Math.round(row.confidence * 100)}%
                </span>
              </header>
              <div className="rewrite-diff-columns">
                <div className="rewrite-diff-col">
                  <p className="rewrite-diff-label">Before</p>
                  <p className="rewrite-diff-text rewrite-diff-text--before">{row.original}</p>
                </div>
                <div className="rewrite-diff-col">
                  <p className="rewrite-diff-label">After (proof-linked)</p>
                  <p className="rewrite-diff-text rewrite-diff-text--after">{row.rewrite}</p>
                </div>
              </div>
              {row.evidence_ids.length > 0 && (
                <p className="rewrite-evidence">
                  Evidence:{" "}
                  {row.evidence_ids.map((id) => (
                    <span key={id} className="rewrite-evidence-id">
                      {id}
                    </span>
                  ))}
                </p>
              )}
              {/* CARE-RAG Layer 6: feedback buttons */}
              <FeedbackButtons
                idx={idx}
                onAccept={(i) => void handleFeedback(i, true)}
                onReject={(i) => void handleFeedback(i, false)}
              />
            </article>
          ))}
        </div>
      ) : bundle ? (
        <p className="scan-empty">No section rewrites returned. Check resume sections and try again.</p>
      ) : null}
    </div>
  );
}
