"use client";

import { useRef } from "react";

type Props = {
  disabled: boolean;
  uploading: boolean;
  error: string | null;
  onFile: (file: File) => void;
};

export function ResumeDropzone({ disabled, uploading, error, onFile }: Props) {
  const inputRef = useRef<HTMLInputElement>(null);

  function pick(file: File | undefined) {
    if (file) onFile(file);
  }

  return (
    <div className="resume-dropzone-wrap">
      <div
        className={`resume-dropzone${disabled ? " resume-dropzone--disabled" : ""}`}
        role="button"
        tabIndex={disabled ? -1 : 0}
        aria-label="Upload resume — click or drag and drop"
        onClick={() => !disabled && !uploading && inputRef.current?.click()}
        onKeyDown={(e) => e.key === "Enter" && inputRef.current?.click()}
        onDragOver={(e) => e.preventDefault()}
        onDrop={(e) => {
          e.preventDefault();
          if (!disabled && !uploading) pick(e.dataTransfer.files[0]);
        }}
      >
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#0071c5" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" className="resume-dropzone-icon" aria-hidden="true">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
          <polyline points="17 8 12 3 7 8" />
          <line x1="12" y1="3" x2="12" y2="15" />
        </svg>
        <p className="resume-dropzone-title">{uploading ? "Parsing…" : "Drop your resume here"}</p>
        <p className="resume-dropzone-hint">PDF or DOCX · max 5 MB · resume-parser + ATS heuristics</p>
      </div>
      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.doc,.docx"
        disabled={disabled || uploading}
        className="file-input-hidden"
        aria-hidden="true"
        onChange={(e) => {
          pick(e.target.files?.[0]);
          e.target.value = "";
        }}
      />
      {error ? (
        <p className="workspace-error" role="alert">
          {error}
        </p>
      ) : null}
    </div>
  );
}
