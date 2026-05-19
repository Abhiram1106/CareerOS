"use client";

import { useState } from "react";
import { SectionNav } from "../components/SectionNav";
import { AccountPane } from "../components/panes/AccountPane";
import { ResumePane } from "../components/panes/ResumePane";
import { JobsPane } from "../components/panes/JobsPane";
import { ActivePane } from "../components/panes/types";
import { useCareerOSWorkspace } from "../hooks/useCareerOSWorkspace";

export default function Page() {
  const [activePane, setActivePane] = useState<ActivePane>("account");
  const workspace = useCareerOSWorkspace();

  return (
    <main>
      <div className="top">
        <div>
          <h1>CareerOS Campus AI</h1>
          <p className="muted">Placement-readiness console — profile, resume, ATS scoring</p>
        </div>
        <strong>{workspace.status}</strong>
      </div>

      <SectionNav activePane={activePane} onChange={setActivePane} />

      {activePane === "account" ? <p className="pane-title">Identity + profile setup</p> : null}
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

      {activePane === "resume" ? <p className="pane-title">Resume generation and ATS scoring</p> : null}
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

      {activePane === "jobs" ? <p className="pane-title">Placement readiness snapshot</p> : null}
      {activePane === "jobs" ? (
        <JobsPane
          dashboard={workspace.dashboard}
          refreshDashboard={workspace.refreshDashboard}
        />
      ) : null}
    </main>
  );
}
