export type AuthResponse = { token: string; email: string; full_name: string };

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

export const api = {
  register: (payload: { email: string; password: string; full_name: string }) => request<AuthResponse>("/auth/register", "POST", payload),
  login: (payload: { email: string; password: string }) => request<AuthResponse>("/auth/login", "POST", payload),
  getProfile: (token: string) => request("/profile", "GET", undefined, token),
  updateProfile: (token: string, payload: unknown) => request("/profile", "PUT", payload, token),
  listResumes: (token: string) => request<{ resumes: Array<{ id: number; template_name: string; created_at: string }> }>("/resumes", "GET", undefined, token),
  generateResume: (token: string, payload: { template_name: string }) => request<{ resume_id: number; content: string }>("/resumes/generate", "POST", payload, token),
  exportResume: (token: string, resume_id: number) => request<{ job_id: number; status: string }>("/resumes/export", "POST", { resume_id }, token),
  exportStatus: (token: string, job_id: number) => request<{ job_id: number; status: string; has_file: boolean }>(`/resumes/export/${job_id}`, "GET", undefined, token),
  scan: (token: string, payload: { jd_text: string }) => request("/ats/scan", "POST", payload, token),
  jobs: (token: string) => request<{ jobs: Array<{ id: number; title: string; company: string; location: string; score: number }> }>("/jobs/matches", "GET", undefined, token),
  atsHistory: (token: string) => request<{ scans: Array<{ id: number; composite_score: number; created_at: string }> }>("/ats/scans", "GET", undefined, token),
  createAlert: (token: string, payload: { query: string; location: string; min_score: number }) => request("/jobs/alerts", "POST", payload, token),
  listAlerts: (token: string) => request<{ alerts: Array<{ id: number; query: string; location: string; min_score: number; is_active: boolean }> }>("/jobs/alerts", "GET", undefined, token),
  deleteAlert: (token: string, id: number) => request(`/jobs/alerts/${id}`, "DELETE", undefined, token),
  dispatchAlerts: (token: string) => request("/jobs/alerts/dispatch", "POST", {}, token),
  listNotifications: (token: string) => request<{ notifications: Array<{ id: number; title: string; body: string; is_read: boolean; created_at: string }> }>("/jobs/alerts/notifications", "GET", undefined, token),
  markNotificationRead: (token: string, id: number) => request(`/jobs/alerts/notifications/${id}/read`, "PUT", {}, token),
  createApplication: (token: string, payload: { company: string; role: string; status: string; notes: string }) => request("/applications", "POST", payload, token),
  listApplications: (token: string) => request<{ applications: Array<{ id: number; company: string; role: string; status: string; notes: string; applied_on: string }> }>("/applications", "GET", undefined, token),
  updateApplication: (token: string, id: number, payload: { status: string; notes: string }) => request(`/applications/${id}`, "PUT", payload, token),
  deleteApplication: (token: string, id: number) => request(`/applications/${id}`, "DELETE", undefined, token),
  billingPlans: () => request<{ plans: Array<{ code: string; name: string; price_inr_month: number }> }>("/billing/plans"),
  subscribe: (token: string, plan_code: string) => request("/billing/subscribe", "POST", { plan_code }, token),
  checkout: (token: string, payload: { provider: string; plan_code: string }) => request<{ transaction_id: number; checkout_url: string }>("/billing/checkout", "POST", payload, token),
  mySubscription: (token: string) => request<{ plan_code: string; status: string; renews_on?: string }>("/billing/me", "GET", undefined, token),
  dashboard: (token: string) => request("/dashboard", "GET", undefined, token),
  nexusCreateRequisition: (token: string, payload: { title: string; department?: string; description_raw?: string; required_skills_csv?: string }) =>
    request<{ id: string; req_number: string; status: string }>("/nexus-ats/requisitions", "POST", payload, token),
  nexusListRequisitions: (token: string) =>
    request<{ items: Array<{ id: string; req_number: string; title: string; department: string; status: string; active_candidate_count: number }> }>("/nexus-ats/requisitions", "GET", undefined, token),
  nexusCreateCandidate: (token: string, payload: { email: string; full_name: string; skills_csv?: string; headline?: string; location?: string }) =>
    request<{ id: string; email: string; full_name: string }>("/nexus-ats/candidates", "POST", payload, token),
  nexusListCandidates: (token: string) =>
    request<{ items: Array<{ id: string; full_name: string; email: string; skills_csv: string }> }>("/nexus-ats/candidates", "GET", undefined, token),
  nexusCreateApplication: (token: string, payload: { candidate_id: string; requisition_id: string; source_channel?: string }) =>
    request<{ id: string; match_score: number; stage: string }>("/nexus-ats/applications", "POST", payload, token),
  nexusListApplications: (token: string) =>
    request<{ items: Array<{ id: string; candidate_id: string; requisition_id: string; stage_name: string; status: string; match_score: number }> }>("/nexus-ats/applications", "GET", undefined, token),
  nexusMoveApplicationStage: (token: string, application_id: string, payload: { stage_id: string; stage_name: string; note?: string }) =>
    request<{ ok: boolean; stage_name: string }>(`/nexus-ats/applications/${application_id}/stage`, "POST", payload, token),
  nexusSetApplicationStatus: (token: string, application_id: string, payload: { status: "reject" | "withdraw" | "hire"; note?: string }) =>
    request<{ ok: boolean; status: string }>(`/nexus-ats/applications/${application_id}/status`, "PATCH", payload, token),
  nexusBulkApplications: (token: string) =>
    request<{ format: string; items: Array<{ application_id: string; candidate_id: string; requisition_id: string; stage_name: string; status: string; source_channel: string; match_score: number }> }>(
      "/nexus-ats/applications/bulk",
      "GET",
      undefined,
      token
    ),
  nexusReqAnalytics: (token: string, req_id: string) =>
    request<{ stage_conversion_rates: Record<string, number>; source_breakdown: Record<string, number>; ai_forecast: { predicted_days_to_fill: number; pipeline_health: string } }>(
      `/nexus-ats/requisitions/${req_id}/analytics`,
      "GET",
      undefined,
      token
    ),
  nexusAiMatch: (token: string, payload: { candidate_id: string; requisition_id: string }) =>
    request<{ score: number; top_strengths: string[]; gaps: string[] }>("/nexus-ats/ai/match", "POST", payload, token),
  nexusAiParseResume: (token: string, text: string) =>
    request<{ candidate_fields: Record<string, string>; skills: string[]; confidence_scores: Record<string, number> }>(
      "/nexus-ats/ai/parse-resume",
      "POST",
      { text },
      token
    ),
  nexusAiPredictTimeToFill: (token: string, requisition_id: string) =>
    request<{ p50_days: number; p90_days: number; confidence: number; key_factors: string[] }>(
      "/nexus-ats/ai/predict/time-to-fill",
      "POST",
      { requisition_id },
      token
    ),
  nexusCandidateSearch: (token: string, payload: { query?: string; skill_ids?: string[]; include_internal?: boolean }) =>
    request<{ items: Array<{ id: string; full_name: string; email: string; skills_csv: string; search_score: number }> }>(
      "/nexus-ats/candidates/search",
      "POST",
      payload,
      token
    ),
  nexusCreateInterview: (token: string, payload: { application_id: string; interview_type?: string; scheduled_at?: string; timezone?: string; panel_csv?: string }) =>
    request<{ id: string; status: string }>("/nexus-ats/interviews", "POST", payload, token),
  nexusConfirmInterview: (token: string, interview_id: string) =>
    request<{ ok: boolean; status: string }>(`/nexus-ats/interviews/${interview_id}/confirm`, "POST", {}, token),
  nexusCreateScorecard: (token: string, payload: { interview_id: string; application_id: string; reviewer_id?: string; competency_scores?: string; recommendation?: string; comments?: string }) =>
    request<{ id: string; recommendation: string }>("/nexus-ats/scorecards", "POST", payload, token),
  nexusCreateOffer: (token: string, payload: { application_id: string; base_salary: number; currency?: string }) =>
    request<{ id: string; status: string }>("/nexus-ats/offers", "POST", payload, token),
  nexusSendOffer: (token: string, offer_id: string) =>
    request<{ ok: boolean; status: string }>(`/nexus-ats/offers/${offer_id}/send`, "POST", {}, token),
  nexusRespondOffer: (token: string, offer_id: string, action: "accepted" | "declined") =>
    request<{ ok: boolean; status: string }>(`/nexus-ats/offers/${offer_id}/respond`, "POST", { action }, token),
  nexusWebhookEvents: (token: string) =>
    request<{ items: Array<{ id: string; event_name: string; payload: string; created_at: string }> }>("/nexus-ats/webhooks/events", "GET", undefined, token),
};
