"use client";

import { useState } from "react";

import { getStoredAuth } from "../../lib/auth";
import { toErrorMessage } from "../../lib/errors";
import { createOfficerBatch, uploadOfficerBatch } from "../../modules/officer/services/officerService";

type OfficerBatchUploadProps = {
  onComplete: () => void;
};

export function OfficerBatchUpload({ onComplete }: OfficerBatchUploadProps) {
  const token = getStoredAuth()?.token ?? "";
  const [name, setName] = useState("");
  const [gradYear, setGradYear] = useState(2026);
  const [files, setFiles] = useState<File[]>([]);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const onSubmit = async () => {
    if (!token || !name.trim() || files.length === 0) return;
    setBusy(true);
    setError(null);
    setMessage(null);
    try {
      const created = await createOfficerBatch(token, { name: name.trim(), grad_year: gradYear });
      const result = await uploadOfficerBatch(token, created.batch.id, files);
      setMessage(`Uploaded ${result.uploaded} resume(s) to batch “${created.batch.name}”.`);
      if (result.errors.length) {
        setError(result.errors.join(" · "));
      }
      setName("");
      setFiles([]);
      onComplete();
    } catch (err) {
      setError(toErrorMessage(err, "Batch upload failed"));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="content-card">
      <div className="content-card-header">
        <h2 className="content-card-title">Batch intake</h2>
        <span className="chip chip-primary">PDF / DOCX</span>
      </div>
      <div className="content-card-body">
        <p style={{ fontSize: "0.84rem", color: "#414752", marginBottom: 12, lineHeight: 1.55 }}>
          Create a campus batch and upload resumes in one step. Each file becomes an intake student linked to the batch.
        </p>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 120px", gap: 8, marginBottom: 10 }}>
          <input
            className="auth-input"
            placeholder="Batch name (e.g. CSE 2026)"
            value={name}
            onChange={(e) => setName(e.target.value)}
            disabled={busy}
          />
          <input
            className="auth-input"
            type="number"
            min={2020}
            max={2035}
            value={gradYear}
            onChange={(e) => setGradYear(Number(e.target.value))}
            disabled={busy}
          />
        </div>
        <input
          type="file"
          accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
          multiple
          disabled={busy}
          onChange={(e) => setFiles(Array.from(e.target.files ?? []))}
        />
        {files.length > 0 ? (
          <p style={{ fontSize: "0.78rem", color: "#717783", marginTop: 8 }}>
            {files.length} file(s) selected
          </p>
        ) : null}
        <button
          type="button"
          className="btn-primary"
          style={{ marginTop: 12 }}
          disabled={busy || !name.trim() || files.length === 0}
          onClick={() => void onSubmit()}
        >
          {busy ? "Uploading…" : "Create batch & upload"}
        </button>
        {message ? <p style={{ fontSize: "0.82rem", color: "#16a34a", marginTop: 10 }}>{message}</p> : null}
        {error ? (
          <p className="workspace-error" role="alert" style={{ marginTop: 8 }}>
            {error}
          </p>
        ) : null}
      </div>
    </div>
  );
}
