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
    <CardSection title="Resume Builder">
      <FormField label="Template">
        <select value={template} onChange={(e) => setTemplate(e.target.value)}>
          <option value="classic">Classic ATS</option><option value="tech">Technical</option><option value="fresher">Fresher</option>
        </select>
      </FormField>
      <div className="row">
        <button onClick={() => setProfile({ ...profile, summary: "Results-oriented engineer with strong backend and cloud foundation.", experience_bullet: "Built and shipped feature modules that improved conversion by 28%." })}>Autofill Content</button>
        <button onClick={onGenerateResume}>Generate Resume</button>
      </div>
      <h3>Preview</h3>
      <pre>{preview}</pre>
      {resumeText ? (<><h3>Generated Resume</h3><pre>{resumeText}</pre></>) : null}
      <div className="row" style={{ marginTop: 10 }}>
        <button onClick={onExportResume}>Queue PDF Export</button>
        <button onClick={checkExport}>Check Export Status</button>
      </div>
      {exportJobId ? (
        <p className="muted">
          Export #{exportJobId}: {exportStatus || "queued"}{" "}
          {exportStatus === "completed" ? <button onClick={downloadExport}>Download</button> : null}
        </p>
      ) : null}
    </CardSection>
  );
}
