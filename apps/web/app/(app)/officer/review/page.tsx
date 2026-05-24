"use client";

import { OfficerPageShell } from "../../../../components/officer/OfficerPageShell";
import { OfficerReviewTable } from "../../../../components/officer/OfficerReviewTable";
import { OfficerStateMessage } from "../../../../components/officer/OfficerStateMessage";
import { useOfficerReview } from "../../../../modules/officer/hooks/useOfficerReview";

export default function OfficerReviewPage() {
  const { items, loading, error } = useOfficerReview();

  return (
    <OfficerPageShell
      title="Review Queue"
      subtitle="Students sorted by readiness score — approve proof-linked rewrites before drives."
    >
      <OfficerStateMessage loading={loading} error={error} />
      {!loading && !error && <OfficerReviewTable items={items} />}
    </OfficerPageShell>
  );
}
