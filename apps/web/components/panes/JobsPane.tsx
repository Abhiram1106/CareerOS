import {
  Alert,
  AlertFormState,
  Application,
  AppFormState,
  Dashboard,
  JobMatch,
  Notification,
  StateSetter,
} from "./types";
import { JobAlertsCard } from "./sections/JobAlertsCard";
import { DashboardApplicationsCard } from "./sections/DashboardApplicationsCard";

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
  dashboard: Dashboard;
  refreshDashboard: () => Promise<void>;
  appForm: AppFormState;
  setAppForm: StateSetter<AppFormState>;
  onCreateApplication: () => Promise<void>;
  refreshApplications: () => Promise<void>;
  applications: Application[];
  onDeleteApplication: (id: number) => Promise<void>;
};

export function JobsPane({
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
    <div className="grid pane-grid">
      <JobAlertsCard
        jobs={jobs}
        refreshJobs={refreshJobs}
        alertForm={alertForm}
        setAlertForm={setAlertForm}
        onCreateAlert={onCreateAlert}
        refreshAlerts={refreshAlerts}
        onDispatchAlerts={onDispatchAlerts}
        refreshNotifications={refreshNotifications}
        alerts={alerts}
        onDeleteAlert={onDeleteAlert}
        notifications={notifications}
      />
      <DashboardApplicationsCard
        dashboard={dashboard}
        refreshDashboard={refreshDashboard}
        appForm={appForm}
        setAppForm={setAppForm}
        onCreateApplication={onCreateApplication}
        refreshApplications={refreshApplications}
        applications={applications}
        onDeleteApplication={onDeleteApplication}
      />
    </div>
  );
}
