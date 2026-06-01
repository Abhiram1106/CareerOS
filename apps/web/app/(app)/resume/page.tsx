"use client";

import { ResumeDropzone } from "../../../components/workspace/ResumeDropzone";
import { usePlacementWorkspace } from "../../../hooks/usePlacementWorkspace";
import { TEMPLATE_OPTIONS } from "../../../lib/placement";

export default function ResumePage() {
  const ws = usePlacementWorkspace("resume");

  return (
    <div className="page-canvas">
      <div className="page-title-row">
        <div>
          <h1 className="page-title">Resume</h1>
          <p className="page-subtitle">Upload, parse, and export ATS-safe versions with persistent session state.</p>
        </div>
      </div>

      <div className="workspace-grid">
        <div className="content-card">
          <div className="content-card-header">
            <h2 className="content-card-title">Document Intelligence</h2>
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
                          <span>{f}</span>
                          <span className="ats-flag-badge">HIGH RISK</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                <p className="section-list-heading">Extracted sections</p>
                <div className="section-list">
                  {ws.parseResult.sections.map((s) => (
                    <div key={s.section_name} className="section-list-item">
                      <div>
                        <p className="section-list-name">{s.section_name}</p>
                      </div>
                      <span className="section-conf-badge">{Math.round(s.confidence * 100)}% CONF</span>
                    </div>
                  ))}
                </div>

                <button type="button" className="btn-secondary" onClick={ws.replaceResume}>
                  Replace resume
                </button>
              </div>
            )}
          </div>
        </div>

        <div className="content-card">
          <div className="content-card-header">
            <h2 className="content-card-title">Generation & Export</h2>
          </div>
          <div className="content-card-body">
            <label className="auth-label" htmlFor="template-select">
              Template
            </label>
            <select
              id="template-select"
              className="auth-input workspace-select"
              value={ws.template}
              onChange={(e) => ws.setTemplate(e.target.value as typeof ws.template)}
            >
              {TEMPLATE_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
            <pre className="resume-preview-snippet">{ws.resumePreview}</pre>
            <button
              type="button"
              className="btn-primary btn-block"
              disabled={!ws.canGenerate || ws.generating}
              onClick={() => void ws.generateResume()}
            >
              {ws.generating ? "Generating..." : "Generate Resume"}
            </button>
            <div className="export-actions">
              <button
                type="button"
                className="btn-secondary btn-flex"
                disabled={!ws.canExport}
                onClick={() => void ws.queueExport()}
              >
                Queue ATS-safe PDF
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
          </div>
        </div>
      </div>
    </div>
  );
}
