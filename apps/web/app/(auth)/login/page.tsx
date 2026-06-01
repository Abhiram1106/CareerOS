"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { storeAuth } from "../../../lib/auth";
import { login as loginRequest } from "../../../modules/auth/authService";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [remember, setRemember] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const data = await loginRequest({ email, password });
      storeAuth({
        token: data.token,
        email: data.email,
        full_name: data.full_name,
        role: "student",
      });
      router.replace("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Cannot reach the server. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-brand">
        <div className="auth-brand-overlay" />
        <div className="auth-brand-logo">
          <div className="auth-brand-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M22 10v6M2 10l10-5 10 5-10 5z" />
              <path d="M6 12v5c3 3 9 3 12 0v-5" />
            </svg>
          </div>
          <span className="auth-brand-name">
            CareerOS <span>Student AI</span>
          </span>
        </div>

        <div className="auth-brand-body">
          <h2 className="auth-brand-headline">Intel-optimized placement scoring for Indian students.</h2>
          <p className="auth-brand-sub">
            Upload your resume, match against real JDs, and improve with proof-linked rewrites before campus drives.
          </p>

          <div className="auth-brand-glass">
            <div className="auth-brand-glass-row">
              <svg className="icon-sm" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#a2c9ff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <rect x="2" y="3" width="20" height="14" rx="2" />
                <path d="M8 21h8M12 17v4" />
              </svg>
              <span className="auth-brand-glass-label">System Status</span>
            </div>
            <p className="auth-brand-glass-text">
              Resume intelligence, JD matching, and ATS-safe export are available in your student workspace.
            </p>
          </div>
        </div>

        <p className="auth-brand-footer">Secure Infrastructure · Enterprise Grade</p>
      </div>

      <div className="auth-form-panel">
        <div className="auth-form-box">
          <div className="auth-mobile-logo">
            <div className="auth-mobile-logo-icon">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M22 10v6M2 10l10-5 10 5-10 5z" />
                <path d="M6 12v5c3 3 9 3 12 0v-5" />
              </svg>
            </div>
            <span className="auth-mobile-logo-text">CareerOS</span>
          </div>

          <h2 className="auth-heading">Welcome back</h2>
          <p className="auth-sub">Sign in to continue your placement readiness journey.</p>

          {error && (
            <div className="auth-error" role="alert">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="10" />
                <line x1="12" y1="8" x2="12" y2="12" />
                <line x1="12" y1="16" x2="12.01" y2="16" />
              </svg>
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <div className="auth-field">
              <label className="auth-label" htmlFor="login-email">
                Academic Email
              </label>
              <div className="auth-input-wrap">
                <span className="auth-input-icon" aria-hidden="true">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <rect x="2" y="4" width="20" height="16" rx="2" />
                    <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7" />
                  </svg>
                </span>
                <input
                  id="login-email"
                  type="email"
                  className="auth-input"
                  placeholder="you@university.edu"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  autoComplete="email"
                  required
                />
              </div>
            </div>

            <div className="auth-field">
              <label className="auth-label" htmlFor="login-password">
                Password
              </label>
              <div className="auth-input-wrap">
                <span className="auth-input-icon" aria-hidden="true">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <rect x="3" y="11" width="18" height="11" rx="2" />
                    <path d="M7 11V7a5 5 0 0 1 10 0v4" />
                  </svg>
                </span>
                <input
                  id="login-password"
                  type="password"
                  className="auth-input"
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  autoComplete="current-password"
                  required
                />
              </div>
            </div>

            <div className="auth-remember-row">
              <label className="auth-remember">
                <input type="checkbox" checked={remember} onChange={(e) => setRemember(e.target.checked)} />
                <span className="auth-remember-label">Remember me</span>
              </label>
              <span className="auth-help-text">Need password help? Contact your placement coordinator.</span>
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
              <Link href="/register" className="auth-link" style={{ fontWeight: 700 }}>
                Create an account
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
