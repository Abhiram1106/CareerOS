import { Application, AppFormState, Dashboard, StateSetter } from "../types";
import { CardSection, FormField, MetricTile } from "../../ui/primitives";

type Props = {
  dashboard: Dashboard;
  refreshDashboard: () => Promise<void>;
  appForm: AppFormState;
  setAppForm: StateSetter<AppFormState>;
  onCreateApplication: () => Promise<void>;
  refreshApplications: () => Promise<void>;
  applications: Application[];
  onDeleteApplication: (id: number) => Promise<void>;
};

export function DashboardApplicationsCard({
  dashboard,
  refreshDashboard,
  appForm,
  setAppForm,
  onCreateApplication,
  refreshApplications,
  applications,
  onDeleteApplication,
}: Props) {
  return (
    <CardSection title="Dashboard + Applications">
      <div className="row"><button onClick={refreshDashboard}>Refresh Dashboard</button></div>
      <div className="metric-grid" style={{ marginTop: 12 }}>
        <MetricTile label="Best ATS" value={dashboard.best_ats_score} />
        <MetricTile label="Resumes" value={dashboard.total_resumes} />
        <MetricTile label="Scans" value={dashboard.scans_performed} />
        <MetricTile label="Jobs 70%+" value={dashboard.jobs_matched_over_70} />
        <MetricTile label="Applications" value={dashboard.applications_tracked} />
        <MetricTile label="Profile %" value={dashboard.profile_completeness} />
      </div>

      <h3 style={{ marginTop: 16 }}>Add Application</h3>
      <FormField label="Company"><input value={appForm.company} onChange={(e) => setAppForm({ ...appForm, company: e.target.value })} /></FormField>
      <FormField label="Role"><input value={appForm.role} onChange={(e) => setAppForm({ ...appForm, role: e.target.value })} /></FormField>
      <FormField label="Status"><input value={appForm.status} onChange={(e) => setAppForm({ ...appForm, status: e.target.value })} /></FormField>
      <FormField label="Notes"><textarea rows={2} value={appForm.notes} onChange={(e) => setAppForm({ ...appForm, notes: e.target.value })} /></FormField>
      <div className="row"><button onClick={onCreateApplication}>Add</button><button onClick={refreshApplications}>Refresh Applications</button></div>
      {applications.map((a) => <p key={a.id} className="muted">{a.company} | {a.role} | {a.status} <button onClick={() => onDeleteApplication(a.id)}>Delete</button></p>)}
    </CardSection>
  );
}
