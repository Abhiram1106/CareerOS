"use client";

import { useCallback, useEffect, useState } from "react";

import { getStoredAuth } from "../../../lib/auth";
import { toErrorMessage } from "../../../lib/errors";
import { fetchOfficerDashboard } from "../services/officerService";
import type { OfficerDashboardResult } from "../types/officer.types";

export function useOfficerDashboard() {
  const token = getStoredAuth()?.token ?? "";
  const [data, setData] = useState<OfficerDashboardResult | null>(null);
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
      setData(await fetchOfficerDashboard(token));
    } catch (err) {
      setError(toErrorMessage(err, "Failed to load cohort dashboard"));
      setData(null);
    } finally {
      setLoading(false);
    }
  }, [token]);

  useEffect(() => {
    void reload();
  }, [reload]);

  return { data, loading, error, reload };
}
