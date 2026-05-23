"use client";

import { useCallback, useEffect, useState } from "react";

import { JobCard } from "../../../../components/workspace/JobCard";
import { api, type AgentRunResult, type JobSearchItem } from "../../../../lib/api";
import { getStoredAuth } from "../../../../lib/auth";
import { toErrorMessage } from "../../../../lib/errors";

export default function WorkspaceJobsPage() {
  const token = getStoredAuth()?.token ?? "";

  const [query, setQuery] = useState("software engineer");
  const [location, setLocation] = useState("India");
  const [loading, setLoading] = useState(false);
  const [jobs, setJobs] = useState<JobSearchItem[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [resumeId, setResumeId] = useState<number | null>(null);
  const [agentState, setAgentState] = useState<AgentRunResult | null>(null);
  const [runningJobId, setRunningJobId] = useState<number | null>(null);

  useEffect(() => {
    if (!token) return;
    void api
      .listResumes(token)
      .then((res) => {
        const newest = res.resumes[0];
        if (newest) setResumeId(newest.id);
      })
      .catch(() => {
        setResumeId(null);
      });
  }, [token]);

  const runSearch = useCallback(async () => {
    if (!token) {
      setError("Sign in to search jobs.");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const res = await api.searchJobs(token, query, location, 1);
      setJobs(res.results);
    } catch (err) {
      setError(toErrorMessage(err, "Job search failed"));
      setJobs([]);
    } finally {
      setLoading(false);
    }
  }, [token, query, location]);

  const runAgentForJob = useCallback(
    async (jobId: number) => {
      if (!token) {
        setError("Sign in to run agent.");
        return;
      }
      if (!resumeId) {
        setError("Upload a resume first in Workspace > Document Intelligence.");
        return;
      }
      setRunningJobId(jobId);
      setError(null);
      try {
        const result = await api.runAgent(token, {
          resume_id: resumeId,
          job_id: jobId,
          ats_flags: [],
        });
        setAgentState(result);
      } catch (err) {
        setError(toErrorMessage(err, "Agent run failed"));
      } finally {
        setRunningJobId(null);
      }
    },
    [token, resumeId]
  );

  return (
    <div className="page-canvas">
      <div className="content-card">
        <div className="content-card-header">
          <h1 className="content-card-title">Real-time Jobs Feed</h1>
        </div>
        <div className="content-card-body">
          <div className="scan-grid">
            <input
              className="auth-input"
              placeholder="Role keyword"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
            <input
              className="auth-input"
              placeholder="Location"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
            />
          </div>
          <button type="button" className="btn-primary" disabled={loading} onClick={() => void runSearch()}>
            {loading ? "Searching..." : "Search jobs"}
          </button>
          {resumeId ? (
            <p className="scan-intro">Using resume #{resumeId} for agent runs.</p>
          ) : (
            <p className="workspace-error">No uploaded resume found yet.</p>
          )}
          {agentState ? (
            <p className="scan-intro">
              Last run: #{agentState.run_id} · {agentState.current_step} · {agentState.status}
            </p>
          ) : null}
          {error ? (
            <p className="workspace-error" role="alert">
              {error}
            </p>
          ) : null}
        </div>
      </div>

      <div className="readiness-stack">
        {jobs.map((job) => (
          <JobCard
            key={job.id}
            job={job}
            busy={runningJobId === job.id}
            onRunAgent={(id) => void runAgentForJob(id)}
          />
        ))}
        {jobs.length === 0 && !loading ? (
          <div className="content-card">
            <div className="content-card-body scan-empty-state">
              <p>Search for jobs to begin agent-assisted matching.</p>
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
}
