"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { storeAuth, DEMO_USERS, type UserRole } from "../../../lib/auth";
import type { AuthResponse } from "../../../lib/api";

const API = process.env.NEXT_PUBLIC_CORE_API_URL ?? "http://localhost:8000";
const DEMO = process.env.NEXT_PUBLIC_DEMO === "true";

export default function LoginPage() {
  const router = useRouter();
  const [role, setRole] = useState<UserRole>("student");
  const [email, setEmail] = useState(DEMO ? "student@demo.cos" : "");
  const [password, setPassword] = useState(DEMO ? "demo" : "");
  const [remember, setRemember] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      // Demo mode: bypass API
      if (DEMO && DEMO_USERS[email]) {
        const user = DEMO_USERS[email];
        storeAuth(user);
        router.replace(user.role === "officer" ? "/officer" : "/workspace");
        return;
      }

      const res = await fetch(`${API}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        setError((data as { detail?: string }).detail ?? "Invalid email or password.");
        return;
      }

      const data = (await res.json()) as AuthResponse;
      storeAuth({ token: data.token, email: data.email, full_name: data.full_name, role: (data.role ?? role) as UserRole });
      router.replace(data.role === "officer" ? "/officer" : "/workspace");
    } catch {
      setError("Cannot reach the server. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  function fillDemo(r: UserRole) {
    setRole(r);
    setEmail(r === "officer" ? "officer@demo.cos" : "student@demo.cos");
    setPassword("demo");
    setError(null);
  }

  return (
    <div className="auth-page">
      {/* Left brand panel */}
      <div className="auth-brand">
        <div className="auth-brand-overlay" />
        {/* Logo */}
        <div className="auth-brand-logo">
          <div className="auth-brand-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M22 10v6M2 10l10-5 10 5-10 5z" />
              <path d="M6 12v5c3 3 9 3 12 0v-5" />
            </svg>
          </div>
          <span className="auth-brand-name">CareerOS <span>Campus AI</span></span>
        </div>

        {/* Body copy */}
        <div className="auth-brand-body">
          <h2 className="auth-brand-headline">
            Powering the next generation of campus placements.
          </h2>
          <p className="auth-brand-sub">
            An ecosystem optimized for high-performance recruitment, bringing data-driven clarity to the academic landscape.
          </p>

          {/* Glassmorphism status panel */}
          <div className="auth-brand-glass">
            <div className="auth-brand-glass-row">
              <svg className="icon-sm" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#a2c9ff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <rect x="2" y="3" width="20" height="14" rx="2" />
                <path d="M8 21h8M12 17v4" />
              </svg>
              <span className="auth-brand-glass-label">System Status</span>
            </div>
            <p className="auth-brand-glass-text">
              Matchmaking engine online. Processing real-time placement data across 450+ enterprise partners.
            </p>
          </div>
        </div>

        {/* Footer */}
        <p className="auth-brand-footer">Secure Infrastructure · Enterprise Grade</p>
      </div>

      {/* Right form panel */}
      <div className="auth-form-panel">
        <div className="auth-form-box">
          {/* Mobile logo */}
          <div className="auth-mobile-logo">
            <div className="auth-mobile-logo-icon">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M22 10v6M2 10l10-5 10 5-10 5z" />
                <path d="M6 12v5c3 3 9 3 12 0v-5" />
              </svg>
            </div>
            <span className="auth-mobile-logo-text">CareerOS</span>
          </div>

          {/* Demo banner */}
          {DEMO && (
            <div style={{ background: "linear-gradient(90deg, #004c85, #0071c5)", color: "#fff", borderRadius: 8, padding: "10px 14px", marginBottom: 20, fontSize: "0.82rem", display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap" }}>
              <span style={{ background: "rgba(255,255,255,0.2)", borderRadius: 9999, padding: "2px 8px", fontWeight: 700, fontSize: "0.7rem", textTransform: "uppercase", letterSpacing: "0.06em" }}>Demo</span>
              <span>Pre-filled with demo credentials. Click Sign In to continue.</span>
              <span style={{ marginLeft: "auto", display: "flex", gap: 8 }}>
                <button type="button" onClick={() => fillDemo("student")} style={{ background: "rgba(255,255,255,0.15)", border: "none", borderRadius: 6, color: "#fff", padding: "4px 10px", fontSize: "0.78rem", cursor: "pointer" }}>Student</button>
                <button type="button" onClick={() => fillDemo("officer")} style={{ background: "rgba(255,255,255,0.15)", border: "none", borderRadius: 6, color: "#fff", padding: "4px 10px", fontSize: "0.78rem", cursor: "pointer" }}>Officer</button>
              </span>
            </div>
          )}

          <h2 className="auth-heading">Welcome back</h2>
          <p className="auth-sub">Please enter your details to access your command center.</p>

          {/* Role tabs */}
          <div className="auth-role-tabs" role="tablist" aria-label="Login role">
            <button
              type="button"
              role="tab"
              aria-selected={role === "student"}
              className={`auth-role-tab${role === "student" ? " active" : ""}`}
              onClick={() => { setRole("student"); setError(null); }}
            >
              Student
            </button>
            <button
              type="button"
              role="tab"
              aria-selected={role === "officer"}
              className={`auth-role-tab${role === "officer" ? " active" : ""}`}
              onClick={() => { setRole("officer"); setError(null); }}
            >
              Placement Officer
            </button>
          </div>

          {/* Error */}
          {error && (
            <div className="auth-error" role="alert">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="10" /><line x1="12" y1="8" x2="12" y2="12" /><line x1="12" y1="16" x2="12.01" y2="16" />
              </svg>
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            {/* Email */}
            <div className="auth-field">
              <label className="auth-label" htmlFor="login-email">Academic Email</label>
              <div className="auth-input-wrap">
                <span className="auth-input-icon" aria-hidden="true">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <rect x="2" y="4" width="20" height="16" rx="2" /><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7" />
                  </svg>
                </span>
                <input
                  id="login-email"
                  type="email"
                  className="auth-input"
                  placeholder="you@university.edu"
                  value={email}
                  onChange={e => setEmail(e.target.value)}
                  autoComplete="email"
                  required
                />
              </div>
            </div>

            {/* Password */}
            <div className="auth-field">
              <label className="auth-label" htmlFor="login-password">Password</label>
              <div className="auth-input-wrap">
                <span className="auth-input-icon" aria-hidden="true">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <rect x="3" y="11" width="18" height="11" rx="2" /><path d="M7 11V7a5 5 0 0 1 10 0v4" />
                  </svg>
                </span>
                <input
                  id="login-password"
                  type="password"
                  className="auth-input"
                  placeholder="••••••••"
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                  autoComplete="current-password"
                  required
                />
              </div>
            </div>

            {/* Remember + Forgot */}
            <div className="auth-remember-row">
              <label className="auth-remember">
                <input
                  type="checkbox"
                  checked={remember}
                  onChange={e => setRemember(e.target.checked)}
                />
                <span className="auth-remember-label">Remember me</span>
              </label>
              <Link href="#" className="auth-link">Forgot Password?</Link>
            </div>

            <button type="submit" className="auth-submit" disabled={loading}>
              {loading ? "Signing in…" : "Sign In"}
              {!loading && (
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M5 12h14M12 5l7 7-7 7" />
                </svg>
              )}
            </button>
          </form>

          <div className="auth-footer">
            <p className="auth-footer-text">
              New to CareerOS?{" "}
              <Link href="/register" className="auth-link" style={{ fontWeight: 700 }}>Create an account</Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
