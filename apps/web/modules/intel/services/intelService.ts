import { api, type BenchmarkPanelResult } from "../../../lib/api";

export async function fetchBenchmarkPanel(): Promise<BenchmarkPanelResult> {
  return api.benchmarks();
}
