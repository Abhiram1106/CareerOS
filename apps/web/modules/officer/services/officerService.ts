import {
  api,
  type OfficerBatchListResult,
  type OfficerBatchUploadResult,
  type OfficerDashboardResult,
  type OfficerHeatmapResult,
  type OfficerReviewListResult,
  type OfficerSkillGapsResult,
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

export async function fetchOfficerHeatmap(token: string): Promise<OfficerHeatmapResult> {
  return api.officerHeatmap(token);
}

export async function fetchOfficerSkillGaps(token: string): Promise<OfficerSkillGapsResult> {
  return api.officerSkillGaps(token);
}

export async function createOfficerBatch(
  token: string,
  payload: { name: string; grad_year: number; dept_id?: number | null }
) {
  return api.officerCreateBatch(token, payload);
}

export async function uploadOfficerBatch(
  token: string,
  batchId: number,
  files: File[]
): Promise<OfficerBatchUploadResult> {
  return api.officerBatchUpload(token, batchId, files);
}

export async function downloadOfficerReadinessReport(token: string): Promise<Blob> {
  return api.downloadOfficerReadinessReport(token);
}
