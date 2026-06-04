export type AuthResponse = { token: string; email: string; full_name: string; role: string };

// ── Structured career profile section types ────────────────────────────────
export type WorkExperience = {
  id: number;
  company: string;
  title: string;
  employment_type: string;
  location: string;
  start_date: string;
  end_date: string;
  is_current: boolean;
  bullets: string[];
  sort_order: number;
};

export type Education = {
  id: number;
  institution: string;
  degree: string;
  field: string;
  start_year: number | null;
  end_year: number | null;
  cgpa: number | null;
  percentage: number | null;
  coursework: string;
  sort_order: number;
};

export type Skill = {
  id: number;
  name: string;
  category: "technical" | "soft" | "tool" | "language";
  proficiency: "beginner" | "intermediate" | "advanced" | "expert";
};

export type Project = {
  id: number;
  title: string;
  description: string;
  tech_stack: string[];
  github_url: string;
  live_url: string;
  start_date: string;
  end_date: string;
  sort_order: number;
};

export type Certification = {
  id: number;
  name: string;
  issuer: string;
  issue_date: string;
  expiry_date: string;
  credential_id: string;
  credential_url: string;
  sort_order: number;
};

export type JobApplication = {
  id: number;
  job_external_id: string;
  job_title: string;
  company: string;
  apply_url: string;
  status: "saved" | "applied" | "screening" | "interview" | "offer" | "rejected";
  resume_id: number | null;
  notes: string;
  applied_at: string | null;
  created_at: string;
};

export type FullProfile = {
  user: {
    id: number;
    full_name: string;
    email: string;
    phone: string;
    linkedin_url: string;
    github_url: string;
    portfolio_url: string;
  };
  work_experiences: WorkExperience[];
  educations: Education[];
  skills: Skill[];
  projects: Project[];
  certifications: Certification[];
};

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

export type ATSCheck = {
  key: string;
  label: string;
  score: number;
  weight: number;
  status: string;
};

export type ATSIssue = {
  id: string;
  dimension: string;
  severity: "high" | "medium" | "low";
  message: string;
  fix: string;
};

export type VendorScore = {
  id: string;
  name: string;
  score: number;
  weight_pct: number;
};

export type VendorSimulation = {
  composite_score: number;
  vendors: VendorScore[];
};

export type KeywordItem = { keyword: string; context: string; frequency?: number };
export type MissingKeyword = { keyword: string; importance: "high" | "medium" | "low"; frequency?: number };

export type KeywordGap = {
  matched: KeywordItem[];
  missing: MissingKeyword[];
  match_rate: number;
  total_jd_keywords: number;
};

export type GraphGapItem = {
  skill: string;
  distance: number | null;   // hop count from nearest known skill; null = unreachable
  nearest_known: string | null;
  reachable: boolean;
};

export type QualityClassInfo = {
  key: string;    // e.g. "impact_weak"
  label: string;  // e.g. "Impact Weak"
  guidance: string; // actionable fix text
};

export type ScorecardResult = {
  scorecard_id: number;
  jd_id: number;
  overall_score: number;
  bucket: string;
  quality_class?: QualityClassInfo;  // CARE-RAG Layer 2
  components: ScorecardComponents;
  raw: Record<string, number>;
  missing_required_skills: string[];
  matched_skills: string[];
  semantic_method?: string;
  ats_bucket?: string;
  ats_checks?: ATSCheck[];
  ats_issues?: ATSIssue[];
  vendor_simulation?: VendorSimulation;
  keyword_gap?: KeywordGap;
  graph_gap?: GraphGapItem[];  // CARE-RAG Layer 3D skill graph enrichment
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
  apply_url?: string;
};

