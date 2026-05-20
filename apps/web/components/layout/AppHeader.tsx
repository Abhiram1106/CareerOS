import type { ReactNode } from "react";
import type { AppView } from "../panes/types";
import { SiteNav } from "./SiteNav";

type Props = {
  activeView: AppView;
  onViewChange: (view: AppView) => void;
  status: string;
  actions?: ReactNode;
};

export function AppHeader({ activeView, onViewChange, status, actions }: Props) {
  return (
    <header className="app-header">
      <div className="app-header-inner">
        {/* Brand */}
        <div className="brand-lockup">
          <span className="brand-mark" aria-hidden="true">C</span>
          <div className="brand-text">
            <strong>CareerOS</strong>
            <span>Campus AI</span>
          </div>
        </div>

        {/* Primary nav */}
        <SiteNav activeView={activeView} onChange={onViewChange} />

        {/* Right-side actions + status */}
        <div className="app-header-end">
          <span className="badge badge-intel" aria-label="Intel-optimized">
            ⚡ Intel
          </span>
          {actions}
          <span className="status-pill" role="status" aria-live="polite">
            {status}
          </span>
        </div>
      </div>
    </header>
  );
}
