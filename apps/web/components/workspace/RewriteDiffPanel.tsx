"use client";

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

export function RewriteDiffPanel({ bundle, loading, error, onRunRewrite, canRun, source = "manual" }: Props) {
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
            </article>
          ))}
        </div>
      ) : bundle ? (
        <p className="scan-empty">No section rewrites returned. Check resume sections and try again.</p>
      ) : null}
    </div>
  );
}
