export type AuthResponse = { token: string; email: string; full_name: string; role: string };

export type ResumeSection = {
  section_name: string;
  content_json: Record<string, unknown>;
  confidence: number;
};

export type ParseResult = {
  resume_id: number;
  source_format: string;
  sections: ResumeSection[];
  ats_flags: string[];
  parse_warnings: string[];
  char_count: number;
};

export type ScorecardComponents = {
  jd_match: number;
  ats_safety: number;
  evidence: number;
  completeness: number;
  interview: number;
  hygiene: number;
};

export type ScorecardResult = {
  scorecard_id: number;
  jd_id: number;
  overall_score: number;
  bucket: string;
  components: ScorecardComponents;
  raw: Record<string, number>;
  missing_required_skills: string[];
  matched_skills: string[];
  semantic_method?: string;
};

export type RewriteSection = {
  section: string;
  original: string;
  rewrite: string;
  evidence_ids: string[];
  confidence: number;
};

export type RewriteResult = {
  scorecard_id: number;
  top_issues: Array<{ type: string; message: string; severity: string }>;
  section_rewrites: RewriteSection[];
  unsupported_claims: Array<{ claim: string; reason: string }>;
  requires_confirmation: Array<{ field: string; suggested_change: string }>;
};

export type JobSearchItem = {
  id: number;
  source: string;
  external_id: string;
  title: string;
  company: string;
  location: string;
  skills_required: string[];
  raw_jd_text: string;
};

export type JobsSearchResult = {
  source: string;
  total: number;
  page: number;
  page_size: number;
  results: JobSearchItem[];
};

export type OfficerKpis = {
  students_scored: number;
  avg_readiness: number;
  parse_safe_rate: number;
  ready_count: number;
};

export type OfficerBuckets = {
  strong: number;
  ready: number;
  borderline: number;
  risk: number;
};

export type OfficerReviewItem = {
  student_name: string;
  target_role: string;
  overall_score: number;
  bucket: string;
  scorecard_id: number;
  resume_id: number;
};

export type OfficerDashboardResult = {
  kpis: OfficerKpis;
  buckets: OfficerBuckets;
};

export type OfficerReviewListResult = {
  items: OfficerReviewItem[];
};

export type OfficerBatchItem = {
  id: number;
  name: string;
  grad_year: number;
  college_id: number;
  dept_id: number | null;
  created_at: string;
};

export type OfficerBatchListResult = {
  batches: OfficerBatchItem[];
};

export type OfficerCohortResult = OfficerDashboardResult & {
  review_queue: OfficerReviewItem[];
};

export type BenchmarkWorkload = {
  id: string;
  name: string;
  tool: string;
  status: string;
  note: string;
  baseline_p50_ms: number | null;
  intel_p50_ms: number | null;
  baseline_p95_ms: number | null;
  intel_p95_ms: number | null;
  speedup: number | null;
  accuracy_delta_pct: number | null;
  throughput_baseline_rph: number | null;
  throughput_intel_rph: number | null;
  dataset: Record<string, unknown>;
};

export type BenchmarkPanelResult = {
  generated_at: string;
  hardware: { platform: string; processor: string; python: string };
  methodology: { baseline: string; intel_path: string; accuracy_guard: string };
  workloads: BenchmarkWorkload[];
};

export type AgentRunResult = {
  run_id: number;
  status: string;
  current_step: string;
  scorecard_id?: number | null;
  job_id?: number | null;
  export_job_id?: number | null;
  summary: Record<string, unknown>;
};

const API_BASE = process.env.NEXT_PUBLIC_CORE_API_URL || "http://localhost:8000";

async function request<T>(path: string, method = "GET", body?: unknown, token?: string): Promise<T> {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (token) headers.Authorization = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
    cache: "no-store",
  });

  if (!res.ok) {
    let msg = "Request failed";
    try {
      const err = await res.json();
      msg = err.detail || msg;
    } catch {
      // noop
    }
    throw new Error(msg);
  }
  return res.json();
}

async function uploadFile<T>(path: string, file: File, token: string): Promise<T> {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: form,
    cache: "no-store",
  });
  if (!res.ok) {
    let msg = "Upload failed";
    try {
      const err = await res.json();
      msg = err.detail || msg;
    } catch {
      // noop
    }
    throw new Error(msg);
  }
  return res.json();
}

