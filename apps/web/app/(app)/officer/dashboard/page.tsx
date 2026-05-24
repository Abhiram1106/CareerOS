"use client";

import { OfficerBucketSummary } from "../../../../components/officer/OfficerBucketSummary";
import { OfficerDeptHeatmapPlaceholder } from "../../../../components/officer/OfficerDeptHeatmapPlaceholder";
import { OfficerKpiGrid } from "../../../../components/officer/OfficerKpiGrid";
import { OfficerPageShell } from "../../../../components/officer/OfficerPageShell";
import { OfficerSkillGapsPlaceholder } from "../../../../components/officer/OfficerSkillGapsPlaceholder";
import { OfficerStateMessage } from "../../../../components/officer/OfficerStateMessage";
import { useOfficerDashboard } from "../../../../modules/officer/hooks/useOfficerDashboard";

export default function OfficerDashboardPage() {
  const { data, loading, error } = useOfficerDashboard();

  return (
    <OfficerPageShell
      title="Cohort Readiness"
      subtitle="Placement intelligence from live scorecards — department heatmap follows college scoping."
    >
      <OfficerStateMessage loading={loading} error={error} />
      {!loading && !error && data && (
        <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
          <OfficerKpiGrid kpis={data.kpis} />
          <OfficerBucketSummary buckets={data.buckets} />
          <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr", gap: 20 }}>
            <OfficerDeptHeatmapPlaceholder />
            <OfficerSkillGapsPlaceholder />
          </div>
        </div>
      )}
    </OfficerPageShell>
  );
}
