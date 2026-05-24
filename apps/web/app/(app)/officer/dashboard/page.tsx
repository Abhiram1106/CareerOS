"use client";

import { OfficerBucketSummary } from "../../../../components/officer/OfficerBucketSummary";
import { OfficerDeptHeatmap } from "../../../../components/officer/OfficerDeptHeatmap";
import { OfficerKpiGrid } from "../../../../components/officer/OfficerKpiGrid";
import { OfficerPageShell } from "../../../../components/officer/OfficerPageShell";
import { OfficerSkillGaps } from "../../../../components/officer/OfficerSkillGaps";
import { OfficerStateMessage } from "../../../../components/officer/OfficerStateMessage";
import { useOfficerDashboard } from "../../../../modules/officer/hooks/useOfficerDashboard";
import { useOfficerHeatmap } from "../../../../modules/officer/hooks/useOfficerHeatmap";
import { useOfficerSkillGaps } from "../../../../modules/officer/hooks/useOfficerSkillGaps";

export default function OfficerDashboardPage() {
  const { data, loading, error } = useOfficerDashboard();
  const heatmap = useOfficerHeatmap();
  const gaps = useOfficerSkillGaps();

  return (
    <OfficerPageShell
      title="Cohort Readiness"
      subtitle="Placement intelligence from live scorecards — department heatmap and skill gaps from cohort data."
    >
      <OfficerStateMessage loading={loading} error={error} />
      {!loading && !error && data && (
        <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
          <OfficerKpiGrid kpis={data.kpis} />
          <OfficerBucketSummary buckets={data.buckets} />
          <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr", gap: 20 }}>
            {heatmap.loading ? (
              <OfficerStateMessage loading />
            ) : heatmap.error ? (
              <OfficerStateMessage error={heatmap.error} />
            ) : (
              <OfficerDeptHeatmap departments={heatmap.departments} />
            )}
            {gaps.loading ? (
              <OfficerStateMessage loading />
            ) : gaps.error ? (
              <OfficerStateMessage error={gaps.error} />
            ) : (
              <OfficerSkillGaps items={gaps.items} />
            )}
          </div>
        </div>
      )}
    </OfficerPageShell>
  );
}
