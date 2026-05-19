import { ActivePane } from "./panes/types";

type Props = {
  activePane: ActivePane;
  onChange: (pane: ActivePane) => void;
};

/** @deprecated Use WorkspaceTabs — kept for any external imports during transition */
export function SectionNav({ activePane, onChange }: Props) {
  return (
    <div className="section-nav">
      <button
        type="button"
        className={activePane === "account" ? "active" : ""}
        onClick={() => onChange("account")}
      >
        Account
      </button>
      <button
        type="button"
        className={activePane === "resume" ? "active" : ""}
        onClick={() => onChange("resume")}
      >
        Resume & ATS
      </button>
      <button
        type="button"
        className={activePane === "jobs" ? "active" : ""}
        onClick={() => onChange("jobs")}
      >
        Jobs
      </button>
    </div>
  );
}
