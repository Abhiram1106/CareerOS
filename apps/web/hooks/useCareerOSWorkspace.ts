"use client";

import { useEffect, useMemo, useState } from "react";
import { api } from "../lib/api";
import {
  Alert,
  AlertFormState,
  Application,
  AppFormState,
  AuthState,
  Dashboard,
  History,
  JobMatch,
  NexusApp,
  NexusCandidate,
  NexusCandidateFormState,
  NexusEvent,
  NexusReq,
  NexusReqFormState,
  Notification,
  Plan,
  ProfileState,
  ResumeItem,
  Scan,
} from "../components/panes/types";

const emptyDashboard: Dashboard = {
  best_ats_score: 0,
  total_resumes: 0,
  scans_performed: 0,
  jobs_matched_over_70: 0,
  applications_tracked: 0,
  profile_completeness: 0,
};

function errMsg(error: unknown, fallback: string) {
  if (error instanceof Error && error.message) return error.message;
  return fallback;
}

export function useCareerOSWorkspace() {
  const [status, setStatus] = useState("Ready");
  const [token, setToken] = useState<string>("");

  const [auth, setAuth] = useState<AuthState>({ full_name: "", email: "", password: "" });
  const [profile, setProfile] = useState<ProfileState>({ city: "", professional_status: "Fresher", target_role: "Software Engineer", skills_csv: "", summary: "", experience_bullet: "" });

  const [template, setTemplate] = useState("classic");
  const [resumeText, setResumeText] = useState("");
  const [jdText, setJdText] = useState("");
  const [scan, setScan] = useState<Scan>(null);
  const [jobs, setJobs] = useState<JobMatch[]>([]);
  const [dashboard, setDashboard] = useState<Dashboard>(emptyDashboard);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [applications, setApplications] = useState<Application[]>([]);
  const [history, setHistory] = useState<History[]>([]);
  const [plans, setPlans] = useState<Plan[]>([]);
  const [myPlan, setMyPlan] = useState("free");
  const [resumes, setResumes] = useState<ResumeItem[]>([]);
  const [exportJobId, setExportJobId] = useState<number | null>(null);
  const [exportStatus, setExportStatus] = useState<string>("");
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [nexusReqs, setNexusReqs] = useState<NexusReq[]>([]);
  const [nexusCandidates, setNexusCandidates] = useState<NexusCandidate[]>([]);
  const [nexusApps, setNexusApps] = useState<NexusApp[]>([]);
  const [nexusMatchResult, setNexusMatchResult] = useState<{ score: number; top_strengths: string[]; gaps: string[] } | null>(null);
  const [nexusEvents, setNexusEvents] = useState<NexusEvent[]>([]);
  const [latestInterviewId, setLatestInterviewId] = useState<string>("");
  const [latestOfferId, setLatestOfferId] = useState<string>("");

  const [alertForm, setAlertForm] = useState<AlertFormState>({ query: "Software Engineer", location: "", min_score: 70 });
  const [appForm, setAppForm] = useState<AppFormState>({ company: "", role: "", status: "applied", notes: "" });
  const [nexusReqForm, setNexusReqForm] = useState<NexusReqFormState>({ title: "Backend Engineer", department: "Engineering", description_raw: "", required_skills_csv: "python,fastapi,sql,docker" });
  const [nexusCandidateForm, setNexusCandidateForm] = useState<NexusCandidateFormState>({ full_name: "", email: "", skills_csv: "" });

  useEffect(() => {
    const saved = window.localStorage.getItem("careeros_token");
    if (saved) setToken(saved);
  }, []);

  useEffect(() => {
    if (!token) return;
    hydrate(token);
  }, [token]);

  useEffect(() => {
    api.billingPlans().then((r) => setPlans(r.plans)).catch(() => {});
  }, []);

  const preview = useMemo(() => {
    return `${auth.full_name || "Your Name"}\n${profile.target_role}\n\nSummary\n${profile.summary || "..."}\n\nExperience\n- ${profile.experience_bullet || "..."}\n\nSkills\n${profile.skills_csv || "..."}`;
  }, [auth.full_name, profile]);

  async function hydrate(authToken: string) {
    try {
      const p = (await api.getProfile(authToken)) as ProfileState & { full_name: string; email: string };
      setAuth((old) => ({ ...old, full_name: p.full_name, email: p.email }));
      setProfile({
        city: p.city || "",
        professional_status: p.professional_status || "Fresher",
        target_role: p.target_role || "Software Engineer",
        skills_csv: p.skills_csv || "",
        summary: p.summary || "",
        experience_bullet: p.experience_bullet || "",
      });
      await Promise.all([
        refreshJobs(authToken),
        refreshDashboard(authToken),
        refreshAlerts(authToken),
        refreshApplications(authToken),
        refreshHistory(authToken),
        refreshNotifications(authToken),
        refreshNexusReqs(authToken),
        refreshNexusCandidates(authToken),
        refreshNexusApps(authToken),
        refreshNexusEvents(authToken),
      ]);
      await refreshResumes(authToken);
      const sub = await api.mySubscription(authToken);
      setMyPlan(sub.plan_code);
      setStatus("Session restored");
    } catch {
      setStatus("Please login again");
      setToken("");
      window.localStorage.removeItem("careeros_token");
    }
  }

  async function onRegister() {
    try {
      const res = await api.register({ email: auth.email, password: auth.password, full_name: auth.full_name });
      window.localStorage.setItem("careeros_token", res.token);
      setToken(res.token);
      setStatus("Registered and signed in");
    } catch (e) {
      setStatus(errMsg(e, "Registration failed"));
    }
  }

  async function onLogin() {
    try {
      const res = await api.login({ email: auth.email, password: auth.password });
      window.localStorage.setItem("careeros_token", res.token);
      setToken(res.token);
      setStatus("Logged in");
    } catch (e) {
      setStatus(errMsg(e, "Login failed"));
    }
  }

  async function onSaveProfile() {
    if (!token) return setStatus("Login required");
    try {
      await api.updateProfile(token, profile);
      setStatus("Profile saved");
      await refreshDashboard(token);
    } catch (e) {
      setStatus(errMsg(e, "Profile save failed"));
    }
  }

  async function onGenerateResume() {
    if (!token) return setStatus("Login required");
    try {
      await api.updateProfile(token, profile);
      const res = await api.generateResume(token, { template_name: template });
      setResumeText(res.content);
      setStatus(`Resume #${res.resume_id} generated`);
      await refreshResumes(token);
      await refreshDashboard(token);
    } catch (e) {
      setStatus(errMsg(e, "Resume generation failed"));
    }
  }

  async function onScan() {
    if (!token) return setStatus("Login required");
    try {
      await api.updateProfile(token, profile);
      const res = (await api.scan(token, { jd_text: jdText })) as Scan;
      setScan(res);
      setStatus("ATS scan completed");
      await Promise.all([refreshDashboard(token), refreshHistory(token)]);
    } catch (e) {
      setStatus(errMsg(e, "ATS scan failed"));
    }
  }

  async function onCreateAlert() {
    if (!token) return setStatus("Login required");
    try {
      await api.createAlert(token, alertForm);
      setStatus("Alert created");
      await refreshAlerts(token);
    } catch (e) {
      setStatus(errMsg(e, "Alert creation failed"));
    }
  }

  async function onDeleteAlert(id: number) {
    if (!token) return;
    await api.deleteAlert(token, id);
    await refreshAlerts(token);
  }

  async function onDispatchAlerts() {
    if (!token) return;
    await api.dispatchAlerts(token);
    await refreshNotifications(token);
    setStatus("Alert dispatch triggered");
  }

  async function onCreateApplication() {
    if (!token) return setStatus("Login required");
    try {
      await api.createApplication(token, appForm);
      setStatus("Application added");
      await Promise.all([refreshApplications(token), refreshDashboard(token)]);
    } catch (e) {
      setStatus(errMsg(e, "Application create failed"));
    }
  }

  async function onDeleteApplication(id: number) {
    if (!token) return;
    await api.deleteApplication(token, id);
    await Promise.all([refreshApplications(token), refreshDashboard(token)]);
  }

  async function refreshJobs(authToken = token) {
    if (!authToken) return;
    const res = await api.jobs(authToken);
    setJobs(res.jobs);
  }

  async function refreshDashboard(authToken = token) {
    if (!authToken) return;
    const d = (await api.dashboard(authToken)) as Dashboard;
    setDashboard(d);
  }

  async function refreshAlerts(authToken = token) {
    if (!authToken) return;
    const data = await api.listAlerts(authToken);
    setAlerts(data.alerts);
  }

  async function refreshNotifications(authToken = token) {
    if (!authToken) return;
    const data = await api.listNotifications(authToken);
    setNotifications(data.notifications);
  }

  async function refreshApplications(authToken = token) {
    if (!authToken) return;
    const data = await api.listApplications(authToken);
    setApplications(data.applications);
  }

  async function refreshHistory(authToken = token) {
    if (!authToken) return;
    const data = await api.atsHistory(authToken);
    setHistory(data.scans);
  }

  async function refreshResumes(authToken = token) {
    if (!authToken) return;
    const data = await api.listResumes(authToken);
    setResumes(data.resumes);
  }

  async function refreshNexusReqs(authToken = token) {
    if (!authToken) return;
    const data = await api.nexusListRequisitions(authToken);
    setNexusReqs(data.items);
  }

  async function refreshNexusCandidates(authToken = token) {
    if (!authToken) return;
    const data = await api.nexusListCandidates(authToken);
    setNexusCandidates(data.items);
  }

  async function refreshNexusApps(authToken = token) {
    if (!authToken) return;
    const data = await api.nexusListApplications(authToken);
    setNexusApps(data.items);
  }

  async function refreshNexusEvents(authToken = token) {
    if (!authToken) return;
    const data = await api.nexusWebhookEvents(authToken);
    setNexusEvents(data.items);
  }

  async function onCreateNexusReq() {
    if (!token) return setStatus("Login required");
    try {
      await api.nexusCreateRequisition(token, nexusReqForm);
      setStatus("NEXUS requisition created");
      await refreshNexusReqs(token);
    } catch (e) {
      setStatus(errMsg(e, "NEXUS requisition create failed"));
    }
  }

  async function onCreateNexusCandidate() {
    if (!token) return setStatus("Login required");
    try {
      await api.nexusCreateCandidate(token, nexusCandidateForm);
      setStatus("NEXUS candidate upserted");
      await refreshNexusCandidates(token);
    } catch (e) {
      setStatus(errMsg(e, "NEXUS candidate upsert failed"));
    }
  }

  async function onCreateNexusApplication() {
    if (!token) return setStatus("Login required");
    if (!nexusCandidates.length || !nexusReqs.length) return setStatus("Create at least one requisition and candidate first");
    try {
      await api.nexusCreateApplication(token, {
        candidate_id: nexusCandidates[0].id,
        requisition_id: nexusReqs[0].id,
        source_channel: "webapp",
      });
      setStatus("NEXUS application created");
      await refreshNexusApps(token);
    } catch (e) {
      setStatus(errMsg(e, "NEXUS application create failed"));
    }
  }

  async function onMoveNexusAppStage(appId: string) {
    if (!token) return;
    await api.nexusMoveApplicationStage(token, appId, {
      stage_id: "interview",
      stage_name: "Interview",
      note: "Advanced from webapp",
    });
    await refreshNexusApps(token);
  }

  async function onRunNexusAiMatch() {
    if (!token) return;
    if (!nexusCandidates.length || !nexusReqs.length) return setStatus("Create requisition and candidate first");
    try {
      const data = await api.nexusAiMatch(token, { candidate_id: nexusCandidates[0].id, requisition_id: nexusReqs[0].id });
      setNexusMatchResult(data);
      setStatus("NEXUS AI match computed");
    } catch (e) {
      setStatus(errMsg(e, "NEXUS AI match failed"));
    }
  }

  async function onCreateNexusInterview() {
    if (!token) return;
    if (!nexusApps.length) return setStatus("Create application first");
    const data = await api.nexusCreateInterview(token, {
      application_id: nexusApps[0].id,
      interview_type: "live",
      timezone: "Asia/Kolkata",
      panel_csv: auth.full_name,
    });
    setLatestInterviewId(data.id);
    setStatus("NEXUS interview scheduled");
    await refreshNexusEvents(token);
  }

  async function onSubmitNexusScorecard() {
    if (!token) return;
    if (!latestInterviewId || !nexusApps.length) return setStatus("Create interview first");
    await api.nexusCreateScorecard(token, {
      interview_id: latestInterviewId,
      application_id: nexusApps[0].id,
      competency_scores: JSON.stringify({ technical: 4, communication: 4, problem_solving: 5 }),
      recommendation: "advance",
      comments: "Strong fit from structured interview.",
    });
    setStatus("NEXUS scorecard submitted");
    await refreshNexusEvents(token);
  }

  async function onCreateNexusOffer() {
    if (!token) return;
    if (!nexusApps.length) return setStatus("Create application first");
    const data = await api.nexusCreateOffer(token, { application_id: nexusApps[0].id, base_salary: 2400000, currency: "INR" });
    setLatestOfferId(data.id);
    setStatus("NEXUS offer created");
    await refreshNexusEvents(token);
  }

  async function onSendNexusOffer() {
    if (!token || !latestOfferId) return setStatus("Create offer first");
    await api.nexusSendOffer(token, latestOfferId);
    setStatus("NEXUS offer sent");
    await refreshNexusEvents(token);
  }

  async function onExportResume() {
    if (!token) return setStatus("Login required");
    if (!resumes.length) return setStatus("Generate a resume first");
    const latest = resumes[0];
    const job = await api.exportResume(token, latest.id);
    setExportJobId(job.job_id);
    setExportStatus(job.status);
    setStatus(`Export job queued #${job.job_id}`);
  }

  async function checkExport() {
    if (!token || !exportJobId) return;
    const data = await api.exportStatus(token, exportJobId);
    setExportStatus(data.status);
  }

  async function downloadExport() {
    if (!token || !exportJobId) return;
    const base = process.env.NEXT_PUBLIC_CORE_API_URL || "http://localhost:8000";
    const res = await fetch(`${base}/resumes/export/${exportJobId}/download`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) {
      setStatus("Export download failed");
      return;
    }
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `resume_export_${exportJobId}.pdf`;
    a.click();
    window.URL.revokeObjectURL(url);
  }

  async function onSubscribe(planCode: string) {
    if (!token) return setStatus("Login required");
    try {
      await api.subscribe(token, planCode);
      setMyPlan(planCode);
      setStatus(`Subscribed to ${planCode}`);
    } catch (e) {
      setStatus(errMsg(e, "Subscription failed"));
    }
  }

  async function onCheckout(planCode: string, provider: string) {
    if (!token) return setStatus("Login required");
    try {
      const data = await api.checkout(token, { provider, plan_code: planCode });
      window.open(data.checkout_url, "_blank");
      setStatus(`Checkout initiated via ${provider}`);
    } catch (e) {
      setStatus(errMsg(e, "Checkout failed"));
    }
  }

  return {
    status,
    auth,
    setAuth,
    profile,
    setProfile,
    template,
    setTemplate,
    preview,
    resumeText,
    jdText,
    setJdText,
    scan,
    jobs,
    dashboard,
    alerts,
    applications,
    history,
    plans,
    myPlan,
    exportJobId,
    exportStatus,
    notifications,
    nexusReqs,
    nexusCandidates,
    nexusApps,
    nexusMatchResult,
    nexusEvents,
    latestInterviewId,
    latestOfferId,
    alertForm,
    setAlertForm,
    appForm,
    setAppForm,
    nexusReqForm,
    setNexusReqForm,
    nexusCandidateForm,
    setNexusCandidateForm,
    onRegister,
    onLogin,
    onSaveProfile,
    onGenerateResume,
    onScan,
    onCreateAlert,
    onDeleteAlert,
    onDispatchAlerts,
    onCreateApplication,
    onDeleteApplication,
    refreshJobs,
    refreshDashboard,
    refreshAlerts,
    refreshNotifications,
    refreshApplications,
    onCreateNexusReq,
    refreshNexusReqs,
    onCreateNexusCandidate,
    refreshNexusCandidates,
    onCreateNexusApplication,
    refreshNexusApps,
    onMoveNexusAppStage,
    onRunNexusAiMatch,
    onCreateNexusInterview,
    onSubmitNexusScorecard,
    onCreateNexusOffer,
    onSendNexusOffer,
    refreshNexusEvents,
    onExportResume,
    checkExport,
    downloadExport,
    onSubscribe,
    onCheckout,
  };
}
