"use client";

import { useCallback, useEffect, useState } from "react";

import { getStoredAuth } from "../../../lib/auth";
import { toErrorMessage } from "../../../lib/errors";
import { fetchOfficerBatches } from "../services/officerService";
import type { OfficerBatchItem } from "../types/officer.types";

export function useOfficerBatches() {
  const token = getStoredAuth()?.token ?? "";
  const [batches, setBatches] = useState<OfficerBatchItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const reload = useCallback(async () => {
    if (!token) {
      setError("Sign in as a placement officer.");
      setLoading(false);
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const res = await fetchOfficerBatches(token);
      setBatches(res.batches);
    } catch (err) {
      setError(toErrorMessage(err, "Failed to load batches"));
      setBatches([]);
    } finally {
      setLoading(false);
    }
  }, [token]);

  useEffect(() => {
    void reload();
  }, [reload]);

  return { batches, loading, error, reload };
}
