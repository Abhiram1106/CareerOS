import { ActivePane } from "../panes/types";

type Props = {
  activePane: ActivePane;
  onChange: (pane: ActivePane) => void;
};

const TABS: { id: ActivePane; label: string; description: string }[] = [
  {
    id: "account",
    label: "Account",
    description: "Register, sign in, and complete your placement profile.",
  },
  {
    id: "resume",
    label: "Resume & ATS",
    description: "Upload, generate, export, and score resumes against job descriptions.",
  },
  {
    id: "jobs",
    label: "Readiness",
    description: "Snapshot metrics until the officer cohort dashboard ships in Week 4.",
  },
];

export function WorkspaceTabs({ activePane, onChange }: Props) {
  const active = TABS.find((tab) => tab.id === activePane) ?? TABS[0];

  return (
    <div className="workspace-tabs">
      <div className="workspace-tablist" role="tablist" aria-label="Workspace sections">
        {TABS.map((tab) => (
          <button
            key={tab.id}
            type="button"
            role="tab"
            id={`tab-${tab.id}`}
            aria-selected={activePane === tab.id}
            aria-controls={`panel-${tab.id}`}
            className={activePane === tab.id ? "workspace-tab active" : "workspace-tab"}
            onClick={() => onChange(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>
      <p className="workspace-tab-description" id={`panel-${active.id}-desc`}>
        {active.description}
      </p>
    </div>
  );
}
