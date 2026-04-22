import { Alert, AlertFormState, JobMatch, Notification, StateSetter } from "../types";
import { CardSection, FormField } from "../../ui/primitives";

type Props = {
  jobs: JobMatch[];
  refreshJobs: () => Promise<void>;
  alertForm: AlertFormState;
  setAlertForm: StateSetter<AlertFormState>;
  onCreateAlert: () => Promise<void>;
  refreshAlerts: () => Promise<void>;
  onDispatchAlerts: () => Promise<void>;
  refreshNotifications: () => Promise<void>;
  alerts: Alert[];
  onDeleteAlert: (id: number) => Promise<void>;
  notifications: Notification[];
};

export function JobAlertsCard({
  jobs,
  refreshJobs,
  alertForm,
  setAlertForm,
  onCreateAlert,
  refreshAlerts,
  onDispatchAlerts,
  refreshNotifications,
  alerts,
  onDeleteAlert,
  notifications,
}: Props) {
  return (
    <CardSection title="Job Matches">
      <div className="row"><button onClick={refreshJobs}>Refresh Jobs</button></div>
      <div style={{ marginTop: 10 }}>
        {jobs.map((job) => (
          <div key={job.id} className="job">
            <strong>{job.title}</strong>
            <p className="muted">{job.company} | {job.location} | {job.score}% match</p>
          </div>
        ))}
      </div>
      <h3>Create Alert</h3>
      <FormField label="Query"><input value={alertForm.query} onChange={(e) => setAlertForm({ ...alertForm, query: e.target.value })} /></FormField>
      <FormField label="Location"><input value={alertForm.location} onChange={(e) => setAlertForm({ ...alertForm, location: e.target.value })} /></FormField>
      <FormField label="Min Score"><input type="number" value={alertForm.min_score} onChange={(e) => setAlertForm({ ...alertForm, min_score: Number(e.target.value) })} /></FormField>
      <div className="row"><button onClick={onCreateAlert}>Create Alert</button><button onClick={refreshAlerts}>Refresh Alerts</button></div>
      <div className="row tight"><button onClick={onDispatchAlerts}>Run Alert Dispatch</button><button onClick={refreshNotifications}>Refresh Notifications</button></div>
      {alerts.map((a) => <p key={a.id} className="muted">#{a.id} {a.query} @ {a.location || "any"} (min {a.min_score}) <button onClick={() => onDeleteAlert(a.id)}>Delete</button></p>)}
      <h3>Notifications</h3>
      {notifications.map((n) => <p key={n.id} className="muted">{n.title} | {n.body}</p>)}
    </CardSection>
  );
}
