"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { api } from "../../../lib/api";
import { getStoredAuth } from "../../../lib/auth";
import { toErrorMessage } from "../../../lib/errors";

type ProfileData = {
  full_name: string;
  email: string;
  city: string;
  professional_status: string;
  target_role: string;
  skills_csv: string;
  summary: string;
  experience_bullet: string;
  cgpa: number | null;
  active_backlogs: number;
  branch: string;
  grad_year: number | null;
};

const BRANCH_OPTIONS = ["CSE", "IT", "ECE", "EEE", "ME", "CE", "AIML", "Other"];

export default function SettingsPage() {
  const auth = getStoredAuth();
  const token = auth?.token ?? "";

  const [profile, setProfile] = useState<ProfileData | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!token) return;
    void api
      .getProfile(token)
      .then((res) => setProfile(res as ProfileData))
      .catch((err) => setError(toErrorMessage(err, "Could not load profile")))
      .finally(() => setLoading(false));
  }, [token]);

  async function handleSave(e: React.FormEvent) {
    e.preventDefault();
    if (!profile || !token) return;
    setSaving(true);
    setError(null);
    setSaved(false);
    try {
      await api.updateProfile(token, {
        city: profile.city,
        professional_status: profile.professional_status,
        target_role: profile.target_role,
        skills_csv: profile.skills_csv,
        summary: profile.summary,
        experience_bullet: profile.experience_bullet,
        cgpa: profile.cgpa,
        active_backlogs: profile.active_backlogs,
        branch: profile.branch,
        grad_year: profile.grad_year,
      });
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (err) {
      setError(toErrorMessage(err, "Save failed"));
    } finally {
      setSaving(false);
    }
  }

  function field(key: keyof ProfileData) {
    return (val: string) =>
      setProfile((prev) => (prev ? { ...prev, [key]: val } : prev));
  }

  function numField(key: keyof ProfileData) {
    return (val: string) =>
      setProfile((prev) =>
        prev ? { ...prev, [key]: val === "" ? null : Number(val) } : prev
      );
  }

  if (loading) {
    return (
      <div className="page-canvas">
        <div className="content-card">
          <div className="content-card-body">Loading profile...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="page-canvas">
      <div className="page-title-row">
        <div>
          <h1 className="page-title">Settings</h1>
          <p className="page-subtitle">
            Your profile data is used in scoring and eligibility checks. Keep it accurate.
          </p>
        </div>
      </div>

      {error ? (
        <div className="content-card" style={{ marginBottom: 16 }}>
          <div className="content-card-body" style={{ color: "#93000a" }}>
            {error}
          </div>
        </div>
      ) : null}

      {profile ? (
        <form onSubmit={handleSave}>
          {/* ── Basic info ──────────────────────────────────────────── */}
          <div className="content-card" style={{ marginBottom: 16 }}>
            <div className="content-card-header">
              <h2 className="content-card-title">Basic Information</h2>
            </div>
            <div className="content-card-body">
              <div className="settings-grid">
                <div className="auth-field">
                  <label className="auth-label" htmlFor="s-name">Full name</label>
                  <input id="s-name" className="auth-input" value={profile.full_name} disabled />
                </div>
                <div className="auth-field">
                  <label className="auth-label" htmlFor="s-email">Email</label>
                  <input id="s-email" className="auth-input" value={profile.email} disabled />
                </div>
                <div className="auth-field">
                  <label className="auth-label" htmlFor="s-city">City</label>
                  <input
                    id="s-city"
                    className="auth-input"
                    value={profile.city}
                    onChange={(e) => field("city")(e.target.value)}
                    placeholder="e.g. Bengaluru"
                  />
                </div>
                <div className="auth-field">
                  <label className="auth-label" htmlFor="s-role">Target role</label>
                  <input
                    id="s-role"
                    className="auth-input"
                    value={profile.target_role}
                    onChange={(e) => field("target_role")(e.target.value)}
                    placeholder="e.g. Backend Engineer"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* ── Eligibility fields ─────────────────────────────────── */}
          <div className="content-card" style={{ marginBottom: 16 }}>
            <div className="content-card-header">
              <h2 className="content-card-title">Academic Eligibility</h2>
              <span className="chip chip-mono">Used in JD match scoring</span>
            </div>
            <div className="content-card-body">
              <p className="scan-intro" style={{ marginBottom: 14 }}>
                These fields are compared against JD eligibility criteria (CGPA cutoff, backlog limits, branch filters).
                Accurate values give you a real eligibility score instead of a 90/100 placeholder.
              </p>
              <div className="settings-grid">
                <div className="auth-field">
                  <label className="auth-label" htmlFor="s-cgpa">CGPA (out of 10)</label>
                  <input
                    id="s-cgpa"
                    type="number"
                    step="0.01"
                    min="0"
                    max="10"
                    className="auth-input"
                    value={profile.cgpa ?? ""}
                    onChange={(e) => numField("cgpa")(e.target.value)}
                    placeholder="e.g. 8.4"
                  />
                </div>
                <div className="auth-field">
                  <label className="auth-label" htmlFor="s-backlogs">Active backlogs</label>
                  <input
                    id="s-backlogs"
                    type="number"
                    min="0"
                    className="auth-input"
                    value={profile.active_backlogs}
                    onChange={(e) => numField("active_backlogs")(e.target.value)}
                    placeholder="0"
                  />
                </div>
                <div className="auth-field">
                  <label className="auth-label" htmlFor="s-branch">Branch</label>
                  <select
                    id="s-branch"
                    className="auth-input workspace-select"
                    value={profile.branch}
                    onChange={(e) => field("branch")(e.target.value)}
                  >
                    <option value="">— Select branch —</option>
                    {BRANCH_OPTIONS.map((b) => (
                      <option key={b} value={b}>{b}</option>
                    ))}
                  </select>
                </div>
                <div className="auth-field">
                  <label className="auth-label" htmlFor="s-gradyear">Graduation year</label>
                  <input
                    id="s-gradyear"
                    type="number"
                    min="2020"
                    max="2030"
                    className="auth-input"
                    value={profile.grad_year ?? ""}
                    onChange={(e) => numField("grad_year")(e.target.value)}
                    placeholder="e.g. 2025"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* ── Skills & summary ───────────────────────────────────── */}
          <div className="content-card" style={{ marginBottom: 16 }}>
            <div className="content-card-header">
              <h2 className="content-card-title">Skills & Summary</h2>
            </div>
            <div className="content-card-body">
              <div className="auth-field">
                <label className="auth-label" htmlFor="s-skills">
                  Skills (comma-separated)
                </label>
                <input
                  id="s-skills"
                  className="auth-input"
                  value={profile.skills_csv}
                  onChange={(e) => field("skills_csv")(e.target.value)}
                  placeholder="Python, SQL, Docker, React"
                />
              </div>
              <div className="auth-field">
                <label className="auth-label" htmlFor="s-summary">Professional summary</label>
                <textarea
                  id="s-summary"
                  className="jd-textarea"
                  rows={3}
                  value={profile.summary}
                  onChange={(e) => field("summary")(e.target.value)}
                  placeholder="2–3 sentences about your background and strongest skills."
                />
              </div>
              <div className="auth-field">
                <label className="auth-label" htmlFor="s-exp">Key experience bullet</label>
                <textarea
                  id="s-exp"
                  className="jd-textarea"
                  rows={3}
                  value={profile.experience_bullet}
                  onChange={(e) => field("experience_bullet")(e.target.value)}
                  placeholder="Built X using Y, achieving Z% improvement."
                />
              </div>
            </div>
          </div>

          <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
            <button type="submit" className="btn-primary" disabled={saving}>
              {saving ? "Saving…" : "Save profile"}
            </button>
            {saved ? (
              <span style={{ color: "#16a34a", fontSize: "0.88rem", fontWeight: 600 }}>
                ✓ Saved
              </span>
            ) : null}
          </div>
        </form>
      ) : null}

      <div className="content-card" style={{ marginTop: 20 }}>
        <div className="content-card-header">
          <h2 className="content-card-title">Privacy</h2>
        </div>
        <div className="content-card-body">
          <Link href="/privacy/assistant" className="btn-secondary">
            Assistant privacy notice
          </Link>
        </div>
      </div>
    </div>
  );
}
