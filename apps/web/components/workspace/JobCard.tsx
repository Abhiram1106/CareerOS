import type { JobSearchItem } from "../../lib/api";

type Props = {
  job: JobSearchItem;
  onRunAgent: (jobId: number) => void;
  busy?: boolean;
};

export function JobCard({ job, onRunAgent, busy = false }: Props) {
  return (
    <article className="content-card">
      <div className="content-card-header">
        <h3 className="content-card-title">{job.title}</h3>
        <span className="chip chip-mono">#{job.id}</span>
      </div>
      <div className="content-card-body">
        <p className="scan-intro">
          <strong>{job.company}</strong> · {job.location}
        </p>
        {job.skills_required.length > 0 ? (
          <p className="scan-intro">Skills: {job.skills_required.join(", ")}</p>
        ) : null}
        <p className="scan-intro">
          {job.raw_jd_text.length > 220 ? `${job.raw_jd_text.slice(0, 220)}...` : job.raw_jd_text}
        </p>
        <button type="button" className="btn-primary" disabled={busy} onClick={() => onRunAgent(job.id)}>
          {busy ? "Running agent..." : "Run agent on this job"}
        </button>
      </div>
    </article>
  );
}
