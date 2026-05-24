"use client";

import { useCallback, useEffect, useState } from "react";

import { getStoredAuth } from "../../../lib/auth";
import { toErrorMessage } from "../../../lib/errors";
import { fetchOfficerReview } from "../services/officerService";
import type { OfficerReviewItem } from "../types/officer.types";

export function useOfficerReview() {
  const token = getStoredAuth()?.token ?? "";
  const [items, setItems] = useState<OfficerReviewItem[]>([]);
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
      const res = await fetchOfficerReview(token);
      setItems(res.items);
    } catch (err) {
      setError(toErrorMessage(err, "Failed to load review queue"));
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
