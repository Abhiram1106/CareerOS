"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import {
  api,
  type AgentRunResult,
  type ATSCheck,
  type ATSIssue,
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
import { useToast } from "../components/ui/toast";

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

const PERSIST_KEY = "cos_workspace_state_v1";

type BarScores = Record<ScoreComponentKey, number> | null;

type PersistedWorkspaceState = {
  resume_id: number | null;
  jd_text: string;
  tab: WorkspaceTab;
  export_status?: string;
  score_snapshot: {
    bar_scores: Record<ScoreComponentKey, number>;
    overall_score: number;
    score_bucket: string | null;
    missing_skills: string[];
    matched_skills: string[];
    semantic_method: string | null;
    scorecard_id: number | null;
    ats_checks: ATSCheck[];
    ats_issues: ATSIssue[];
    ats_bucket: string | null;
  } | null;
};

export function parseWorkspaceTab(raw: string | null): WorkspaceTab {
  return WORKSPACE_TABS.includes(raw as WorkspaceTab) ? (raw as WorkspaceTab) : "resume";
}

function safeReadPersistedState(): PersistedWorkspaceState | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = localStorage.getItem(PERSIST_KEY);
    if (!raw) return null;
    return JSON.parse(raw) as PersistedWorkspaceState;
  } catch {
    return null;
  }
}

function safeWritePersistedState(state: PersistedWorkspaceState): void {
  if (typeof window === "undefined") return;
  try {
    localStorage.setItem(PERSIST_KEY, JSON.stringify(state));
  } catch {
    // noop
  }
}

