"use client";

import { useRef, useState } from "react";
import { getStoredAuth } from "../../../lib/auth";
import { uploadResume } from "../../../modules/resume/services/resumeService";
const DEMO = process.env.NEXT_PUBLIC_DEMO === "true";

type Section = { section_name: string; content_json: Record<string, unknown>; confidence: number };
type ParseResult = {
  resume_id: number;
  source_format: string;
  sections: Section[];
  ats_flags: string[];
  parse_warnings: string[];
  char_count: number;
} | null;

const SCORE_COMPONENTS = [
  { key: "jd_match",    label: "JD Match",           weight: "35%", color: "#0071c5" },
  { key: "ats_safety",  label: "ATS Parse Safety",   weight: "20%", color: "#16a34a" },
  { key: "evidence",    label: "Evidence Quality",   weight: "20%", color: "#005d7f" },
  { key: "completeness",label: "Profile Completeness",weight: "10%", color: "#d97706" },
  { key: "interview",   label: "Interview Readiness",weight: "10%", color: "#7c3aed" },
  { key: "hygiene",     label: "Placement Hygiene",  weight: "5%",  color: "#414752" },
];

const DEMO_SECTIONS: Section[] = [
  { section_name: "Professional Summary", content_json: { text: "Final year B.Tech CSE student with internship experience in Python and React." }, confidence: 0.98 },
  { section_name: "Education", content_json: { cgpa: "8.34/10", degree: "B.Tech CSE", year: "2026" }, confidence: 0.99 },
  { section_name: "Experience & Internships", content_json: { roles: ["SWE Intern @ Infosys (2025)"] }, confidence: 0.94 },
  { section_name: "Technical Skills", content_json: { skills: ["Python", "React", "Django", "SQL (basic)"] }, confidence: 0.91 },
  { section_name: "Projects", content_json: { projects: ["Placement Readiness Tracker", "E-commerce Portal"] }, confidence: 0.88 },
];

const DEMO_PARSE: ParseResult = {
  resume_id: 1,
  source_format: "pdf",
  sections: DEMO_SECTIONS,
  ats_flags: ["Two-column layout detected", "Table-based skills section"],
  parse_warnings: [],
  char_count: 4821,
};

type Tab = "resume" | "scan" | "readiness";

