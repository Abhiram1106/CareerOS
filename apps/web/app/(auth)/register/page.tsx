"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { storeAuth } from "../../../lib/auth";
import { register as registerRequest } from "../../../modules/auth/authService";

const YEARS = ["2024", "2025", "2026", "2027", "2028"];

export default function RegisterPage() {
  const router = useRouter();
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [batchYear, setBatchYear] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const data = await registerRequest({
        full_name: fullName,
        email,
        password,
      });
      storeAuth({ token: data.token, email: data.email, full_name: data.full_name, role: "student" });
      router.replace("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Cannot reach the server. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-brand" style={{ flex: "0 0 42%" }}>
        <div className="auth-brand-overlay" />
        <div className="auth-brand-logo">
          <div className="auth-brand-icon">
            <svg
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M22 10v6M2 10l10-5 10 5-10 5z" />
              <path d="M6 12v5c3 3 9 3 12 0v-5" />
            </svg>
          </div>
          <span className="auth-brand-name">CareerOS</span>
        </div>

        <div className="auth-brand-body">
          <h2 className="auth-brand-headline">Start your placement readiness workspace.</h2>
          <p className="auth-brand-sub">
            Create your account and move from resume upload to job-specific readiness in one guided flow.
          </p>
          <div className="auth-brand-glass">
            <div className="auth-brand-glass-row">
              <svg
                className="icon-sm"
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                stroke="#a2c9ff"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <rect x="2" y="3" width="20" height="14" rx="2" />
                <path d="M8 21h8M12 17v4" />
              </svg>
              <span className="auth-brand-glass-label">Performance Core</span>
            </div>
            <p className="auth-brand-glass-text">
              Intel-accelerated matching pipeline with ATS-safe scoring for Indian academic resumes.
            </p>
          </div>
        </div>

        <p className="auth-brand-footer">Student-first workflow · Intel-optimized scoring</p>
      </div>

      <div className="auth-form-panel">
        <div className="auth-form-box" style={{ maxWidth: 480 }}>
          <div className="auth-mobile-logo">
            <div className="auth-mobile-logo-icon">
              <svg
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M22 10v6M2 10l10-5 10 5-10 5z" />
                <path d="M6 12v5c3 3 9 3 12 0v-5" />
              </svg>
            </div>
            <span className="auth-mobile-logo-text">CareerOS</span>
          </div>

          <h2 className="auth-heading">Create your account</h2>
          <p className="auth-sub">Set up your student workspace in one step.</p>

          {error && (
            <div className="auth-error" role="alert">
              <svg
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <circle cx="12" cy="12" r="10" />
                <line x1="12" y1="8" x2="12" y2="12" />
                <line x1="12" y1="16" x2="12.01" y2="16" />
              </svg>
              {error}
            </div>
          )}

          <div
            style={{
              background: "#fff",
              border: "1px solid rgba(192,199,211,0.4)",
              borderRadius: 18,
              padding: "24px",
              boxShadow: "0 4px 24px rgba(0,28,56,0.05)",
              transition: "box-shadow 0.2s",
            }}
          >
            <form onSubmit={handleSubmit}>
              <div className="auth-field">
                <label className="auth-label" htmlFor="reg-name">
                  Full Name
                </label>
                <div className="auth-input-wrap">
                  <span className="auth-input-icon">
                    <svg
                      width="18"
                      height="18"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    >
                      <circle cx="12" cy="8" r="4" />
                      <path d="M4 20c0-4 3.6-7 8-7s8 3 8 7" />
                    </svg>
                  </span>
                  <input
                    id="reg-name"
                    type="text"
                    className="auth-input"
                    placeholder="John Doe"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    autoComplete="name"
                    required
                  />
                </div>
              </div>

              <div className="auth-field">
                <label className="auth-label" htmlFor="reg-email">
                  University Email
                </label>
                <div className="auth-input-wrap">
                  <span className="auth-input-icon">
                    <svg
                      width="18"
                      height="18"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    >
                      <rect x="2" y="4" width="20" height="16" rx="2" />
                      <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7" />
                    </svg>
                  </span>
                  <input
                    id="reg-email"
                    type="email"
                    className="auth-input"
                    placeholder="john.doe@university.edu"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    autoComplete="email"
                    required
                  />
                </div>
              </div>

              <div className="auth-field">
                <label className="auth-label" htmlFor="reg-password">
                  Password
                </label>
                <div className="auth-input-wrap">
                  <span className="auth-input-icon">
                    <svg
                      width="18"
                      height="18"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    >
                      <rect x="3" y="11" width="18" height="11" rx="2" />
                      <path d="M7 11V7a5 5 0 0 1 10 0v4" />
                    </svg>
                  </span>
                  <input
                    id="reg-password"
                    type="password"
                    className="auth-input"
                    placeholder="********"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    autoComplete="new-password"
                    required
                    minLength={8}
                  />
                </div>
              </div>

              <div className="auth-field">
                <label className="auth-label" htmlFor="reg-batch">
                  Batch / Graduation Year
                </label>
                <div className="auth-input-wrap">
                  <span className="auth-input-icon">
                    <svg
                      width="18"
                      height="18"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    >
                      <path d="M22 10v6M2 10l10-5 10 5-10 5z" />
                      <path d="M6 12v5c3 3 9 3 12 0v-5" />
                    </svg>
                  </span>
                  <select
                    id="reg-batch"
                    className="auth-input"
                    value={batchYear}
                    onChange={(e) => setBatchYear(e.target.value)}
                    required
                    style={{ appearance: "none" }}
                  >
                    <option value="" disabled>
                      Select year
                    </option>
                    {YEARS.map((y) => (
                      <option key={y} value={y}>
                        Class of {y}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <button type="submit" className="auth-submit" disabled={loading}>
                {loading ? "Initializing..." : "Initialize Account"}
                {!loading && (
                  <svg
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2.5"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <path d="M5 12h14M12 5l7 7-7 7" />
                  </svg>
                )}
              </button>
            </form>
          </div>

          <div className="auth-footer">
            <p className="auth-footer-text">
              Already registered?{" "}
              <Link href="/login" className="auth-link" style={{ fontWeight: 700 }}>
                Return to Login
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
