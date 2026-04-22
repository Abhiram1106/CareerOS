import { NexusApp, NexusCandidate, NexusCandidateFormState, NexusEvent, StateSetter } from "../types";
import { CardSection, FormField } from "../../ui/primitives";

type Props = {
  nexusCandidateForm: NexusCandidateFormState;
  setNexusCandidateForm: StateSetter<NexusCandidateFormState>;
  onCreateNexusCandidate: () => Promise<void>;
  refreshNexusCandidates: () => Promise<void>;
  nexusCandidates: NexusCandidate[];
  onCreateNexusApplication: () => Promise<void>;
  refreshNexusApps: () => Promise<void>;
  nexusApps: NexusApp[];
  onMoveNexusAppStage: (appId: string) => Promise<void>;
  onRunNexusAiMatch: () => Promise<void>;
  nexusMatchResult: { score: number; top_strengths: string[]; gaps: string[] } | null;
  onCreateNexusInterview: () => Promise<void>;
  onSubmitNexusScorecard: () => Promise<void>;
  onCreateNexusOffer: () => Promise<void>;
  onSendNexusOffer: () => Promise<void>;
  refreshNexusEvents: () => Promise<void>;
  latestInterviewId: string;
  latestOfferId: string;
  nexusEvents: NexusEvent[];
};

export function NexusPipelineCard({
  nexusCandidateForm,
  setNexusCandidateForm,
  onCreateNexusCandidate,
  refreshNexusCandidates,
  nexusCandidates,
  onCreateNexusApplication,
  refreshNexusApps,
  nexusApps,
  onMoveNexusAppStage,
  onRunNexusAiMatch,
  nexusMatchResult,
  onCreateNexusInterview,
  onSubmitNexusScorecard,
  onCreateNexusOffer,
  onSendNexusOffer,
  refreshNexusEvents,
  latestInterviewId,
  latestOfferId,
  nexusEvents,
}: Props) {
  return (
    <CardSection title="NEXUS Candidates + Pipeline">
      <FormField label="Candidate Name"><input value={nexusCandidateForm.full_name} onChange={(e) => setNexusCandidateForm({ ...nexusCandidateForm, full_name: e.target.value })} /></FormField>
      <FormField label="Candidate Email"><input value={nexusCandidateForm.email} onChange={(e) => setNexusCandidateForm({ ...nexusCandidateForm, email: e.target.value })} /></FormField>
      <FormField label="Skills CSV"><input value={nexusCandidateForm.skills_csv} onChange={(e) => setNexusCandidateForm({ ...nexusCandidateForm, skills_csv: e.target.value })} /></FormField>
      <div className="row">
        <button onClick={onCreateNexusCandidate}>Upsert Candidate</button>
        <button onClick={refreshNexusCandidates}>Refresh Candidates</button>
      </div>
      {nexusCandidates.slice(0, 5).map((c) => <p key={c.id} className="muted">{c.full_name} | {c.email} | {c.skills_csv}</p>)}
      <div className="row" style={{ marginTop: 10 }}>
        <button onClick={onCreateNexusApplication}>Create Application (top candidate to top requisition)</button>
        <button onClick={refreshNexusApps}>Refresh Applications</button>
      </div>
      {nexusApps.slice(0, 5).map((a) => (
        <p key={a.id} className="muted">
          {a.id.slice(0, 8)} | {a.stage_name} | {a.status} | match {a.match_score}
          <button onClick={() => onMoveNexusAppStage(a.id)}>Move to Interview</button>
        </p>
      ))}
      <div className="row" style={{ marginTop: 10 }}>
        <button onClick={onRunNexusAiMatch}>Run AI Match (top candidate vs top requisition)</button>
      </div>
      {nexusMatchResult ? <p className="muted">Score {nexusMatchResult.score} | strengths: {nexusMatchResult.top_strengths.join(", ")} | gaps: {nexusMatchResult.gaps.join(", ")}</p> : null}
      <div className="row" style={{ marginTop: 10 }}>
        <button onClick={onCreateNexusInterview}>Schedule Interview (top application)</button>
        <button onClick={onSubmitNexusScorecard}>Submit Scorecard</button>
      </div>
      <div className="row" style={{ marginTop: 10 }}>
        <button onClick={onCreateNexusOffer}>Create Offer</button>
        <button onClick={onSendNexusOffer}>Send Offer</button>
        <button onClick={refreshNexusEvents}>Refresh ATS Events</button>
      </div>
      {latestInterviewId ? <p className="muted">Latest interview: {latestInterviewId}</p> : null}
      {latestOfferId ? <p className="muted">Latest offer: {latestOfferId}</p> : null}
      <h3>ATS Event Feed</h3>
      {nexusEvents.slice(0, 8).map((e) => <p key={e.id} className="muted">{e.event_name} | {new Date(e.created_at).toLocaleString()}</p>)}
    </CardSection>
  );
}