export default function WorkspacePage() {
  const auth = getStoredAuth();
  const fileRef = useRef<HTMLInputElement>(null);

  const [tab, setTab] = useState<Tab>("resume");
  const [uploading, setUploading] = useState(false);
  const [parseResult, setParseResult] = useState<ParseResult>(DEMO ? DEMO_PARSE : null);
  const [uploadError, setUploadError] = useState<string | null>(null);

  const [jdText, setJdText] = useState("");
  const [scanning, setScanning] = useState(false);
  const [scanResult, setScanResult] = useState<Record<string, number> | null>(
    DEMO ? { jd_match: 35, ats_safety: 14, evidence: 10, completeness: 6, interview: 5, hygiene: 3 } : null
  );

  async function handleUpload(file: File) {
    if (!auth?.token) return;
    setUploading(true);
    setUploadError(null);
    try {
      if (DEMO) {
        await new Promise(r => setTimeout(r, 900));
        setParseResult(DEMO_PARSE);
        setTab("readiness");
        return;
      }
      setParseResult(await uploadResume(auth.token, file));
      setTab("readiness");
    } catch (err) {
      setUploadError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setUploading(false);
    }
  }

  async function handleScan() {
    if (!jdText.trim() || !parseResult) return;
    setScanning(true);
    try {
      if (DEMO) {
        await new Promise(r => setTimeout(r, 1200));
        setScanResult({ jd_match: 31, ats_safety: 14, evidence: 10, completeness: 6, interview: 5, hygiene: 3 });
        return;
      }
      // Real: call /scorecards/score when match-engine is live (Week 2)
      setScanResult({ jd_match: 0, ats_safety: 0, evidence: 0, completeness: 0, interview: 0, hygiene: 0 });
    } finally {
      setScanning(false);
    }
  }

  const totalScore = scanResult
    ? Object.values(scanResult).reduce((a, b) => a + b, 0)
    : null;

  function bucket(score: number) {
    if (score >= 85) return { label: "Strong", cls: "bucket-strong" };
    if (score >= 70) return { label: "Ready", cls: "bucket-ready" };
    if (score >= 50) return { label: "Borderline", cls: "bucket-borderline" };
    return { label: "High Risk", cls: "bucket-risk" };
  }

  return (
    <div className="page-canvas">
      {/* Header */}
      <div className="page-title-row">
        <div>
          <h1 className="page-title">Resume & ATS Engine</h1>
          <p className="page-subtitle">Optimize and validate your profile against global ATS standards.</p>
        </div>
        {DEMO && <span className="chip chip-primary" style={{ fontFamily: "var(--font-mono)", fontSize: "0.72rem" }}>Demo Mode</span>}
      </div>

      {/* Tabs */}
      <div style={{ display: "flex", gap: 2, borderBottom: "1px solid rgba(192,199,211,0.4)", marginBottom: 24 }} role="tablist">
        {([ ["resume", "Document Intelligence"], ["scan", "JD Match Scan"], ["readiness", "Readiness Snapshot"] ] as [Tab, string][]).map(([t, label]) => (
          <button
            key={t}
            type="button"
            role="tab"
            aria-selected={tab === t}
            onClick={() => setTab(t)}
            style={{
              padding: "10px 18px",
              border: "none",
              borderBottom: tab === t ? "2px solid #0071c5" : "2px solid transparent",
              background: "transparent",
              color: tab === t ? "#0071c5" : "#414752",
              fontWeight: 600,
              fontSize: "0.88rem",
              cursor: "pointer",
              transition: "color 0.12s, border-color 0.12s",
              borderRadius: "0",
            }}
          >
            {label}
          </button>
        ))}
      </div>

      {/* Tab: Document Intelligence */}
      {tab === "resume" && (
        <div style={{ display: "grid", gridTemplateColumns: "1fr 300px", gap: 20, alignItems: "start" }}>
          <div className="content-card">
            <div className="content-card-header">
              <h2 className="content-card-title">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0071c5" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" /><polyline points="14 2 14 8 20 8" />
                </svg>
                Document Intelligence
              </h2>
              {parseResult && (
                <span className="chip chip-mono">{parseResult.char_count.toLocaleString()} chars · {parseResult.sections.length} sections</span>
              )}
            </div>
            <div className="content-card-body">
              {/* Upload zone */}
              {!parseResult ? (
                <div>
                  <div
                    onClick={() => fileRef.current?.click()}
                    onDragOver={e => e.preventDefault()}
                    onDrop={e => { e.preventDefault(); const f = e.dataTransfer.files[0]; if (f) handleUpload(f); }}
                    style={{
                      border: "2px dashed #c0c7d3", borderRadius: 12, padding: "48px 24px", textAlign: "center",
                      cursor: "pointer", transition: "border-color 0.15s, background 0.15s", background: "#f7f9fc",
                    }}
                    role="button"
                    aria-label="Upload resume — click or drag and drop"
                    tabIndex={0}
                    onKeyDown={e => e.key === "Enter" && fileRef.current?.click()}
                  >
                    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#0071c5" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" style={{ margin: "0 auto 14px", display: "block" }}>
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" /><polyline points="17 8 12 3 7 8" /><line x1="12" y1="3" x2="12" y2="15" />
                    </svg>
                    <p style={{ fontWeight: 700, color: "#191c1e", marginBottom: 6 }}>
                      {uploading ? "Parsing…" : "Drop your resume here"}
                    </p>
                    <p style={{ fontSize: "0.82rem", color: "#717783" }}>PDF or DOCX · max 5 MB</p>
                    {DEMO && <p style={{ marginTop: 10, fontSize: "0.78rem", color: "#0071c5", fontWeight: 600 }}>Demo: click to load sample resume data</p>}
                  </div>
                  <input
                    ref={fileRef}
                    type="file"
                    accept=".pdf,.docx"
                    className="file-input-hidden"
                    aria-label="Resume file upload"
                    onChange={e => { const f = e.target.files?.[0]; if (f) handleUpload(f); }}
                  />
                  {uploadError && <p style={{ color: "#ba1a1a", marginTop: 10, fontSize: "0.84rem" }}>{uploadError}</p>}
                </div>
              ) : (
                <div>
                  {/* ATS warnings */}
                  {parseResult.ats_flags.length > 0 && (
                    <div style={{ background: "#ffdad6", border: "1px solid rgba(186,26,26,0.2)", borderRadius: 8, padding: "12px 16px", marginBottom: 16, display: "flex", gap: 10 }}>
                      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#ba1a1a" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ flexShrink: 0, marginTop: 1 }}>
                        <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" /><line x1="12" y1="9" x2="12" y2="13" /><line x1="12" y1="17" x2="12.01" y2="17" />
                      </svg>
                      <div>
                        <p style={{ fontFamily: "var(--font-mono)", fontSize: "0.7rem", fontWeight: 600, color: "#93000a", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: 8 }}>
                          Structural ATS Warnings ({parseResult.ats_flags.length})
                        </p>
                        {parseResult.ats_flags.map(f => (
                          <div key={f} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "5px 0", borderBottom: "1px solid rgba(186,26,26,0.1)", fontSize: "0.86rem", color: "#191c1e" }}>
                            <span>{f}</span>
                            <span style={{ background: "rgba(186,26,26,0.1)", color: "#ba1a1a", borderRadius: 4, padding: "2px 7px", fontSize: "0.72rem", fontWeight: 700, flexShrink: 0 }}>HIGH RISK</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Extracted sections */}
                  <p style={{ fontFamily: "var(--font-mono)", fontSize: "0.7rem", fontWeight: 500, color: "#717783", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: 10, borderBottom: "1px solid rgba(192,199,211,0.3)", paddingBottom: 8 }}>
                    Extracted Taxonomy
                  </p>
                  <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
                    {parseResult.sections.map(s => (
                      <div key={s.section_name} style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "10px 14px", background: "#f7f9fc", borderRadius: 8, border: "1px solid rgba(192,199,211,0.3)", transition: "background 0.1s" }}>
                        <div>
                          <p style={{ fontWeight: 600, fontSize: "0.88rem", color: "#191c1e", margin: 0 }}>{s.section_name}</p>
                          {typeof s.content_json.cgpa === "string" && <p style={{ fontFamily: "var(--font-mono)", fontSize: "0.72rem", color: "#717783", margin: "3px 0 0" }}>CGPA: {s.content_json.cgpa}</p>}
                        </div>
                        <span style={{ fontFamily: "var(--font-mono)", fontSize: "0.68rem", fontWeight: 600, background: "rgba(0,88,156,0.1)", color: "#00589c", borderRadius: 4, padding: "2px 8px", border: "1px solid rgba(0,88,156,0.15)", flexShrink: 0 }}>
                          {Math.round(s.confidence * 100)}% CONF
                        </span>
                      </div>
                    ))}
                  </div>

                  <button
                    type="button"
                    onClick={() => { setParseResult(null); setTab("resume"); }}
                    style={{ marginTop: 16, padding: "8px 16px", borderRadius: 8, background: "transparent", border: "1px solid #c0c7d3", color: "#414752", cursor: "pointer", fontSize: "0.84rem", fontWeight: 600 }}
                  >
                    Replace resume
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* Generation matrix sidebar */}
          <div className="content-card">
            <div className="content-card-header">
              <h2 className="content-card-title">Generation Matrix</h2>
            </div>
            <div className="content-card-body">
              <label className="auth-label" htmlFor="template-select">Template Architecture</label>
              <select id="template-select" className="auth-input" style={{ paddingLeft: 14, marginBottom: 16 }}>
                <option>Classic ATS (Single Column)</option>
                <option>Technical / Developer</option>
                <option>Fresher Graduate</option>
              </select>
              <div style={{ background: "#f2f4f7", borderRadius: 8, border: "1px solid rgba(192,199,211,0.3)", padding: 12, fontFamily: "var(--font-mono)", fontSize: "0.72rem", color: "#717783", lineHeight: 1.7, marginBottom: 16, height: 100, overflow: "hidden", position: "relative" }}>
                JOHN DOE<br />software engineer<br /><br />SUMMARY<br />results-driven developer…<br /><br />SKILLS<br />python, javascript, react…
                <div style={{ position: "absolute", bottom: 0, left: 0, right: 0, height: 30, background: "linear-gradient(transparent, #f2f4f7)" }} />
              </div>
              <button type="button" style={{ width: "100%", padding: "10px", borderRadius: 8, background: "#0071c5", border: "1px solid #0071c5", color: "#fff", fontWeight: 600, cursor: "pointer", marginBottom: 8 }}>
                Generate Document
              </button>
              <div style={{ display: "flex", gap: 8 }}>
                <button type="button" style={{ flex: 1, padding: "8px", borderRadius: 8, background: "transparent", border: "1px solid #c0c7d3", color: "#00589c", fontWeight: 600, cursor: "pointer", fontSize: "0.84rem" }}>
                  Queue PDF
                </button>
                <button type="button" style={{ padding: "8px 12px", borderRadius: 8, background: "transparent", border: "1px solid #c0c7d3", color: "#414752", cursor: "pointer" }}>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" /><polyline points="7 10 12 15 17 10" /><line x1="12" y1="15" x2="12" y2="3" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab: JD Match Scan */}
      {tab === "scan" && (
        <div className="content-card">
          <div className="content-card-header">
            <h2 className="content-card-title">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0071c5" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
              </svg>
              Job Description Match
            </h2>
          </div>
          <div className="content-card-body">
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24 }}>
              {/* Input */}
              <div>
                <p style={{ fontSize: "0.88rem", color: "#414752", marginBottom: 12 }}>
                  Paste the target Job Description to run semantic similarity and keyword density checks.
                </p>
                {!parseResult && (
                  <div style={{ background: "#fef3c7", border: "1px solid rgba(217,119,6,0.25)", borderRadius: 8, padding: "10px 14px", marginBottom: 14, fontSize: "0.84rem", color: "#92400e" }}>
                    Upload your resume first on the Document Intelligence tab.
                  </div>
                )}
                <textarea
                  value={jdText}
                  onChange={e => setJdText(e.target.value)}
                  placeholder="Paste JD here…"
                  style={{ width: "100%", minHeight: 160, padding: "12px 14px", border: "1.5px solid #c0c7d3", borderRadius: 8, fontFamily: "var(--font-body)", fontSize: "0.88rem", resize: "vertical", outline: "none", background: "#f7f9fc" }}
                />
                <button
                  type="button"
                  onClick={handleScan}
                  disabled={scanning || !jdText.trim() || !parseResult}
                  style={{ marginTop: 12, padding: "12px 28px", borderRadius: 8, background: "#0071c5", border: "none", color: "#fff", fontWeight: 600, cursor: "pointer", opacity: (!jdText.trim() || !parseResult) ? 0.5 : 1 }}
                >
                  {scanning ? "Scanning…" : "Run ATS Scan"}
                </button>
                {DEMO && (
                  <p style={{ marginTop: 8, fontSize: "0.78rem", color: "#0071c5" }}>Demo: click Run ATS Scan to see simulated score</p>
                )}
              </div>

              {/* Score grid */}
              <div>
                <p style={{ fontFamily: "var(--font-mono)", fontSize: "0.7rem", fontWeight: 500, color: "#717783", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: 12, borderBottom: "1px solid rgba(192,199,211,0.3)", paddingBottom: 8 }}>
                  Diagnostic Results
                </p>
                {scanResult ? (
                  <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                    {SCORE_COMPONENTS.map(sc => {
                      const val = scanResult[sc.key] ?? 0;
                      return (
                        <div key={sc.key} style={{ display: "flex", alignItems: "center", gap: 10 }}>
                          <span style={{ fontSize: "0.8rem", color: "#414752", width: 170, flexShrink: 0 }}>{sc.label} <span style={{ color: "#717783", fontSize: "0.72rem" }}>({sc.weight})</span></span>
                          <div style={{ flex: 1, height: 6, background: "#e6e8eb", borderRadius: 9999, overflow: "hidden" }}>
                            <div style={{ height: "100%", width: `${val}%`, background: sc.color, borderRadius: 9999, transition: "width 0.6s ease" }} />
                          </div>
                          <span style={{ fontFamily: "var(--font-mono)", fontSize: "0.75rem", fontWeight: 600, color: sc.color, width: 28, textAlign: "right" }}>{val}</span>
                        </div>
                      );
                    })}
                    {totalScore !== null && (
                      <div style={{ marginTop: 12, padding: "14px 16px", background: "#f7f9fc", borderRadius: 10, border: "1px solid rgba(192,199,211,0.3)", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                        <span style={{ fontWeight: 700, color: "#191c1e" }}>Composite Score</span>
                        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                          <span style={{ fontFamily: "var(--font-display)", fontSize: "1.6rem", fontWeight: 800, color: "#0071c5" }}>{totalScore}</span>
                          <span className={`bucket-badge ${bucket(totalScore).cls}`}>{bucket(totalScore).label}</span>
                        </div>
                      </div>
                    )}
                  </div>
                ) : (
                  <div style={{ padding: "32px", textAlign: "center", color: "#717783", fontSize: "0.88rem" }}>
                    Score will appear here after scanning.
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab: Readiness Snapshot */}
      {tab === "readiness" && (
        <div>
          {!parseResult ? (
            <div className="content-card">
              <div className="content-card-body" style={{ textAlign: "center", padding: "48px 24px" }}>
                <p style={{ color: "#717783", marginBottom: 16 }}>Upload your resume to see your readiness snapshot.</p>
                <button type="button" onClick={() => setTab("resume")} style={{ padding: "12px 24px", borderRadius: 8, background: "#0071c5", border: "none", color: "#fff", fontWeight: 600, cursor: "pointer" }}>
                  Go to Document Intelligence
                </button>
              </div>
            </div>
          ) : (
            <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
              {/* AI Insight panel (glassmorphism) */}
              <div className="intel-panel">
                <div className="intel-panel-header">
                  <p className="intel-panel-sub">AI Diagnostic · Proof-linked analysis</p>
                  <h2 className="intel-panel-title">Placement Readiness Snapshot</h2>
                </div>
                <div className="intel-panel-body">
                  {scanResult ? (
                    <div style={{ display: "grid", gridTemplateColumns: "auto 1fr", gap: 24, alignItems: "center" }}>
                      <div style={{ textAlign: "center" }}>
                        <div style={{ fontFamily: "var(--font-display)", fontSize: "3rem", fontWeight: 800, color: "#0071c5", lineHeight: 1 }}>{totalScore}</div>
                        <span className={`bucket-badge ${bucket(totalScore!).cls}`} style={{ marginTop: 8, display: "inline-flex" }}>{bucket(totalScore!).label}</span>
                      </div>
                      <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
                        {SCORE_COMPONENTS.map(sc => (
                          <div key={sc.key} style={{ display: "flex", alignItems: "center", gap: 10 }}>
                            <span style={{ fontSize: "0.78rem", color: "#414752", width: 160, flexShrink: 0 }}>{sc.label}</span>
                            <div className="prog-bar" style={{ flex: 1 }}>
                              <div className="prog-bar-fill" style={{ width: `${(scanResult[sc.key] ?? 0)}%`, background: sc.color }} />
                            </div>
                            <span style={{ fontFamily: "var(--font-mono)", fontSize: "0.72rem", color: sc.color, width: 24, textAlign: "right" }}>{scanResult[sc.key] ?? 0}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  ) : (
                    <div style={{ textAlign: "center", padding: "12px 0" }}>
                      <p style={{ color: "rgba(255,255,255,0.7)", marginBottom: 12, fontSize: "0.88rem" }}>Run the JD Match Scan to see your full score breakdown.</p>
                      <button type="button" onClick={() => setTab("scan")} style={{ padding: "10px 20px", borderRadius: 8, background: "rgba(255,255,255,0.2)", border: "1px solid rgba(255,255,255,0.3)", color: "#fff", fontWeight: 600, cursor: "pointer" }}>
                        Go to JD Match Scan
                      </button>
                    </div>
                  )}
                </div>
              </div>

              {/* Parsed sections summary */}
              <div className="content-card">
                <div className="content-card-header">
                  <h2 className="content-card-title">Extracted Profile Summary</h2>
                  <span className="chip chip-success">{parseResult.sections.length} sections extracted</span>
                </div>
                <div className="content-card-body">
                  <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))", gap: 12 }}>
                    {parseResult.sections.map(s => (
                      <div key={s.section_name} style={{ padding: "12px 14px", background: "#f7f9fc", borderRadius: 8, border: "1px solid rgba(192,199,211,0.3)" }}>
                        <p style={{ fontWeight: 700, fontSize: "0.88rem", color: "#191c1e", marginBottom: 4 }}>{s.section_name}</p>
                        <p style={{ fontFamily: "var(--font-mono)", fontSize: "0.7rem", color: "#0071c5" }}>{Math.round(s.confidence * 100)}% confidence</p>
                      </div>
                    ))}
                  </div>
                  {parseResult.ats_flags.length > 0 && (
                    <div style={{ marginTop: 16, padding: "12px 16px", background: "#ffdad6", borderRadius: 8, border: "1px solid rgba(186,26,26,0.2)" }}>
                      <p style={{ fontFamily: "var(--font-mono)", fontSize: "0.7rem", fontWeight: 600, color: "#93000a", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: 6 }}>
                        ATS Risk Flags
                      </p>
                      {parseResult.ats_flags.map(f => (
                        <p key={f} style={{ fontSize: "0.84rem", color: "#191c1e", margin: "4px 0" }}>• {f}</p>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
