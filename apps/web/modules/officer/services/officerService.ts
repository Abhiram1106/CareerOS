import {
  api,
  type OfficerBatchListResult,
  type OfficerDashboardResult,
  type OfficerReviewListResult,
} from "../../../lib/api";

export async function fetchOfficerDashboard(token: string): Promise<OfficerDashboardResult> {
  return api.officerDashboard(token);
}

export async function fetchOfficerReview(token: string): Promise<OfficerReviewListResult> {
  return api.officerReview(token);
}

export async function fetchOfficerBatches(token: string): Promise<OfficerBatchListResult> {
  return api.officerBatches(token);
}
