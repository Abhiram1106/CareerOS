import { Dashboard } from "./types";
import { CardSection, MetricTile } from "../ui/primitives";

type Props = {
  dashboard: Dashboard;
  refreshDashboard: () => Promise<void>;
};

// Placeholder — becomes Placement Officer JD/Cohort manager in Week 4.
export function JobsPane({ dashboard, refreshDashboard }: Props) {
  return (
    <div className="grid pane-grid">
      <CardSection
        title="Placement readiness — snapshot"
        subtitle="Officer cohort dashboard, batch upload, and JD manager land in Week 4."
        badge="Week 4"
        action={
          <button type="button" className="btn-ghost btn-compact" onClick={refreshDashboard}>
            Refresh
          </button>
        }
      >
        <div className="metric-grid">
          <MetricTile label="Best ATS"  value={dashboard.best_ats_score}       variant="intel" />
          <MetricTile label="Resumes"   value={dashboard.total_resumes} />
          <MetricTile label="Scans"     value={dashboard.scans_performed} />
          <MetricTile label="Profile %" value={dashboard.profile_completeness}  variant={dashboard.profile_completeness >= 75 ? "success" : "warn"} />
        </div>
      </CardSection>
    </div>
  );
}
