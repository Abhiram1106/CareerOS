"use client";

import { useEffect, useMemo, useState } from "react";
import { api } from "../lib/api";
import {
  AuthState,
  Dashboard,
  History,
  ParseResult,
  ProfileState,
  ResumeItem,
  Scan,
} from "../components/panes/types";

const emptyDashboard: Dashboard = {
  best_ats_score: 0,
  total_resumes: 0,
  scans_performed: 0,
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
  const [profile, setProfile] = useState<ProfileState>({
    city: "",
    professional_status: "Fresher",
    target_role: "Software Engineer",
    skills_csv: "",
    summary: "",
    experience_bullet: "",
  });

  const [template, setTemplate] = useState("classic");
  const [resumeText, setResumeText] = useState("");
  const [jdText, setJdText] = useState("");
  const [scan, setScan] = useState<Scan>(null);
  const [dashboard, setDashboard] = useState<Dashboard>(emptyDashboard);
  const [history, setHistory] = useState<History[]>([]);
  const [resumes, setResumes] = useState<ResumeItem[]>([]);
  const [exportJobId, setExportJobId] = useState<number | null>(null);
  const [exportStatus, setExportStatus] = useState<string>("");
  const [parseResult, setParseResult] = useState<ParseResult>(null);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    const saved = window.localStorage.getItem("careeros_token");
    if (saved) setToken(saved);
  }, []);

  useEffect(() => {
    if (!token) return;
    hydrate(token);
  }, [token]);

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
      await Promise.all([refreshDashboard(authToken), refreshHistory(authToken)]);
      await refreshResumes(authToken);
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

  async function refreshDashboard(authToken = token) {
    if (!authToken) return;
    const d = (await api.dashboard(authToken)) as Dashboard;
    setDashboard(d);
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

  async function onUploadResume(file: File) {
    if (!token) return setStatus("Login required");
    setUploading(true);
    setParseResult(null);
    try {
      const result = await api.uploadResume(token, file);
      setParseResult(result);
      setStatus(`Resume parsed — ${result.sections.length} sections found`);
      await refreshResumes(token);
    } catch (e) {
      setStatus(errMsg(e, "Upload failed"));
    } finally {
      setUploading(false);
    }
  }

  async function downloadExport() {
    if (!token || !exportJobId) return;
    try {
      const blob = await api.downloadExport(token, exportJobId);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `resume_export_${exportJobId}.pdf`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch {
      setStatus("Export download failed");
    }
  }

  return {
    status,
    uploading,
    parseResult,
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
    dashboard,
    history,
    exportJobId,
    exportStatus,
    onRegister,
    onLogin,
    onSaveProfile,
    onGenerateResume,
    onScan,
    refreshDashboard,
    onExportResume,
    checkExport,
    downloadExport,
    onUploadResume,
  };
}