export function usePlacementWorkspace(initialTab: WorkspaceTab = "resume") {
  const auth = getStoredAuth();
  const token = auth?.token ?? "";
  const { push } = useToast();

  const [tab, setTab] = useState<WorkspaceTab>(initialTab);
  const [hasHydrated, setHasHydrated] = useState(false);

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
  const [atsChecks, setAtsChecks] = useState<ATSCheck[]>([]);
  const [atsIssues, setAtsIssues] = useState<ATSIssue[]>([]);
  const [atsBucket, setAtsBucket] = useState<string | null>(null);

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
          `Summary\n${p.summary || "-"}\n\nExperience\n- ${p.experience_bullet || "-"}\n\n` +
          `Skills\n${p.skills_csv || "-"}`
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
    setAtsChecks([]);
    setAtsIssues([]);
    setAtsBucket(null);
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
    setAtsChecks(res.ats_checks ?? []);
    setAtsIssues(res.ats_issues ?? []);
    setAtsBucket(res.ats_bucket ?? null);
  }, []);

  const hydrateResumeFromId = useCallback(
    async (resumeId: number) => {
      if (!token) return;
      try {
        const details = await api.getResumeSections(token, resumeId);
        const charCount = details.sections.reduce((acc, section) => {
          return acc + JSON.stringify(section.content_json).length;
        }, 0);
        setParseResult({
          resume_id: details.resume_id,
          source_format: details.source_format,
          sections: details.sections,
          ats_flags: [],
          parse_warnings: [],
          char_count: charCount,
        });
      } catch {
        setParseResult(null);
      }
    },
    [token]
  );

  useEffect(() => {
    if (!token || hasHydrated) return;
    const persisted = safeReadPersistedState();

    if (persisted?.jd_text) {
      setJdText(persisted.jd_text);
    }
    if (persisted?.score_snapshot) {
      setBarScores(persisted.score_snapshot.bar_scores);
      setOverallScore(persisted.score_snapshot.overall_score);
      setScoreBucket(persisted.score_snapshot.score_bucket);
      setMissingSkills(persisted.score_snapshot.missing_skills);
      setMatchedSkills(persisted.score_snapshot.matched_skills);
      setSemanticMethod(persisted.score_snapshot.semantic_method);
      setLastScorecardId(persisted.score_snapshot.scorecard_id);
      setAtsChecks(persisted.score_snapshot.ats_checks ?? []);
      setAtsIssues(persisted.score_snapshot.ats_issues ?? []);
      setAtsBucket(persisted.score_snapshot.ats_bucket ?? null);
    }
    if (persisted?.tab && persisted.tab !== initialTab) {
      setTab(persisted.tab);
    }

    const resumeId = persisted?.resume_id;
    const bootstrap = async () => {
      if (resumeId) {
        await hydrateResumeFromId(resumeId);
      } else {
        try {
          const list = await api.listResumes(token);
          const latest = list.resumes[0];
          if (latest) {
            await hydrateResumeFromId(latest.id);
          }
        } catch {
          // noop
        }
      }
      setHasHydrated(true);
    };
    void bootstrap();
  }, [token, hasHydrated, hydrateResumeFromId, initialTab]);

  useEffect(() => {
    if (!token) return;
    const scoreSnapshot =
      barScores && overallScore !== null
        ? {
            bar_scores: barScores,
            overall_score: overallScore,
            score_bucket: scoreBucket,
            missing_skills: missingSkills,
            matched_skills: matchedSkills,
            semantic_method: semanticMethod,
            scorecard_id: lastScorecardId,
            ats_checks: atsChecks,
            ats_issues: atsIssues,
            ats_bucket: atsBucket,
          }
        : null;

    safeWritePersistedState({
      resume_id: parseResult?.resume_id ?? null,
      jd_text: jdText,
      tab,
      score_snapshot: scoreSnapshot,
    });
  }, [
    token,
    parseResult?.resume_id,
    jdText,
    tab,
    barScores,
    overallScore,
    scoreBucket,
    missingSkills,
    matchedSkills,
    semanticMethod,
    lastScorecardId,
    atsChecks,
    atsIssues,
    atsBucket,
  ]);

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
        push({
          title: "Resume uploaded",
          message: `${result.sections.length} sections extracted`,
          variant: "success",
        });
      } catch (err) {
        const message = toErrorMessage(err, "Upload failed");
        setUploadError(message);
        push({ title: "Upload failed", message, variant: "error" });
      } finally {
        setUploading(false);
      }
    },
    [token, resetScore, push]
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
      push({
        title: "Score updated",
        message: `Readiness score ${res.overall_score} (${res.bucket})`,
        variant: "success",
      });
    } catch (err) {
      const message = toErrorMessage(err, "Placement score failed");
      setScanError(message);
      resetScore();
      push({ title: "Scoring failed", message, variant: "error" });
    } finally {
      setScanning(false);
    }
  }, [token, parseResult, jdText, applyScorecard, resetScore, push]);

  const runProofRewrite = useCallback(async () => {
    if (!token || !lastScorecardId) return;
    setRewriting(true);
    setRewriteError(null);
    try {
      const res = await api.runRewrite(token, lastScorecardId);
      setRewriteBundle(res);
      setTab("rewrite");
      push({
        title: "Rewrite generated",
        message: `${res.section_rewrites.length} sections improved`,
        variant: "success",
      });
    } catch (err) {
      const message = toErrorMessage(err, "Rewrite failed");
      setRewriteError(message);
      push({ title: "Rewrite failed", message, variant: "error" });
    } finally {
      setRewriting(false);
    }
  }, [token, lastScorecardId, push]);

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
        if (res.results.length === 0) {
          push({ title: "No jobs found", message: "Try another role or location", variant: "info" });
        }
      } catch (err) {
        const message = toErrorMessage(err, "Job search failed");
        setJobsError(message);
        setJobs([]);
        push({ title: "Job search failed", message, variant: "error" });
      } finally {
        setJobsLoading(false);
      }
    },
    [token, push]
  );

  const runAgent = useCallback(
    async (payload: { job_id?: number; jd_text?: string; job_query?: string; location?: string }) => {
      if (!token || !parseResult?.resume_id) {
        const message = "Upload a resume first.";
        setAgentError(message);
        push({ title: "Agent run unavailable", message, variant: "error" });
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
        push({
          title: "Agent started",
          message: `Run #${res.run_id} is now ${res.status}`,
          variant: "info",
        });
      } catch (err) {
        const message = toErrorMessage(err, "Agent run failed");
        setAgentError(message);
        push({ title: "Agent run failed", message, variant: "error" });
      }
    },
    [token, parseResult, push]
  );

  const refreshAgentRun = useCallback(async () => {
    if (!token || !agentRun?.run_id) return;
    setAgentPolling(true);
    try {
      const latest = await api.getAgentRun(token, agentRun.run_id);
      setAgentRun(latest);
      if (latest.status === "completed") {
        push({
          title: "Agent run completed",
          message: `Run #${latest.run_id} finished successfully`,
          variant: "success",
        });
      }
    } catch (err) {
      const message = toErrorMessage(err, "Agent status refresh failed");
      setAgentError(message);
      push({ title: "Agent refresh failed", message, variant: "error" });
    } finally {
      setAgentPolling(false);
    }
  }, [token, agentRun?.run_id, push]);

  const replaceResume = useCallback(() => {
    setParseResult(null);
    resetScore();
    setTab("resume");
    push({ title: "Resume cleared", message: "Upload a new version to continue", variant: "info" });
  }, [resetScore, push]);

  const generateResume = useCallback(async () => {
    if (!token) return;
    setGenerating(true);
    setActionError(null);
    try {
      const res = await api.generateResume(token, { template_name: template });
      setResumePreview(res.content);
      push({ title: "Resume generated", variant: "success" });
    } catch (err) {
      const message = toErrorMessage(err, "Resume generation failed");
      setActionError(message);
      push({ title: "Generation failed", message, variant: "error" });
    } finally {
      setGenerating(false);
    }
  }, [token, template, push]);

  const queueExport = useCallback(async () => {
    if (!token || !parseResult?.resume_id) return;
    setActionError(null);
    try {
      const job = await api.exportResume(token, parseResult.resume_id);
      setExportJobId(job.job_id);
      setExportStatus(job.status);
      push({
        title: "Export queued",
        message: `Export job #${job.job_id} has started`,
        variant: "info",
      });
    } catch (err) {
      const message = toErrorMessage(err, "Export queue failed");
      setActionError(message);
      push({ title: "Export failed", message, variant: "error" });
    }
  }, [token, parseResult?.resume_id, push]);

  const refreshExportStatus = useCallback(async () => {
    if (!token || !exportJobId) return;
    try {
      const data = await api.exportStatus(token, exportJobId);
      setExportStatus(data.status);
      if (data.status === "completed" || data.status === "complete") {
        push({ title: "Export is ready", message: "Download your ATS-safe PDF now", variant: "success" });
        // Persist so dashboard checklist reflects the completed export
        const prev = safeReadPersistedState();
        if (prev) safeWritePersistedState({ ...prev, export_status: "done" });
      }
    } catch (err) {
      const message = toErrorMessage(err, "Could not refresh export status");
      setActionError(message);
      push({ title: "Export refresh failed", message, variant: "error" });
    }
  }, [token, exportJobId, push]);

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
      push({ title: "Download started", variant: "success" });
    } catch (err) {
      const message = toErrorMessage(err, "Export download failed");
      setActionError(message);
      push({ title: "Download failed", message, variant: "error" });
    }
  }, [token, exportJobId, push]);

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
    atsChecks,
    atsIssues,
    atsBucket,
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
