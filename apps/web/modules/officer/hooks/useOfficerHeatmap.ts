"use client";

import { useCallback, useEffect, useState } from "react";

import { getStoredAuth } from "../../../lib/auth";
import { toErrorMessage } from "../../../lib/errors";
import { fetchOfficerHeatmap } from "../services/officerService";
import type { OfficerHeatmapRow } from "../../../lib/api";

export function useOfficerHeatmap() {
  const token = getStoredAuth()?.token ?? "";
  const [departments, setDepartments] = useState<OfficerHeatmapRow[]>([]);
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
      const res = await fetchOfficerHeatmap(token);
      setDepartments(res.departments);
    } catch (err) {
      setError(toErrorMessage(err, "Failed to load heatmap"));
      setDepartments([]);
    } finally {
      setLoading(false);
    }
  }, [token]);

  useEffect(() => {
    void reload();
  }, [reload]);

  return { departments, loading, error, reload };
}
