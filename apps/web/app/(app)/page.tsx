"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { getStoredAuth, type AuthUser } from "../../lib/auth";

const STATS = [
  { value: "42.6%", label: "Indian graduates unemployable (Mercer Mettl 2025)" },
  { value: "8.47L", label: "Engineering graduates per year" },
  { value: "450+", label: "Enterprise partners in network" },
  { value: "~2×", label: "Intel-accelerated parse throughput vs baseline" },
];

export default function OverviewPage() {
  const [user, setUser] = useState<AuthUser | null>(null);

  useEffect(() => {
    setUser(getStoredAuth());
  }, []);

  const isOfficer = user?.role === "officer";

  return (
    <div className="page-canvas">
      {/* Hero section */}
      <section style={{ textAlign: "center", padding: "48px 0 40px", position: "relative", overflow: "hidden" }}>
        {/* Mesh gradient background */}
        <div aria-hidden="true" style={{
          position: "absolute", inset: 0, zIndex: 0, pointerEvents: "none",
          background: "radial-gradient(circle at 15% 50%, rgba(0,88,156,0.08), transparent 40%), radial-gradient(circle at 85% 30%, rgba(0,113,197,0.06), transparent 40%), radial-gradient(circle at 50% 80%, rgba(123,208,255,0.06), transparent 40%)",
        }} />

        <div style={{ position: "relative", zIndex: 1 }}>
          {/* Intel badge */}
          <div style={{ display: "inline-flex", alignItems: "center", gap: 8, background: "rgba(236,238,241,0.8)", backdropFilter: "blur(8px)", borderRadius: 9999, padding: "6px 14px", marginBottom: 20, border: "1px solid rgba(0,88,156,0.15)", fontSize: "0.78rem", fontFamily: "var(--font-mono)", fontWeight: 500, color: "#00589c" }}>
            <span style={{ width: 8, height: 8, borderRadius: "50%", background: "#0071c5", display: "inline-block" }} className="icon-shimmer" />
            Intel-optimized · Week {new Date().getFullYear() >= 2026 ? "2" : "1"} live
          </div>

          <h1 style={{ fontFamily: "var(--font-display)", fontSize: "clamp(2rem, 5vw, 3.2rem)", fontWeight: 800, letterSpacing: "-0.04em", lineHeight: 1.1, background: "linear-gradient(135deg, #00589c, #0071c5, #005d7f)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent", marginBottom: 16 }}>
            The placement-readiness<br />operating layer for Indian colleges
          </h1>

          <p style={{ fontSize: "1.05rem", color: "#414752", maxWidth: 600, margin: "0 auto 36px", lineHeight: 1.65 }}>
            Turn unstructured resumes into structured, actionable readiness signals. Empowering placement cells with deterministic AI and{" "}
            <strong style={{ color: "#0071c5" }}>Intel-accelerated compute</strong>.
          </p>

          {/* Not-a-job-board disclaimer */}
          <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 16, flexWrap: "wrap", marginBottom: 40, fontFamily: "var(--font-mono)", fontSize: "0.72rem", color: "#717783" }}>
            <span style={{ textDecoration: "line-through" }}>Not a job board</span>
            <span>·</span>
            <span style={{ textDecoration: "line-through" }}>Not a LinkedIn scraper</span>
            <span>·</span>
            <span style={{ textDecoration: "line-through" }}>Not a resume builder</span>
          </div>

          {/* RBAC CTA cards */}
          <div style={{ display: "flex", gap: 20, justifyContent: "center", flexWrap: "wrap", maxWidth: 860, margin: "0 auto" }}>
            {/* Student card */}
            <div className="rbac-card" style={{ flex: "1 1 340px", maxWidth: 400, textAlign: "left" }}>
              <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 12 }}>
                <div style={{ width: 44, height: 44, borderRadius: 10, background: "rgba(0,88,156,0.1)", display: "grid", placeItems: "center", color: "#00589c", flexShrink: 0 }}>
                  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M22 10v6M2 10l10-5 10 5-10 5z" /><path d="M6 12v5c3 3 9 3 12 0v-5" />
                  </svg>
                </div>
                <div>
                  <h3 style={{ fontFamily: "var(--font-display)", fontSize: "1.05rem", fontWeight: 700, color: "#191c1e", margin: 0 }}>For Students</h3>
                  <span style={{ fontFamily: "var(--font-mono)", fontSize: "0.68rem", color: "#717783", textTransform: "uppercase", letterSpacing: "0.06em" }}>Priya's path</span>
                </div>
              </div>
              <p style={{ fontSize: "0.88rem", color: "#414752", lineHeight: 1.6, marginBottom: 20 }}>
                Analyze your resume, identify skill gaps vs. your target JD, and get proof-linked improvement suggestions — not fabricated claims.
              </p>
              <Link href="/workspace" style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 8, width: "100%", padding: "13px", borderRadius: 9999, background: "linear-gradient(135deg, #001c38, #00589c)", color: "#fff", fontWeight: 600, fontSize: "0.9rem", textDecoration: "none", boxShadow: "0 4px 14px rgba(0,28,56,0.2)", transition: "box-shadow 0.15s, transform 0.1s" }}>
                Open student workspace
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M5 12h14M12 5l7 7-7 7" />
                </svg>
              </Link>
            </div>

            {/* Officer card */}
            <div className="rbac-card" style={{ flex: "1 1 340px", maxWidth: 400, textAlign: "left" }}>
              <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 12 }}>
                <div style={{ width: 44, height: 44, borderRadius: 10, background: "rgba(0,93,127,0.1)", display: "grid", placeItems: "center", color: "#005d7f", flexShrink: 0 }}>
                  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
                  </svg>
                </div>
                <div>
                  <h3 style={{ fontFamily: "var(--font-display)", fontSize: "1.05rem", fontWeight: 700, color: "#191c1e", margin: 0 }}>For Placement Officers</h3>
                  <span style={{ fontFamily: "var(--font-mono)", fontSize: "0.68rem", color: "#717783", textTransform: "uppercase", letterSpacing: "0.06em" }}>Mr. Ramesh's dashboard</span>
                </div>
              </div>
              <p style={{ fontSize: "0.88rem", color: "#414752", lineHeight: 1.6, marginBottom: 20 }}>
                Monitor batch readiness, view department heatmaps, enforce AI guardrails, and track top skill gaps before every drive.
              </p>
              <Link href="/officer" style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 8, width: "100%", padding: "13px", borderRadius: 10, background: "transparent", color: "#005d7f", fontWeight: 600, fontSize: "0.9rem", textDecoration: "none", border: "2px solid #005d7f", transition: "background 0.15s, color 0.15s" }}>
                Officer command center
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                  <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
                </svg>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Stats row */}
      <section style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(180px, 1fr))", gap: 14, marginBottom: 40 }}>
        {STATS.map(s => (
          <div key={s.value} style={{ background: "#fff", border: "1px solid rgba(192,199,211,0.4)", borderRadius: 12, padding: "18px 20px", boxShadow: "0 1px 4px rgba(0,28,56,0.05)" }}>
            <div style={{ fontFamily: "var(--font-display)", fontSize: "1.6rem", fontWeight: 800, color: "#0071c5", letterSpacing: "-0.03em", marginBottom: 6 }}>{s.value}</div>
            <p style={{ fontSize: "0.8rem", color: "#414752", lineHeight: 1.5, margin: 0 }}>{s.label}</p>
          </div>
        ))}
      </section>

      {/* Week roadmap */}
      <section>
        <div className="content-card">
          <div className="content-card-header">
            <h2 className="content-card-title">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0071c5" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <rect x="3" y="4" width="18" height="18" rx="2" /><line x1="16" y1="2" x2="16" y2="6" /><line x1="8" y1="2" x2="8" y2="6" /><line x1="3" y1="10" x2="21" y2="10" />
              </svg>
              5-Week Build Roadmap
            </h2>
            <span className="chip chip-primary">Intel AI Bootcamp</span>
          </div>
          <div className="content-card-body" style={{ padding: "0 0 4px" }}>
            <table className="stitch-table">
              <thead>
                <tr>
                  <th>Week</th>
                  <th>Focus</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {[
                  { week: "W1", focus: "Foundation — auth, resume upload, pdfplumber parser, UI shell", done: true },
                  { week: "W2", focus: "JD parser · match-engine (TF-IDF + embeddings + sklearnex) · score UI", done: false },
                  { week: "W3", focus: "AI rewriter with proof-linked JSON guardrails · PDF export", done: false },
                  { week: "W4", focus: "Officer dashboard · batch upload · dept heatmap · review queue", done: false },
                  { week: "W5", focus: "Intel bench harness (OpenVINO + sklearnex) · /lab panel · pitch deck", done: false },
                ].map(row => (
                  <tr key={row.week}>
                    <td>
                      <span className="chip chip-mono">{row.week}</span>
                    </td>
                    <td style={{ color: "#414752" }}>{row.focus}</td>
                    <td>
                      {row.done
                        ? <span className="chip chip-success">✓ Done</span>
                        : <span className="chip" style={{ background: "#eceef1", color: "#717783" }}>Pending</span>}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </div>
  );
}
