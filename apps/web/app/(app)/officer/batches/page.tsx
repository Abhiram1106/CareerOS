"use client";

import { OfficerBatchList } from "../../../../components/officer/OfficerBatchList";
import { OfficerPageShell } from "../../../../components/officer/OfficerPageShell";
import { OfficerStateMessage } from "../../../../components/officer/OfficerStateMessage";
import { useOfficerBatches } from "../../../../modules/officer/hooks/useOfficerBatches";

export default function OfficerBatchesPage() {
  const { batches, loading, error } = useOfficerBatches();

  return (
    <OfficerPageShell
      title="Batches"
      subtitle="Campus cohorts for bulk resume intake — upload workflow ships next in Phase 4."
    >
      <OfficerStateMessage loading={loading} error={error} />
      {!loading && !error && <OfficerBatchList batches={batches} />}
    </OfficerPageShell>
  );
}
