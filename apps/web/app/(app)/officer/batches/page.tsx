"use client";

import { OfficerBatchList } from "../../../../components/officer/OfficerBatchList";
import { OfficerBatchUpload } from "../../../../components/officer/OfficerBatchUpload";
import { OfficerPageShell } from "../../../../components/officer/OfficerPageShell";
import { OfficerStateMessage } from "../../../../components/officer/OfficerStateMessage";
import { useOfficerBatches } from "../../../../modules/officer/hooks/useOfficerBatches";

export default function OfficerBatchesPage() {
  const { batches, loading, error, reload } = useOfficerBatches();

  return (
    <OfficerPageShell
      title="Batches"
      subtitle="Create campus cohorts and bulk-upload resumes for placement intake."
    >
      <OfficerStateMessage loading={loading} error={error} />
      {!loading && !error && (
        <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
          <OfficerBatchUpload onComplete={() => void reload()} />
          <OfficerBatchList batches={batches} />
        </div>
      )}
    </OfficerPageShell>
  );
}
