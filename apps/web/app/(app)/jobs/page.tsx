"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { JobCard } from "../../../components/workspace/JobCard";
import { usePlacementWorkspace } from "../../../hooks/usePlacementWorkspace";
import type { JobApplication } from "../../../lib/api";
import { api } from "../../../lib/api";
import { getStoredAuth } from "../../../lib/auth";

export default function JobsPage() {
  const ws = usePlacementWorkspace("jobs");
  const token = getStoredAuth()?.token ?? "";
  const [jobsQuery, setJobsQuery] = useState("software engineer");
  const [jobsLoc, setJobsLoc] = useState("India");

  // Map external_id → JobApplication for saved state
  const [savedMap, setSavedMap] = useState<Record<string, JobApplication>>({});

  const loadSaved = useCallback(async () => {
    if (!token) return;
    try {
      const res = await api.listApplications(token);
      const map: Record<string, JobApplication> = {};
      for (const app of res.applications) {
        map[app.job_external_id] = app;
      }
      setSavedMap(map);
    } catch {
      // noop
    }
  }, [token]);

  useEffect(() => {
    void loadSaved();
  }, [loadSaved]);

  useEffect(() => {
    if (ws.jobs.length > 0 || ws.jobsLoading) return;
    void ws.searchJobs(jobsQuery, jobsLoc, 1);
  }, [ws.jobs.length, ws.jobsLoading, ws.searchJobs, jobsQuery, jobsLoc]);

  function handleSaved(app: JobApplication) {
    setSavedMap((prev) => ({ ...prev, [app.job_external_id]: app }));
  }

  return (
    <div className="page-canvas">
      <div className="page-title-row">
        <div>
          <h1 className="page-title">Jobs</h1>
          <p className="page-subtitle">Discover matching openings, save them, and track your applications.</p>
        </div>
        <Link href="/applications" className="btn-secondary" style={{ alignSelf: "center", whiteSpace: "nowrap" }}>
          My applications ({Object.keys(savedMap).length})
        </Link>
      </div>

      <div className="content-card">
        <div className="content-card-header">
          <h2 className="content-card-title">Search</h2>
        </div>
        <div className="content-card-body">
          <div className="scan-grid">
            <input
              className="auth-input"
              value={jobsQuery}
              onChange={(e) => setJobsQuery(e.target.value)}
              onKeyDown={(e) => { if (e.key === "Enter") void ws.searchJobs(jobsQuery, jobsLoc, 1); }}
              placeholder="Role keyword"
            />
            <input
              className="auth-input"
              value={jobsLoc}
              onChange={(e) => setJobsLoc(e.target.value)}
              onKeyDown={(e) => { if (e.key === "Enter") void ws.searchJobs(jobsQuery, jobsLoc, 1); }}
              placeholder="Location"
            />
          </div>
          <button
            type="button"
            className="btn-primary"
            disabled={ws.jobsLoading}
            onClick={() => void ws.searchJobs(jobsQuery, jobsLoc, 1)}
          >
            {ws.jobsLoading ? "Searching…" : "Search jobs"}
          </button>
          {ws.jobsError ? <p className="workspace-error" role="alert">{ws.jobsError}</p> : null}
        </div>
      </div>

      <div className="readiness-stack" style={{ marginTop: 16 }}>
        {ws.jobs.map((job) => (
          <JobCard
            key={job.id}
            job={job}
            busy={false}
            savedApplication={savedMap[job.external_id] ?? null}
            onSaved={handleSaved}
            onRunAgent={(jobId) => void ws.runAgent({ job_id: jobId })}
          />
        ))}
        {!ws.jobsLoading && ws.jobs.length === 0 && (
          <div className="content-card">
            <div className="content-card-body scan-empty-state">
              <p>Search for a role above to see matching jobs.</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
