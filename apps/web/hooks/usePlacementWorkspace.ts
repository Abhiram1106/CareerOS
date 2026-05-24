"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import {
  api,
  type AgentRunResult,
  type JobSearchItem,
  type ParseResult,
  type RewriteResult,
  type ScorecardResult,
} from "../lib/api";
import { getStoredAuth } from "../lib/auth";
import { toErrorMessage } from "../lib/errors";
import {
  normalizeAtsFlags,
  scorecardToBarScores,
  type ScoreComponentKey,
  type TemplateName,
} from "../lib/placement";

export type WorkspaceTab = "resume" | "scan" | "readiness" | "rewrite" | "jobs" | "builder" | "assistant";

const WORKSPACE_TABS: WorkspaceTab[] = [
  "resume",
  "scan",
  "readiness",
  "rewrite",
  "jobs",
  "builder",
  "assistant",
];

export function parseWorkspaceTab(raw: string | null): WorkspaceTab {
  return WORKSPACE_TABS.includes(raw as WorkspaceTab) ? (raw as WorkspaceTab) : "resume";
}

type BarScores = Record<ScoreComponentKey, number> | null;

export function usePlacementWorkspace(initialTab: WorkspaceTab = "resume") {
  const auth = getStoredAuth();
  const token = auth?.token ?? "";

  const [tab, setTab] = useState<WorkspaceTab>(initialTab);

  useEffect(() => {
    setTab(initialTab);
  }, [initialTab]);
  const [parseResult, setParseResult] = useState<ParseResult | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);

  const [jdText, setJdText] = useState("");
  const [scanning, setScanning] = useState(false);
  const [scanError, setScanError] = useState<string | null>(null);
  const [barScores, setBarScores] = useState<BarScores>(null);
  const [overallScore, setOverallScore] = useState<number | null>(null);
  const [scoreBucket, setScoreBucket] = useState<string | null>(null);
  const [missingSkills, setMissingSkills] = useState<string[]>([]);
  const [matchedSkills, setMatchedSkills] = useState<string[]>([]);
  const [lastScorecardId, setLastScorecardId] = useState<number | null>(null);
  const [semanticMethod, setSemanticMethod] = useState<string | null>(null);

  const [rewriteBundle, setRewriteBundle] = useState<RewriteResult | null>(null);
  const [rewriting, setRewriting] = useState(false);
  const [rewriteError, setRewriteError] = useState<string | null>(null);

  const [jobs, setJobs] = useState<JobSearchItem[]>([]);
  const [jobsLoading, setJobsLoading] = useState(false);
  const [jobsError, setJobsError] = useState<string | null>(null);
  const [agentRun, setAgentRun] = useState<AgentRunResult | null>(null);
  const [agentPolling, setAgentPolling] = useState(false);
  const [agentError, setAgentError] = useState<string | null>(null);

  const [template, setTemplate] = useState<TemplateName>("classic");
  const [resumePreview, setResumePreview] = useState("");
  const [generating, setGenerating] = useState(false);
  const [exportJobId, setExportJobId] = useState<number | null>(null);
  const [exportStatus, setExportStatus] = useState("");
  const [actionError, setActionError] = useState<string | null>(null);

  const [profileReady, setProfileReady] = useState(false);

  const canScan = Boolean(token && parseResult && jdText.trim().length >= 20);
  const canUpload = Boolean(token);
  const canGenerate = Boolean(token && profileReady);
  const canExport = Boolean(token && parseResult?.resume_id);
  const canRewrite = Boolean(token && lastScorecardId);
  const canRunAgent = Boolean(token && parseResult?.resume_id);

  const hydrateProfile = useCallback(async () => {
    if (!token) return;
    try {
      const p = (await api.getProfile(token)) as {
        city: string;
        professional_status: string;
        target_role: string;
        skills_csv: string;
        summary: string;
        experience_bullet: string;
        full_name: string;
      };
      setResumePreview(
        `${p.full_name || auth?.full_name || "Your Name"}\n${p.target_role || "Target Role"}\n\n` +
          `Summary\n${p.summary || "—"}\n\nExperience\n- ${p.experience_bullet || "—"}\n\n` +
          `Skills\n${p.skills_csv || "—"}`
      );
      setProfileReady(true);
    } catch {
      setProfileReady(false);
    }
  }, [token, auth?.full_name]);

  useEffect(() => {
    void hydrateProfile();
  }, [hydrateProfile]);

  const resetScore = useCallback(() => {
    setBarScores(null);
    setOverallScore(null);
    setScoreBucket(null);
    setMissingSkills([]);
    setMatchedSkills([]);
    setLastScorecardId(null);
    setSemanticMethod(null);
    setScanError(null);
    setRewriteBundle(null);
    setRewriteError(null);
    setAgentRun(null);
    setAgentError(null);
  }, []);

  const applyScorecard = useCallback((res: ScorecardResult) => {
    setBarScores(scorecardToBarScores(res));
    setOverallScore(res.overall_score);
    setScoreBucket(res.bucket);
    setMissingSkills(res.missing_required_skills);
    setMatchedSkills(res.matched_skills);
    setLastScorecardId(res.scorecard_id);
    setSemanticMethod(res.semantic_method ?? "char_ngram_proxy");
  }, []);

  const uploadResume = useCallback(
    async (file: File) => {
      if (!token) {
        setUploadError("Sign in to upload a resume.");
        return;
      }
      setUploading(true);
      setUploadError(null);
      resetScore();
      try {
        const result = await api.uploadResume(token, file);
        setParseResult(result);
        setTab("readiness");
      } catch (err) {
        setUploadError(toErrorMessage(err, "Upload failed"));
      } finally {
        setUploading(false);
      }
    },
    [token, resetScore]
  );

  const runPlacementScore = useCallback(async () => {
    if (!token || !parseResult || !jdText.trim()) return;
    setScanning(true);
    setScanError(null);
    try {
      const res = await api.scoreResume(token, {
        resume_id: parseResult.resume_id,
        jd_text: jdText.trim(),
        ats_flags: normalizeAtsFlags(parseResult.ats_flags),
      });
      applyScorecard(res);
      setTab("readiness");
    } catch (err) {
      setScanError(toErrorMessage(err, "Placement score failed"));
      resetScore();
    } finally {
      setScanning(false);
    }
  }, [token, parseResult, jdText, applyScorecard, resetScore]);

  const runProofRewrite = useCallback(async () => {
    if (!token || !lastScorecardId) return;
    setRewriting(true);
    setRewriteError(null);
    try {
      const res = await api.runRewrite(token, lastScorecardId);
      setRewriteBundle(res);
      setTab("rewrite");
    } catch (err) {
      setRewriteError(toErrorMessage(err, "Rewrite failed"));
    } finally {
      setRewriting(false);
    }
  }, [token, lastScorecardId]);

  const searchJobs = useCallback(
    async (query: string, location = "", page = 1) => {
      if (!token) {
        setJobsError("Sign in to search jobs.");
        return;
      }
      setJobsLoading(true);
      setJobsError(null);
      try {
        const res = await api.searchJobs(token, query, location, page);
        setJobs(res.results);
      } catch (err) {
        setJobsError(toErrorMessage(err, "Job search failed"));
        setJobs([]);
      } finally {
        setJobsLoading(false);
      }
    },
    [token]
  );

  const runAgent = useCallback(
    async (payload: { job_id?: number; jd_text?: string; job_query?: string; location?: string }) => {
      if (!token || !parseResult?.resume_id) {
        setAgentError("Upload a resume first.");
        return;
      }
      setAgentError(null);
      try {
        const res = await api.runAgent(token, {
          resume_id: parseResult.resume_id,
          ats_flags: parseResult.ats_flags,
          ...payload,
        });
        setAgentRun(res);
      } catch (err) {
        setAgentError(toErrorMessage(err, "Agent run failed"));
      }
    },
    [token, parseResult]
  );

  const refreshAgentRun = useCallback(async () => {
    if (!token || !agentRun?.run_id) return;
    setAgentPolling(true);
    try {
      const latest = await api.getAgentRun(token, agentRun.run_id);
      setAgentRun(latest);
    } catch (err) {
      setAgentError(toErrorMessage(err, "Agent status refresh failed"));
    } finally {
      setAgentPolling(false);
    }
  }, [token, agentRun?.run_id]);

  const replaceResume = useCallback(() => {
    setParseResult(null);
    resetScore();
    setTab("resume");
  }, [resetScore]);

  const generateResume = useCallback(async () => {
    if (!token) return;
    setGenerating(true);
    setActionError(null);
    try {
      const res = await api.generateResume(token, { template_name: template });
      setResumePreview(res.content);
    } catch (err) {
      setActionError(toErrorMessage(err, "Resume generation failed"));
    } finally {
      setGenerating(false);
    }
  }, [token, template]);

  const queueExport = useCallback(async () => {
    if (!token || !parseResult?.resume_id) return;
    setActionError(null);
    try {
      const job = await api.exportResume(token, parseResult.resume_id);
      setExportJobId(job.job_id);
      setExportStatus(job.status);
    } catch (err) {
      setActionError(toErrorMessage(err, "Export queue failed"));
    }
  }, [token, parseResult?.resume_id]);

  const refreshExportStatus = useCallback(async () => {
    if (!token || !exportJobId) return;
    try {
      const data = await api.exportStatus(token, exportJobId);
      setExportStatus(data.status);
    } catch (err) {
      setActionError(toErrorMessage(err, "Could not refresh export status"));
    }
  }, [token, exportJobId]);

  const downloadExport = useCallback(async () => {
    if (!token || !exportJobId) return;
    try {
      const blob = await api.downloadExport(token, exportJobId);
      const url = window.URL.createObjectURL(blob);
      const anchor = document.createElement("a");
      anchor.href = url;
      anchor.download = `resume_export_${exportJobId}.pdf`;
      anchor.click();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setActionError(toErrorMessage(err, "Export download failed"));
    }
  }, [token, exportJobId]);

  const hasScore = barScores !== null && overallScore !== null;

  const exportReady = useMemo(
    () => exportStatus === "completed" || exportStatus === "complete",
    [exportStatus]
  );

  return {
    auth,
    tab,
    setTab,
    parseResult,
    uploading,
    uploadError,
    canUpload,
    uploadResume,
    replaceResume,
    jdText,
    setJdText,
    scanning,
    scanError,
    canScan,
    runPlacementScore,
    barScores,
    overallScore,
    scoreBucket,
    missingSkills,
    matchedSkills,
    lastScorecardId,
    semanticMethod,
    hasScore,
    template,
    setTemplate,
    resumePreview,
    generating,
    canGenerate,
    generateResume,
    exportJobId,
    exportStatus,
    exportReady,
    canExport,
    queueExport,
    refreshExportStatus,
    downloadExport,
    actionError,
    rewriteBundle,
    rewriting,
    rewriteError,
    canRewrite,
    runProofRewrite,
    jobs,
    jobsLoading,
    jobsError,
    searchJobs,
    agentRun,
    agentPolling,
    agentError,
    canRunAgent,
    runAgent,
    refreshAgentRun,
  };
}