export type JobsSearchResult = {
  source: string;
  total: number;
  page: number;
  page_size: number;
  results: JobSearchItem[];
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

export type AssistantSuggestedAction = { label: string; href: string };

export type AssistantChatResult = {
  answer: string;
  sources: string[];
  suggested_actions: AssistantSuggestedAction[];
  score_summary: string | null;
  provider: string;
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
  register: (payload: { email: string; password: string; full_name: string }) =>
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
      bucket: string;
      checks: ATSCheck[];
      issues: ATSIssue[];
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

  benchmarks: () => request<BenchmarkPanelResult>("/benchmarks", "GET"),

  assistantChat: (token: string, message: string) =>
    request<AssistantChatResult>("/assistant/chat", "POST", { message }, token),

  // CARE-RAG Layer 6: feedback loop
  recordRecommendationFeedback: (token: string, recId: number, accepted: boolean) =>
    request<{ ok: boolean; rec_id: number; accepted: boolean; signal: string }>(
      `/recommendations/feedback/${recId}`, "PUT", { accepted }, token
    ),

  // CARE-RAG vector knowledge base
  similarResumes: (token: string, roleFamily?: string, n?: number) =>
    request<{
      patterns: { text: string; similarity: number; overall_score: number; evidence_score: number; role_family: string }[];
      count: number;
      source: string;
    }>(`/analytics/similar-resumes?role_family=${encodeURIComponent(roleFamily ?? "")}&n=${n ?? 3}`, "GET", undefined, token),

  scoreHistory: (token: string) =>
    request<{
      history: { scorecard_id: number; version: number; overall_score: number; bucket: string; quality_class: string; date: string; timestamp: string }[];
      delta: number | null;
      total: number;
    }>("/analytics/score-history", "GET", undefined, token),

  requestPasswordReset: (email: string) =>
    request<{ ok: boolean; note: string }>("/auth/reset-request", "POST", { email }),

  confirmPasswordReset: (token: string, new_password: string) =>
    request<{ ok: boolean; detail: string }>("/auth/reset-confirm", "POST", { token, new_password }),

  // ── Structured profile sections ──────────────────────────────────────────
  getFullProfile: (token: string) =>
    request<FullProfile>("/profile/complete", "GET", undefined, token),

  updateLinks: (token: string, payload: { phone: string; linkedin_url: string; github_url: string; portfolio_url: string }) =>
    request<{ ok: boolean }>("/profile/links", "PUT", payload, token),

  // Work Experience
  listWorkExp: (token: string) =>
    request<{ work_experiences: WorkExperience[] }>("/profile/work-experience", "GET", undefined, token),
  addWorkExp: (token: string, payload: Omit<WorkExperience, "id" | "sort_order">) =>
    request<WorkExperience>("/profile/work-experience", "POST", payload, token),
  updateWorkExp: (token: string, id: number, payload: Partial<Omit<WorkExperience, "id" | "sort_order">>) =>
    request<WorkExperience>(`/profile/work-experience/${id}`, "PUT", payload, token),
  deleteWorkExp: (token: string, id: number) =>
    request<void>(`/profile/work-experience/${id}`, "DELETE", undefined, token),

  // Education
  listEducation: (token: string) =>
    request<{ educations: Education[] }>("/profile/education", "GET", undefined, token),
  addEducation: (token: string, payload: Omit<Education, "id" | "sort_order">) =>
    request<Education>("/profile/education", "POST", payload, token),
  updateEducation: (token: string, id: number, payload: Partial<Omit<Education, "id" | "sort_order">>) =>
    request<Education>(`/profile/education/${id}`, "PUT", payload, token),
  deleteEducation: (token: string, id: number) =>
    request<void>(`/profile/education/${id}`, "DELETE", undefined, token),

  // Skills
  listSkills: (token: string) =>
    request<{ skills: Skill[] }>("/profile/skills", "GET", undefined, token),
  addSkill: (token: string, payload: Omit<Skill, "id">) =>
    request<Skill>("/profile/skills", "POST", payload, token),
  bulkUpsertSkills: (token: string, skills: Omit<Skill, "id">[]) =>
    request<{ skills: Skill[] }>("/profile/skills/bulk", "POST", { skills }, token),
  deleteSkill: (token: string, id: number) =>
    request<void>(`/profile/skills/${id}`, "DELETE", undefined, token),

  // Projects
  listProjects: (token: string) =>
    request<{ projects: Project[] }>("/profile/projects", "GET", undefined, token),
  addProject: (token: string, payload: Omit<Project, "id" | "sort_order">) =>
    request<Project>("/profile/projects", "POST", payload, token),
  updateProject: (token: string, id: number, payload: Partial<Omit<Project, "id" | "sort_order">>) =>
    request<Project>(`/profile/projects/${id}`, "PUT", payload, token),
  deleteProject: (token: string, id: number) =>
    request<void>(`/profile/projects/${id}`, "DELETE", undefined, token),

  // Certifications
  listCertifications: (token: string) =>
    request<{ certifications: Certification[] }>("/profile/certifications", "GET", undefined, token),
  addCertification: (token: string, payload: Omit<Certification, "id" | "sort_order">) =>
    request<Certification>("/profile/certifications", "POST", payload, token),
  updateCertification: (token: string, id: number, payload: Partial<Omit<Certification, "id" | "sort_order">>) =>
    request<Certification>(`/profile/certifications/${id}`, "PUT", payload, token),
  deleteCertification: (token: string, id: number) =>
    request<void>(`/profile/certifications/${id}`, "DELETE", undefined, token),

  // Job Applications
  listApplications: (token: string) =>
    request<{ applications: JobApplication[] }>("/applications", "GET", undefined, token),
  saveApplication: (token: string, payload: { job_external_id: string; job_title: string; company: string; apply_url: string }) =>
    request<JobApplication>("/applications", "POST", payload, token),
  updateApplication: (token: string, id: number, payload: { status?: string; notes?: string; resume_id?: number }) =>
    request<JobApplication>(`/applications/${id}`, "PUT", payload, token),
  deleteApplication: (token: string, id: number) =>
    request<void>(`/applications/${id}`, "DELETE", undefined, token),
};
