"use client";

import { useState } from "react";
import { AppFooter } from "../components/layout/AppFooter";
import { AppHeader } from "../components/layout/AppHeader";
import { HeroPage } from "../components/marketing/HeroPage";
import { AccountPane } from "../components/panes/AccountPane";
import { JobsPane } from "../components/panes/JobsPane";
import { ResumePane } from "../components/panes/ResumePane";
import { ActivePane, AppView } from "../components/panes/types";
import { WorkspaceTabs } from "../components/workspace/WorkspaceTabs";
import { useCareerOSWorkspace } from "../hooks/useCareerOSWorkspace";

export default function Page() {
  const [activeView, setActiveView] = useState<AppView>("overview");
  const [activePane, setActivePane] = useState<ActivePane>("account");
  const workspace = useCareerOSWorkspace();

  const openWorkspace = (pane?: ActivePane) => {
    if (pane) setActivePane(pane);
    setActiveView("workspace");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <>
      <AppHeader
        activeView={activeView}
        onViewChange={setActiveView}
        status={workspace.status}
        actions={
          activeView === "overview" ? (
            <button type="button" className="btn-secondary btn-compact" onClick={() => openWorkspace()}>
              Workspace
            </button>
          ) : null
        }
      />

      <main className="app-main">
        {activeView === "overview" ? <HeroPage onOpenWorkspace={() => openWorkspace()} /> : null}

        {activeView === "workspace" ? (
          <section className="workspace-shell" aria-label="Student workspace">
            <header className="workspace-header">
              <div>
                <h1>Student workspace</h1>
                <p className="muted">
                  Profile → resume pipeline → readiness snapshot. API:{" "}
                  <code className="inline-code">NEXT_PUBLIC_CORE_API_URL</code>
                </p>
              </div>
              <button type="button" className="btn-ghost btn-compact" onClick={() => setActiveView("overview")}>
                Back to overview
              </button>
            </header>

            <WorkspaceTabs activePane={activePane} onChange={setActivePane} />

            <div
              role="tabpanel"
              id={`panel-${activePane}`}
              aria-labelledby={`tab-${activePane}`}
              aria-describedby={`panel-${activePane}-desc`}
            >
              {activePane === "account" ? (
                <AccountPane
                  auth={workspace.auth}
                  setAuth={workspace.setAuth}
                  profile={workspace.profile}
                  setProfile={workspace.setProfile}
                  onRegister={workspace.onRegister}
                  onLogin={workspace.onLogin}
                  onSaveProfile={workspace.onSaveProfile}
                />
              ) : null}

              {activePane === "resume" ? (
                <ResumePane
                  template={workspace.template}
                  setTemplate={workspace.setTemplate}
                  profile={workspace.profile}
                  setProfile={workspace.setProfile}
                  onGenerateResume={workspace.onGenerateResume}
                  preview={workspace.preview}
                  resumeText={workspace.resumeText}
                  onExportResume={workspace.onExportResume}
                  checkExport={workspace.checkExport}
                  exportJobId={workspace.exportJobId}
                  exportStatus={workspace.exportStatus}
                  downloadExport={workspace.downloadExport}
                  jdText={workspace.jdText}
                  setJdText={workspace.setJdText}
                  onScan={workspace.onScan}
                  scan={workspace.scan}
                  history={workspace.history}
                  onUploadResume={workspace.onUploadResume}
                  uploading={workspace.uploading}
                  parseResult={workspace.parseResult}
                />
              ) : null}

              {activePane === "jobs" ? (
                <JobsPane dashboard={workspace.dashboard} refreshDashboard={workspace.refreshDashboard} />
              ) : null}
            </div>
          </section>
        ) : null}
      </main>

      <AppFooter />
    </>
  );
}
