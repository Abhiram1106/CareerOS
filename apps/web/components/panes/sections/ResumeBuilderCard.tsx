import { ProfileState, StateSetter } from "../types";
import { CardSection, FormField } from "../../ui/primitives";

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
};

export function ResumeBuilderCard({
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
}: Props) {
  return (
    <CardSection
      title="Resume Builder"
      subtitle="Generate an ATS-safe resume from your profile, or upload a PDF/DOCX above."
    >
      <FormField label="Template">
        <select value={template} onChange={(e) => setTemplate(e.target.value)}>
          <option value="classic">Classic ATS</option>
          <option value="tech">Technical</option>
          <option value="fresher">Fresher</option>
        </select>
      </FormField>

      <div className="row">
        <button
          type="button"
          className="btn-secondary btn-compact"
          onClick={() =>
            setProfile({
              ...profile,
              summary: "Results-oriented engineer with strong backend and cloud foundation.",
              experience_bullet: "Built and shipped feature modules that improved conversion by 28%.",
            })
          }
        >
          Autofill sample content
        </button>
        <button type="button" onClick={onGenerateResume}>
          Generate resume
        </button>
      </div>

      {preview && (
        <>
          <p className="card-subtitle muted builder-section-label">Preview</p>
          <pre>{preview}</pre>
        </>
      )}

      {resumeText && (
        <>
          <p className="card-subtitle muted builder-section-label">Generated resume</p>
          <pre>{resumeText}</pre>
        </>
      )}

      <div className="row builder-export-row">
        <button type="button" className="btn-secondary btn-compact" onClick={onExportResume}>
          Queue PDF export
        </button>
        <button type="button" className="btn-ghost btn-compact" onClick={checkExport}>
          Check status
        </button>
      </div>

      {exportJobId ? (
        <p className="muted builder-export-status">
          Export #{exportJobId}: {exportStatus || "queued"}
          {exportStatus === "completed" ? (
            <button type="button" className="btn-ghost btn-sm" onClick={downloadExport}>
              Download ↓
            </button>
          ) : null}
        </p>
      ) : null}
    </CardSection>
  );
}
