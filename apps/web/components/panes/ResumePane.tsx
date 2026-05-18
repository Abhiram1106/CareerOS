import { History, ProfileState, Scan, StateSetter } from "./types";
import { ResumeBuilderCard } from "./sections/ResumeBuilderCard";
import { AtsScanCard } from "./sections/AtsScanCard";

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
}: Props) {
  return (
    <div className="grid pane-grid">
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
      <AtsScanCard jdText={jdText} setJdText={setJdText} onScan={onScan} scan={scan} history={history} />
    </div>
  );
}
