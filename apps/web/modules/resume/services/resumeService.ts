import { api, type ParseResult } from "../../../lib/api";

export async function uploadResume(token: string, file: File): Promise<ParseResult> {
  return api.uploadResume(token, file);
}

export async function downloadExport(token: string, jobId: number): Promise<Blob> {
  return api.downloadExport(token, jobId);
}
