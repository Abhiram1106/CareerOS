"use client";

import Link from "next/link";
import { useState } from "react";
import { api } from "../../../lib/api";
import { toErrorMessage } from "../../../lib/errors";

type Stage = "request" | "confirm" | "done";

export default function ResetPasswordPage() {
  const [stage, setStage] = useState<Stage>("request");
  const [email, setEmail] = useState("");
  const [token, setToken] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleRequest(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await api.requestPasswordReset(email);
      setStage("confirm");
    } catch (err) {
      setError(toErrorMessage(err, "Request failed. Try again."));
    } finally {
      setLoading(false);
    }
  }

  async function handleConfirm(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await api.confirmPasswordReset(token, newPassword);
      setStage("done");
    } catch (err) {
      setError(toErrorMessage(err, "Reset failed. Check your token."));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-brand">
        <div className="auth-brand-overlay" />
        <div className="auth-brand-logo">
          <div className="auth-brand-icon">CO</div>
          <span className="auth-brand-name">CareerOS <span>Campus AI</span></span>
        </div>
        <div className="auth-brand-body">
          <h2 className="auth-brand-headline">Reset your password.</h2>
          <p className="auth-brand-sub">
            A reset token will be printed to the server logs.
            Retrieve it with:{" "}
            <code style={{ fontSize: "0.8rem", background: "rgba(255,255,255,0.1)", padding: "2px 6px", borderRadius: 4 }}>
              docker compose logs core-api | grep PASSWORD_RESET_TOKEN
            </code>
          </p>
        </div>
        <p className="auth-brand-footer">Console-mode reset · No email required</p>
      </div>

      <div className="auth-form-panel">
        <div className="auth-form-box">
          <div className="auth-mobile-logo">
            <div className="auth-mobile-logo-icon">CO</div>
            <span className="auth-mobile-logo-text">CareerOS</span>
          </div>

          {stage === "request" && (
            <>
              <h2 className="auth-heading">Forgot password?</h2>
              <p className="auth-sub">Enter your email. A reset token appears in server logs.</p>
              {error && <div className="auth-error" role="alert">{error}</div>}
              <form onSubmit={handleRequest}>
                <div className="auth-field">
                  <label className="auth-label" htmlFor="r-email">Email</label>
                  <div className="auth-input-wrap">
                    <input
                      id="r-email"
                      type="email"
                      className="auth-input"
                      placeholder="you@university.edu"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      required
                    />
                  </div>
                </div>
                <button type="submit" className="auth-submit" disabled={loading}>
                  {loading ? "Sending…" : "Request reset token"}
                </button>
              </form>
            </>
          )}

          {stage === "confirm" && (
            <>
              <h2 className="auth-heading">Enter your token</h2>
              <p className="auth-sub">
                Copy the token from{" "}
                <code style={{ fontSize: "0.78rem" }}>docker compose logs core-api</code>{" "}
                and set your new password.
              </p>
              {error && <div className="auth-error" role="alert">{error}</div>}
              <form onSubmit={handleConfirm}>
                <div className="auth-field">
                  <label className="auth-label" htmlFor="r-token">Reset token</label>
                  <div className="auth-input-wrap">
                    <input
                      id="r-token"
                      type="text"
                      className="auth-input"
                      placeholder="Paste token from server logs"
                      value={token}
                      onChange={(e) => setToken(e.target.value)}
                      required
                    />
                  </div>
                </div>
                <div className="auth-field">
                  <label className="auth-label" htmlFor="r-pw">New password</label>
                  <div className="auth-input-wrap">
                    <input
                      id="r-pw"
                      type="password"
                      className="auth-input"
                      placeholder="At least 8 characters"
                      value={newPassword}
                      onChange={(e) => setNewPassword(e.target.value)}
                      minLength={8}
                      required
                    />
                  </div>
                </div>
                <button type="submit" className="auth-submit" disabled={loading}>
                  {loading ? "Resetting…" : "Set new password"}
                </button>
              </form>
            </>
          )}

          {stage === "done" && (
            <>
              <h2 className="auth-heading">Password updated</h2>
              <p className="auth-sub">All sessions were revoked. Sign in with your new password.</p>
              <Link href="/login" className="auth-submit" style={{ display: "block", textAlign: "center", textDecoration: "none" }}>
                Back to login
              </Link>
            </>
          )}

          <div className="auth-footer">
            <p className="auth-footer-text">
              <Link href="/login" className="auth-link">← Back to sign in</Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
