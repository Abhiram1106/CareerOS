"use client";

import { useCallback, useEffect, useMemo, useState } from "react";

import { AgentProgress } from "../../../../components/workspace/AgentProgress";
import { BuilderWizard } from "../../../../components/workspace/BuilderWizard";
import { JobCard } from "../../../../components/workspace/JobCard";
import { api, type AgentRunResult, type JobSearchItem } from "../../../../lib/api";
import { getStoredAuth } from "../../../../lib/auth";
import { toErrorMessage } from "../../../../lib/errors";

export default function WorkspaceBuilderPage() {
  const token = getStoredAuth()?.token ?? "";

  const [query, setQuery] = useState("backend engineer");
  const [location, setLocation] = useState("India");
  const [jobs, setJobs] = useState<JobSearchItem[]>([]);
  const [loadingJobs, setLoadingJobs] = useState(false);
  const [resumeId, setResumeId] = useState<number | null>(null);
  const [agentRun, setAgentRun] = useState<AgentRunResult | null>(null);
  const [runningJobId, setRunningJobId] = useState<number | null>(null);
  const [polling, setPolling] = useState(false);
  const [error, setError] = useState<string | null>(null);

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

  const searchJobs = useCallback(async () => {
    if (!token) {
      setError("Sign in to search jobs.");
      return;
    }
    setLoadingJobs(true);
    setError(null);
    try {
      const res = await api.searchJobs(token, query, location, 1);
      setJobs(res.results);
    } catch (err) {
      setError(toErrorMessage(err, "Job search failed"));
      setJobs([]);
    } finally {
      setLoadingJobs(false);
    }
  }, [token, query, location]);

  const refreshRun = useCallback(async () => {
    if (!token || !agentRun?.run_id) return;
    setPolling(true);
    try {
      const latest = await api.getAgentRun(token, agentRun.run_id);
      setAgentRun(latest);
    } catch (err) {
      setError(toErrorMessage(err, "Could not refresh run"));
    } finally {
      setPolling(false);
    }
  }, [token, agentRun?.run_id]);

  useEffect(() => {
    if (!agentRun?.run_id) return;
    if (agentRun.status === "completed" || agentRun.status === "failed") return;
    const timer = window.setInterval(() => {
      void refreshRun();
    }, 2500);
    return () => window.clearInterval(timer);
  }, [agentRun, refreshRun]);

  const runAuto = useCallback(
    async (jobId: number) => {
      if (!token) {
        setError("Sign in to run auto mode.");
        return;
      }
      if (!resumeId) {
        setError("Upload a resume first in Workspace.");
        return;
      }
      setRunningJobId(jobId);
      setError(null);
      try {
        const res = await api.runAgent(token, {
          resume_id: resumeId,
          job_id: jobId,
          ats_flags: [],
        });
        setAgentRun(res);
      } catch (err) {
        setError(toErrorMessage(err, "Auto mode failed"));
      } finally {
        setRunningJobId(null);
      }
    },
    [token, resumeId]
  );

  const steps = useMemo(
    () => [
      { id: "resume", title: "1. Document Intelligence", description: "Upload and parse resume sections.", done: !!resumeId },
      { id: "scan", title: "2. JD Match Scan", description: "Compute scorecard with scoring package.", done: !!agentRun?.scorecard_id },
      { id: "readiness", title: "3. Readiness Snapshot", description: "Review weighted readiness components.", done: !!agentRun?.scorecard_id },
      {
        id: "rewrite",
        title: "4. Proof-Linked Rewrite",
        description: "Generate no-fabrication rewrite recommendations and queue export.",
        done: agentRun?.status === "completed",
      },
    ],
    [resumeId, agentRun]
  );

  return (
    <div className="page-canvas">
      <BuilderWizard steps={steps} />

      <section className="content-card">
        <div className="content-card-header">
          <h3 className="content-card-title">Auto Mode (Deterministic Agent)</h3>
        </div>
        <div className="content-card-body">
          <div className="scan-grid">
            <input
              className="auth-input"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Role keyword"
            />
            <input
              className="auth-input"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="Location"
            />
          </div>
          <button type="button" className="btn-primary" disabled={loadingJobs} onClick={() => void searchJobs()}>
            {loadingJobs ? "Loading..." : "Find jobs"}
          </button>
          {error ? (
            <p className="workspace-error" role="alert">
              {error}
            </p>
          ) : null}
        </div>
      </section>

      <AgentProgress run={agentRun} polling={polling} onRefresh={() => void refreshRun()} />

      <div className="readiness-stack">
        {jobs.map((job) => (
          <JobCard key={job.id} job={job} busy={runningJobId === job.id} onRunAgent={(id) => void runAuto(id)} />
        ))}
      </div>
    </div>
  );
}
