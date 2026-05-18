import { Dashboard } from "./types";
import { CardSection, MetricTile } from "../ui/primitives";

type Props = {
  dashboard: Dashboard;
  refreshDashboard: () => Promise<void>;
};

// Placeholder pane — slated to become the Placement Officer JD/Cohort manager
// in Week 4. For now it surfaces the surviving readiness dashboard metrics.
export function JobsPane({ dashboard, refreshDashboard }: Props) {
  return (
    <div className="grid pane-grid">
      <CardSection title="Placement Readiness — Snapshot">
        <p className="muted">
          Officer-side cohort dashboard, batch upload, and JD manager land in Week 4.
          For now, this pane shows aggregate readiness metrics for the signed-in account.
        </p>
        <div className="row"><button onClick={refreshDashboard}>Refresh</button></div>
        <div className="metric-grid" style={{ marginTop: 12 }}>
          <MetricTile label="Best ATS" value={dashboard.best_ats_score} />
          <MetricTile label="Resumes" value={dashboard.total_resumes} />
          <MetricTile label="Scans" value={dashboard.scans_performed} />
          <MetricTile label="Profile %" value={dashboard.profile_completeness} />
        </div>
      </CardSection>
    </div>
  );
}
