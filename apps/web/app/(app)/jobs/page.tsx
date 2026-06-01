"use client";

import { useEffect, useState } from "react";
import { JobCard } from "../../../components/workspace/JobCard";
import { usePlacementWorkspace } from "../../../hooks/usePlacementWorkspace";

export default function JobsPage() {
  const ws = usePlacementWorkspace("jobs");
  const [jobsQuery, setJobsQuery] = useState("software engineer");
  const [jobsLoc, setJobsLoc] = useState("India");

  useEffect(() => {
    if (ws.jobs.length > 0 || ws.jobsLoading) return;
    void ws.searchJobs(jobsQuery, jobsLoc, 1);
  }, [ws.jobs.length, ws.jobsLoading, ws.searchJobs, jobsQuery, jobsLoc]);

  return (
    <div className="page-canvas">
      <div className="page-title-row">
        <div>
          <h1 className="page-title">Jobs</h1>
          <p className="page-subtitle">Discover matching openings and run an agent-assisted relevance pass.</p>
        </div>
      </div>

      <div className="content-card">
        <div className="content-card-header">
          <h2 className="content-card-title">Jobs Search</h2>
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

      <div className="readiness-stack" style={{ marginTop: 16 }}>
        {ws.jobs.map((job) => (
          <JobCard key={job.id} job={job} busy={false} onRunAgent={(jobId) => void ws.runAgent({ job_id: jobId })} />
        ))}
      </div>
    </div>
  );
}
