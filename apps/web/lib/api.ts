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

  // ATS
  scan: (token: string, payload: { jd_text: string }) =>
    request("/ats/scan", "POST", payload, token),
  atsHistory: (token: string) =>
    request<{ scans: Array<{ id: number; composite_score: number; created_at: string }> }>(
      "/ats/scans",
      "GET",
      undefined,
      token
    ),

  // Dashboard
  dashboard: (token: string) => request("/dashboard", "GET", undefined, token),
};
