import { api, type ScorecardResult } from "../../../lib/api";

export type ScoreResumePayload = {
  resume_id: number;
  jd_text: string;
  jd_id?: number;
  company?: string;
  role?: string;
  ats_flags?: string[];
};

export async function scoreResumeAgainstJd(
  token: string,
  payload: ScoreResumePayload
): Promise<ScorecardResult> {
  return api.scoreResume(token, payload);
}
