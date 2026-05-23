import type { ScorecardResult } from "./api";

export type ScoreComponentKey =
  | "jd_match"
  | "ats_safety"
  | "evidence"
  | "completeness"
  | "interview"
  | "hygiene";

export const SCORE_COMPONENTS: ReadonlyArray<{
  key: ScoreComponentKey;
  label: string;
  weight: string;
  color: string;
}> = [
  { key: "jd_match", label: "JD Match", weight: "35%", color: "#0071c5" },
  { key: "ats_safety", label: "ATS Parse Safety", weight: "20%", color: "#16a34a" },
  { key: "evidence", label: "Evidence Quality", weight: "20%", color: "#005d7f" },
  { key: "completeness", label: "Profile Completeness", weight: "10%", color: "#d97706" },
  { key: "interview", label: "Interview Readiness", weight: "10%", color: "#7c3aed" },
  { key: "hygiene", label: "Placement Hygiene", weight: "5%", color: "#414752" },
] as const;

const FLAG_ALIASES: Record<string, string> = {
  two_column_layout_detected: "two_column",
  "two-column_layout_detected": "two_column",
  table_based_skills_section: "table_detected",
  "table-based_skills_section": "table_detected",
};

export function normalizeAtsFlags(flags: string[]): string[] {
  return flags.map((raw) => {
    const key = raw
      .trim()
      .toLowerCase()
      .replace(/[^\w]+/g, "_")
      .replace(/^_+|_+$/g, "");
    return FLAG_ALIASES[key] ?? key;
  });
}

export function readinessBucket(score: number): { label: string; cls: string } {
  if (score >= 85) return { label: "Strong", cls: "bucket-strong" };
  if (score >= 70) return { label: "Ready", cls: "bucket-ready" };
  if (score >= 50) return { label: "Borderline", cls: "bucket-borderline" };
  return { label: "High Risk", cls: "bucket-risk" };
}

export function scorecardToBarScores(res: ScorecardResult): Record<ScoreComponentKey, number> {
  return {
    jd_match: res.raw.jd_match,
    ats_safety: res.raw.ats_parse_safety,
    evidence: res.raw.evidence_quality,
    completeness: res.raw.profile_completeness,
    interview: res.raw.interview_readiness,
    hygiene: res.raw.placement_hygiene,
  };
}

export const TEMPLATE_OPTIONS = [
  { value: "classic", label: "Classic ATS (Single Column)" },
  { value: "technical", label: "Technical / Developer" },
  { value: "fresher", label: "Fresher Graduate" },
] as const;

export type TemplateName = (typeof TEMPLATE_OPTIONS)[number]["value"];
