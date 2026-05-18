import type { Dispatch, SetStateAction } from "react";

export type ActivePane = "account" | "resume" | "nexus" | "jobs" | "billing";
export type StateSetter<T> = Dispatch<SetStateAction<T>>;

export type Scan = { composite: number; keyword: number; format: number; quality: number; complete: number; contact: number } | null;

export type Dashboard = {
  best_ats_score: number;
  total_resumes: number;
  scans_performed: number;
  jobs_matched_over_70: number;
  applications_tracked: number;
  profile_completeness: number;
};

export type Alert = { id: number; query: string; location: string; min_score: number; is_active: boolean };
export type JobMatch = { id: number; title: string; company: string; location: string; score: number };
export type Application = { id: number; company: string; role: string; status: string; notes: string; applied_on: string };
export type History = { id: number; composite_score: number; created_at: string };
export type Plan = { code: string; name: string; price_inr_month: number };
export type ResumeItem = { id: number; template_name: string; created_at: string };
export type Notification = { id: number; title: string; body: string; is_read: boolean; created_at: string };
export type NexusReq = { id: string; req_number: string; title: string; department: string; status: string; active_candidate_count: number };
export type NexusCandidate = { id: string; full_name: string; email: string; skills_csv: string };
export type NexusApp = { id: string; candidate_id: string; requisition_id: string; stage_name: string; status: string; match_score: number };
export type NexusEvent = { id: string; event_name: string; payload: string; created_at: string };

export type AuthState = { full_name: string; email: string; password: string };
export type ProfileState = {
  city: string;
  professional_status: string;
  target_role: string;
  skills_csv: string;
  summary: string;
  experience_bullet: string;
};
export type AlertFormState = { query: string; location: string; min_score: number };
export type AppFormState = { company: string; role: string; status: string; notes: string };
export type NexusReqFormState = { title: string; department: string; description_raw: string; required_skills_csv: string };
export type NexusCandidateFormState = { full_name: string; email: string; skills_csv: string };
