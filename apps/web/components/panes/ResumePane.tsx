"use client";

import { useRef } from "react";
import { History, ParseResult, ProfileState, Scan, StateSetter } from "./types";
import { ResumeBuilderCard } from "./sections/ResumeBuilderCard";
import { AtsScanCard } from "./sections/AtsScanCard";
import { CardSection } from "../ui/primitives";

type Props = {
  template: string;
  setTemplate: StateSetter<string>;
  profile: ProfileState;
  setProfile: StateSetter<ProfileState>;
  onGenerateResume: () => Promise<void>;
  preview: string;
  resumeText: string;
  onExportResume: () => Promise<void>;
  checkExport: () => Promise<void>;
  exportJobId: number | null;
  exportStatus: string;
  downloadExport: () => Promise<void>;
  jdText: string;
  setJdText: StateSetter<string>;
  onScan: () => Promise<void>;
  scan: Scan;
  history: History[];
  onUploadResume: (file: File) => Promise<void>;
  uploading: boolean;
  parseResult: ParseResult;
};

const SECTION_LABELS: Record<string, string> = {
  summary: "Summary / Objective",
  education: "Education",
  experience: "Experience / Internships",
  projects: "Projects",
  skills: "Skills",
  certifications: "Certifications",
  achievements: "Achievements",
  positions_of_responsibility: "Positions of Responsibility",
  links: "Links / Profiles",
  header: "Header Info",
};

const FLAG_MESSAGES: Record<string, string> = {
  file_too_large: "File exceeds safe ATS size limit",
  table_detected: "Table layout detected — may not parse in some ATS systems",
  tab_heavy_may_be_multi_column: "Possible multi-column layout — ATS risk",
  no_email_found: "No email address found in resume",
  missing_standard_headings: "Standard section headings not detected",
  possible_image_content: "Image/photo content detected — ATS cannot read images",
  likely_scanned_resume_ocr_fallback_needed: "Scanned resume — text extraction limited",
  table_content_detected_may_affect_ats: "Table used for content — may cause ATS parsing issues",
};

export function ResumePane({
  template,
  setTemplate,
  profile,
  setProfile,
  onGenerateResume,
  preview,
  resumeText,
  onExportResume,
  checkExport,
  exportJobId,
  exportStatus,
  downloadExport,
  jdText,
  setJdText,
  onScan,
  scan,
  history,
  onUploadResume,
  uploading,
  parseResult,
}: Props) {
  const fileInputRef = useRef<HTMLInputElement>(null);

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (file) onUploadResume(file);
    e.target.value = "";
  }

  return (
    <div className="grid pane-grid">
      {/* ── Upload + Parse Card ────────────────────────────────────────── */}
      <CardSection title="Upload Resume (PDF / DOCX)">
        <p className="muted">
          Upload your resume to extract sections and detect ATS parse-safety
          issues before running a JD match.
        </p>

        <div className="row">
          <label htmlFor="resume-file-input">
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              disabled={uploading}
            >
              {uploading ? "Parsing…" : "Choose file"}
            </button>
          </label>
          <input
            id="resume-file-input"
            ref={fileInputRef}
            type="file"
            accept=".pdf,.docx"
            className="file-input-hidden"
            aria-label="Upload resume PDF or DOCX"
            onChange={handleFileChange}
          />
        </div>

        {parseResult && (
          <>
            <p className="parse-meta">
              Parsed {parseResult.char_count.toLocaleString()} characters ·{" "}
              {parseResult.sections.length} sections ·{" "}
              {parseResult.source_format.toUpperCase()}
            </p>

            {parseResult.ats_flags.length > 0 && (
              <div className="ats-flags">
                <strong>ATS Parse-Safety Issues</strong>
                <ul>
                  {parseResult.ats_flags.map((flag) => (
                    <li key={flag}>⚠ {FLAG_MESSAGES[flag] ?? flag}</li>
                  ))}
                </ul>
              </div>
            )}

            <div className="section-list">
              <strong>Extracted Sections</strong>
              {parseResult.sections.map((sec) => {
                const raw = (sec.content_json as { raw?: string })?.raw ?? "";
                const label = SECTION_LABELS[sec.section_name] ?? sec.section_name;
                const pct = Math.round(sec.confidence * 100);
                return (
                  <details key={sec.section_name} className="section-item">
                    <summary>
                      {label}
                      <span className="section-confidence">{pct}% confidence</span>
                    </summary>
                    <pre className="section-content">{raw || "(empty)"}</pre>
                  </details>
                );
              })}
            </div>

            {parseResult.parse_warnings.length > 0 && (
              <p className="parse-warnings">
                Parser notes: {parseResult.parse_warnings.join(" · ")}
              </p>
            )}
          </>
        )}
      </CardSection>

      {/* ── Existing Cards ────────────────────────────────────────────── */}
      <ResumeBuilderCard
        template={template}
        setTemplate={setTemplate}
        profile={profile}
        setProfile={setProfile}
        onGenerateResume={onGenerateResume}
        preview={preview}
        resumeText={resumeText}
        onExportResume={onExportResume}
        checkExport={checkExport}
        exportJobId={exportJobId}
        exportStatus={exportStatus}
        downloadExport={downloadExport}
      />
      <AtsScanCard
        jdText={jdText}
        setJdText={setJdText}
        onScan={onScan}
        scan={scan}
        history={history}
      />
    </div>
  );
}
