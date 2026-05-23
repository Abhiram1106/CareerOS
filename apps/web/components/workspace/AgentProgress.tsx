import type { AgentRunResult } from "../../lib/api";

type Props = {
  run: AgentRunResult | null;
  polling: boolean;
  onRefresh: () => void;
};

export function AgentProgress({ run, polling, onRefresh }: Props) {
  return (
    <section className="content-card">
      <div className="content-card-header">
        <h3 className="content-card-title">Agent Progress</h3>
      </div>
      <div className="content-card-body">
        {!run ? (
          <p className="scan-empty">Start an auto run to see live progress.</p>
        ) : (
          <>
            <p className="scan-intro">
              Run #{run.run_id} · Step <strong>{run.current_step}</strong> · Status <strong>{run.status}</strong>
            </p>
            {run.scorecard_id ? <p className="scan-intro">Scorecard #{run.scorecard_id}</p> : null}
            {run.export_job_id ? <p className="scan-intro">Export job #{run.export_job_id}</p> : null}
            <button type="button" className="btn-secondary" onClick={onRefresh} disabled={polling}>
              {polling ? "Refreshing..." : "Refresh progress"}
            </button>
          </>
        )}
      </div>
    </section>
  );
}
