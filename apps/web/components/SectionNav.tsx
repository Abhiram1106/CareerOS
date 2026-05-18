import { ActivePane } from "./panes/types";

type Props = {
  activePane: ActivePane;
  onChange: (pane: ActivePane) => void;
};

export function SectionNav({ activePane, onChange }: Props) {
  return (
    <div className="section-nav">
      <button className={activePane === "account" ? "active" : ""} onClick={() => onChange("account")}>Account</button>
      <button className={activePane === "resume" ? "active" : ""} onClick={() => onChange("resume")}>Resume & ATS</button>
      <button className={activePane === "jobs" ? "active" : ""} onClick={() => onChange("jobs")}>Jobs</button>
    </div>
  );
}
