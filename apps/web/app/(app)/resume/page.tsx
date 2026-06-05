"use client";

import { useState } from "react";
import Link from "next/link";
import { ResumeDropzone } from "../../../components/workspace/ResumeDropzone";
import { usePlacementWorkspace } from "../../../hooks/usePlacementWorkspace";
import { type TemplateName } from "../../../lib/placement";

const TEMPLATES: {
  value: TemplateName;
  label: string;
  badge: string;
  badgeClass: string;
  description: string;
}[] = [
  {
    value: "classic",
    label: "Classic ATS",
    badge: "Maximum ATS ✓",
    badgeClass: "chip-success",
    description: "Single-column, no tables. Best for bulk applications to large companies using Taleo, Workday, Naukri.",
  },
  {
    value: "technical",
    label: "Technical / Dev",
    badge: "High ATS ✓",
    badgeClass: "chip-primary",
    description: "GitHub & skills front-and-center. Ideal for SWE, DevOps, and data roles at product companies.",
  },
  {
    value: "fresher",
    label: "Fresher Graduate",
    badge: "High ATS ✓",
    badgeClass: "chip-primary",
    description: "Education-first layout. Emphasises projects and coursework for campus placement drives.",
  },
];

export default function ResumePage() {
  const ws = usePlacementWorkspace("resume");
  const [selectedTemplate, setSelectedTemplate] = useState<TemplateName>("classic");

  return (
    <div className="page-canvas">
      <div className="page-title-row">
        <div>
          <h1 className="page-title">Resume</h1>
          <p className="page-subtitle">Upload an existing resume or generate one from your profile.</p>
        </div>
        <Link
          href="/resume/wizard"
          className="btn-primary"
          style={{ alignSelf: "center", textDecoration: "none", whiteSpace: "nowrap" }}
        >
          🧙 Improvement Wizard
        </Link>
      </div>

      <div className="workspace-grid">
        {/* ── Upload / parse card ─────────────────────────────────── */}
        <div className="content-card">
          <div className="content-card-header">
            <h2 className="content-card-title">Upload Resume</h2>
            {ws.parseResult ? (
              <span className="chip chip-mono">
                {ws.parseResult.char_count.toLocaleString()} chars · {ws.parseResult.sections.length} sections
              </span>
            ) : null}
          </div>
          <div className="content-card-body">
            {!ws.parseResult ? (
              <ResumeDropzone
                disabled={!ws.canUpload}
                uploading={ws.uploading}
                error={ws.uploadError}
                onFile={(file) => void ws.uploadResume(file)}
              />
            ) : (
              <div>
                {ws.parseResult.ats_flags.length > 0 && (
                  <div className="ats-warning-panel">
                    <p className="ats-warning-title">ATS warnings ({ws.parseResult.ats_flags.length})</p>
                    <ul className="ats-warning-list">
                      {ws.parseResult.ats_flags.map((f) => (
                        <li key={f}>
                          <span>{f.replace(/_/g, " ")}</span>
                          <span className="ats-flag-badge">RISK</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                <p className="section-list-heading">Extracted sections</p>
                <div className="section-list">
                  {ws.parseResult.sections.map((s) => (
                    <div key={s.section_name} className="section-list-item">
                      <p className="section-list-name">{s.section_name}</p>
                      <span className="section-conf-badge">{Math.round(s.confidence * 100)}% CONF</span>
                    </div>
                  ))}
                </div>

                <button type="button" className="btn-secondary" onClick={ws.replaceResume} style={{ marginTop: 12 }}>
                  Replace resume
                </button>
              </div>
            )}
          </div>
        </div>

        {/* ── Generate & export card ──────────────────────────────── */}
        <div className="content-card">
          <div className="content-card-header">
            <h2 className="content-card-title">Generate from Profile</h2>
            <span className="chip chip-mono">Reads your Settings profile</span>
          </div>
          <div className="content-card-body">
            {/* Template gallery */}
            <p className="auth-label" style={{ marginBottom: 10 }}>Choose template</p>
            <div style={{ display: "flex", flexDirection: "column", gap: 10, marginBottom: 18 }}>
              {TEMPLATES.map((t) => (
                <button
                  key={t.value}
                  type="button"
                  onClick={() => {
                    setSelectedTemplate(t.value);
                    ws.setTemplate(t.value);
                  }}
                  style={{
                    display: "flex",
                    alignItems: "flex-start",
                    gap: 12,
                    padding: "12px 14px",
                    borderRadius: "var(--radius-md)",
                    border: selectedTemplate === t.value
                      ? "2px solid var(--accent)"
                      : "1px solid var(--line-strong)",
                    background: selectedTemplate === t.value ? "var(--accent-soft)" : "var(--surface-soft)",
                    cursor: "pointer",
                    textAlign: "left",
                    transition: "border-color var(--t-fast)",
                  }}
                >
                  <div style={{ flex: 1 }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 4 }}>
                      <span style={{ fontWeight: 700, fontSize: "0.9rem", color: "var(--ink)" }}>{t.label}</span>
                      <span className={`chip ${t.badgeClass}`} style={{ fontSize: "0.7rem", padding: "2px 8px" }}>{t.badge}</span>
                    </div>
                    <p style={{ fontSize: "0.8rem", color: "var(--muted)", margin: 0, lineHeight: 1.5 }}>{t.description}</p>
                  </div>
                  {selectedTemplate === t.value && (
                    <span style={{ color: "var(--accent)", fontSize: "1.1rem", marginTop: 2 }}>✓</span>
                  )}
                </button>
              ))}
            </div>

            <button
              type="button"
              className="btn-primary btn-block"
              disabled={!ws.canGenerate || ws.generating}
              onClick={() => void ws.generateResume()}
              style={{ marginBottom: 14 }}
            >
              {ws.generating ? "Generating…" : "Generate Resume"}
            </button>

            {ws.resumePreview ? (
              <div style={{ marginBottom: 14 }}>
                <p className="auth-label" style={{ marginBottom: 6 }}>Preview</p>
                <pre
                  style={{
                    fontSize: "0.72rem",
                    background: "var(--surface-soft)",
                    border: "1px solid var(--line)",
                    borderRadius: 8,
                    padding: "12px 14px",
                    overflowX: "auto",
                    maxHeight: 280,
                    overflowY: "auto",
                    lineHeight: 1.6,
                    whiteSpace: "pre-wrap",
                    fontFamily: "var(--font-mono)",
                  }}
                >
                  {ws.resumePreview}
                </pre>
              </div>
            ) : null}

            {/* Export */}
            <p className="auth-label" style={{ marginBottom: 8 }}>Export ATS-safe PDF</p>
            <div className="export-actions">
              <button
                type="button"
                className="btn-secondary btn-flex"
                disabled={!ws.canExport}
                onClick={() => void ws.queueExport()}
              >
                Queue PDF export
              </button>
              <button
                type="button"
                className="btn-icon"
                title="Refresh export status"
                disabled={!ws.exportJobId}
                onClick={() => void ws.refreshExportStatus()}
              >
                ↻
              </button>
              {ws.exportReady ? (
                <button type="button" className="btn-secondary btn-flex" onClick={() => void ws.downloadExport()}>
                  Download PDF
                </button>
              ) : null}
            </div>
            {ws.exportJobId ? (
              <p className="export-status-line">
                Export #{ws.exportJobId}: <strong>{ws.exportStatus || "queued"}</strong>
              </p>
            ) : null}
            {ws.actionError ? (
              <p className="workspace-error" role="alert" style={{ marginTop: 8 }}>{ws.actionError}</p>
            ) : null}
          </div>
        </div>
      </div>
    </div>
  );
}
