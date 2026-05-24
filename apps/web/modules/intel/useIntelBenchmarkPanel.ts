"use client";

import { useCallback, useEffect, useState } from "react";

import { toErrorMessage } from "../../lib/errors";
import { fetchBenchmarkPanel } from "./intelService";
import type { BenchmarkPanelResult } from "./types";

export function useIntelBenchmarkPanel() {
  const [data, setData] = useState<BenchmarkPanelResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const reload = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      setData(await fetchBenchmarkPanel());
    } catch (err) {
      setError(toErrorMessage(err, "Failed to load benchmark panel"));
      setData(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void reload();
  }, [reload]);

  return { data, loading, error, reload };
}
