import type { Dispatch, SetStateAction } from "react";

export type ActivePane = "account" | "resume" | "jobs";
export type StateSetter<T> = Dispatch<SetStateAction<T>>;

export type Scan = { composite: number; keyword: number; format: number; quality: number; complete: number; contact: number } | null;

export type Dashboard = {
  best_ats_score: number;
  total_resumes: number;
  scans_performed: number;
  profile_completeness: number;
};

export type History = { id: number; composite_score: number; created_at: string };
export type ResumeItem = { id: number; template_name: string; created_at: string };

export type AuthState = { full_name: string; email: string; password: string };
export type ProfileState = {
  city: string;
  professional_status: string;
  target_role: string;
  skills_csv: string;
  summary: string;
  experience_bullet: string;
};