export const api = {
  // Auth
  register: (payload: { email: string; password: string; full_name: string; role?: string }) =>
    request<AuthResponse>("/auth/register", "POST", payload),
  login: (payload: { email: string; password: string }) =>
    request<AuthResponse>("/auth/login", "POST", payload),

  // Profile
  getProfile: (token: string) => request("/profile", "GET", undefined, token),
  updateProfile: (token: string, payload: unknown) => request("/profile", "PUT", payload, token),

  // Resumes
  listResumes: (token: string) =>
    request<{ resumes: Array<{ id: number; template_name: string; created_at: string }> }>(
      "/resumes",
      "GET",
      undefined,
      token
    ),
  uploadResume: (token: string, file: File) =>
    uploadFile<ParseResult>("/resumes/upload", file, token),
  getResumeSections: (token: string, resumeId: number) =>
    request<{ resume_id: number; source_format: string; sections: ResumeSection[] }>(
      `/resumes/${resumeId}/sections`,
      "GET",
      undefined,
      token
    ),
  generateResume: (token: string, payload: { template_name: string }) =>
    request<{ resume_id: number; content: string }>("/resumes/generate", "POST", payload, token),
  exportResume: (token: string, resume_id: number) =>
    request<{ job_id: number; status: string }>("/resumes/export", "POST", { resume_id }, token),
  exportStatus: (token: string, job_id: number) =>
    request<{ job_id: number; status: string; has_file: boolean }>(
      `/resumes/export/${job_id}`,
      "GET",
      undefined,
      token
    ),
  downloadExport: async (token: string, job_id: number): Promise<Blob> => {
    const res = await fetch(`${API_BASE}/resumes/export/${job_id}/download`, {
      headers: { Authorization: `Bearer ${token}` },
      cache: "no-store",
    });
    if (!res.ok) {
      let msg = "Export download failed";
      try {
        const err = await res.json();
        msg = err.detail || msg;
      } catch {
        // noop
      }
      throw new Error(msg);
    }
    return res.blob();
  },

  // JD + placement scorecard (Week 2)
  parseJd: (token: string, payload: { jd_text: string; company?: string; role?: string }) =>
    request<{
      jd_id: number;
      company: string;
      role: string;
      required_skills: string[];
      optional_skills: string[];
      eligibility: Record<string, unknown>;
    }>("/jd/parse", "POST", payload, token),
  scoreResume: (
    token: string,
    payload: {
      resume_id: number;
      jd_text: string;
      jd_id?: number;
      company?: string;
      role?: string;
      ats_flags?: string[];
    }
  ) =>
    request<ScorecardResult>("/scorecards/score", "POST", payload, token),

  runRewrite: (token: string, scorecard_id: number) =>
    request<RewriteResult>("/recommendations/rewrite", "POST", { scorecard_id }, token),
  getRecommendations: (token: string, scorecard_id: number) =>
    request<RewriteResult>(`/recommendations/${scorecard_id}`, "GET", undefined, token),
  searchJobs: (token: string, q: string, loc = "", page = 1) =>
    request<JobsSearchResult>(
      `/jobs/search?q=${encodeURIComponent(q)}&loc=${encodeURIComponent(loc)}&page=${page}`,
      "GET",
      undefined,
      token
    ),
  runAgent: (
    token: string,
    payload: { resume_id: number; job_id?: number; jd_text?: string; job_query?: string; location?: string; ats_flags?: string[] }
  ) => request<AgentRunResult>("/agent/run", "POST", payload, token),
  getAgentRun: (token: string, runId: number) =>
    request<AgentRunResult>(`/agent/runs/${runId}`, "GET", undefined, token),

  // ATS parse-safety (flags from resume-parser; scoring formula in packages/scoring)
  atsParseSafety: (token: string, payload: { resume_id: number; ats_flags: string[] }) =>
    request<{
      scan_id: number;
      resume_id: number;
      ats_parse_safety: number;
      penalties: Record<string, number>;
      unknown_flags: string[];
    }>("/ats/parse-safety", "POST", payload, token),
  atsHistory: (token: string) =>
    request<{ scans: Array<{ id: number; ats_parse_safety: number; created_at: string }> }>(
      "/ats/scans",
      "GET",
      undefined,
      token
    ),

  // Dashboard
  dashboard: (token: string) => request("/dashboard", "GET", undefined, token),

  logout: (token: string) =>
    request<{ ok: boolean; revoked: boolean }>("/auth/logout", "POST", undefined, token),

  officerDashboard: (token: string) =>
    request<OfficerDashboardResult>("/officer/dashboard", "GET", undefined, token),

  officerReview: (token: string) =>
    request<OfficerReviewListResult>("/officer/review", "GET", undefined, token),

  officerBatches: (token: string) =>
    request<OfficerBatchListResult>("/officer/batches", "GET", undefined, token),

  officerCohort: (token: string) =>
    request<OfficerCohortResult>("/officer/cohort", "GET", undefined, token),

  benchmarks: () => request<BenchmarkPanelResult>("/benchmarks", "GET"),
};
