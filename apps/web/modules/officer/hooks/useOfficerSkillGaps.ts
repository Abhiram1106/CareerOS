"use client";

import { useCallback, useEffect, useState } from "react";

import { getStoredAuth } from "../../../lib/auth";
import { toErrorMessage } from "../../../lib/errors";
import { fetchOfficerSkillGaps } from "../services/officerService";
import type { OfficerSkillGapItem } from "../../../lib/api";

export function useOfficerSkillGaps() {
  const token = getStoredAuth()?.token ?? "";
  const [items, setItems] = useState<OfficerSkillGapItem[]>([]);
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
      const res = await fetchOfficerSkillGaps(token);
      setItems(res.items);
    } catch (err) {
      setError(toErrorMessage(err, "Failed to load skill gaps"));
      setItems([]);
    } finally {
      setLoading(false);
    }
  }, [token]);

  useEffect(() => {
    void reload();
  }, [reload]);

  return { items, loading, error, reload };
}
