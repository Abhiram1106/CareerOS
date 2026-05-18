"use client";

import { useState } from "react";
import { SectionNav } from "../components/SectionNav";
import { AccountPane } from "../components/panes/AccountPane";
import { ResumePane } from "../components/panes/ResumePane";
import { NexusPane } from "../components/panes/NexusPane";
import { JobsPane } from "../components/panes/JobsPane";
import { BillingPane } from "../components/panes/BillingPane";
import { ActivePane } from "../components/panes/types";
import { useCareerOSWorkspace } from "../hooks/useCareerOSWorkspace";

export default function Page() {
  const [activePane, setActivePane] = useState<ActivePane>("account");
  const workspace = useCareerOSWorkspace();

  return (
    <main>
      <div className="top">
        <div>
          <h1>CareerOS Workspace</h1>
          <p className="muted">Clean console for profile, resume, ATS, jobs, payments, and NEXUS workflows</p>
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
        />
      ) : null}

      {activePane === "nexus" ? <p className="pane-title">Hiring pipeline operations</p> : null}
      {activePane === "nexus" ? (
        <NexusPane
          nexusReqForm={workspace.nexusReqForm}
          setNexusReqForm={workspace.setNexusReqForm}
          onCreateNexusReq={workspace.onCreateNexusReq}
          refreshNexusReqs={workspace.refreshNexusReqs}
          nexusReqs={workspace.nexusReqs}
          nexusCandidateForm={workspace.nexusCandidateForm}
          setNexusCandidateForm={workspace.setNexusCandidateForm}
          onCreateNexusCandidate={workspace.onCreateNexusCandidate}
          refreshNexusCandidates={workspace.refreshNexusCandidates}
          nexusCandidates={workspace.nexusCandidates}
          onCreateNexusApplication={workspace.onCreateNexusApplication}
          refreshNexusApps={workspace.refreshNexusApps}
          nexusApps={workspace.nexusApps}
          onMoveNexusAppStage={workspace.onMoveNexusAppStage}
          onRunNexusAiMatch={workspace.onRunNexusAiMatch}
          nexusMatchResult={workspace.nexusMatchResult}
          onCreateNexusInterview={workspace.onCreateNexusInterview}
          onSubmitNexusScorecard={workspace.onSubmitNexusScorecard}
          onCreateNexusOffer={workspace.onCreateNexusOffer}
          onSendNexusOffer={workspace.onSendNexusOffer}
          refreshNexusEvents={workspace.refreshNexusEvents}
          latestInterviewId={workspace.latestInterviewId}
          latestOfferId={workspace.latestOfferId}
          nexusEvents={workspace.nexusEvents}
        />
      ) : null}

      {activePane === "jobs" ? <p className="pane-title">Matching, alerts, notifications, and application tracking</p> : null}
      {activePane === "jobs" ? (
        <JobsPane
          jobs={workspace.jobs}
          refreshJobs={workspace.refreshJobs}
          alertForm={workspace.alertForm}
          setAlertForm={workspace.setAlertForm}
          onCreateAlert={workspace.onCreateAlert}
          refreshAlerts={workspace.refreshAlerts}
          onDispatchAlerts={workspace.onDispatchAlerts}
          refreshNotifications={workspace.refreshNotifications}
          alerts={workspace.alerts}
          onDeleteAlert={workspace.onDeleteAlert}
          notifications={workspace.notifications}
          dashboard={workspace.dashboard}
          refreshDashboard={workspace.refreshDashboard}
          appForm={workspace.appForm}
          setAppForm={workspace.setAppForm}
          onCreateApplication={workspace.onCreateApplication}
          refreshApplications={workspace.refreshApplications}
          applications={workspace.applications}
          onDeleteApplication={workspace.onDeleteApplication}
        />
      ) : null}

      {activePane === "billing" ? <p className="pane-title">Plans, checkout, and roadmap visibility</p> : null}
      {activePane === "billing" ? (
        <BillingPane
          myPlan={workspace.myPlan}
          plans={workspace.plans}
          onSubscribe={workspace.onSubscribe}
          onCheckout={workspace.onCheckout}
        />
      ) : null}
    </main>
  );
}
