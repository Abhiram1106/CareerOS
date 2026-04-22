import {
  NexusApp,
  NexusCandidate,
  NexusCandidateFormState,
  NexusEvent,
  NexusReq,
  NexusReqFormState,
  StateSetter,
} from "./types";
import { NexusRequisitionCard } from "./sections/NexusRequisitionCard";
import { NexusPipelineCard } from "./sections/NexusPipelineCard";

type Props = {
  nexusReqForm: NexusReqFormState;
  setNexusReqForm: StateSetter<NexusReqFormState>;
  onCreateNexusReq: () => Promise<void>;
  refreshNexusReqs: () => Promise<void>;
  nexusReqs: NexusReq[];
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

export function NexusPane({
  nexusReqForm,
  setNexusReqForm,
  onCreateNexusReq,
  refreshNexusReqs,
  nexusReqs,
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
    <div className="grid pane-grid">
      <NexusRequisitionCard
        nexusReqForm={nexusReqForm}
        setNexusReqForm={setNexusReqForm}
        onCreateNexusReq={onCreateNexusReq}
        refreshNexusReqs={refreshNexusReqs}
        nexusReqs={nexusReqs}
      />
      <NexusPipelineCard
        nexusCandidateForm={nexusCandidateForm}
        setNexusCandidateForm={setNexusCandidateForm}
        onCreateNexusCandidate={onCreateNexusCandidate}
        refreshNexusCandidates={refreshNexusCandidates}
        nexusCandidates={nexusCandidates}
        onCreateNexusApplication={onCreateNexusApplication}
        refreshNexusApps={refreshNexusApps}
        nexusApps={nexusApps}
        onMoveNexusAppStage={onMoveNexusAppStage}
        onRunNexusAiMatch={onRunNexusAiMatch}
        nexusMatchResult={nexusMatchResult}
        onCreateNexusInterview={onCreateNexusInterview}
        onSubmitNexusScorecard={onSubmitNexusScorecard}
        onCreateNexusOffer={onCreateNexusOffer}
        onSendNexusOffer={onSendNexusOffer}
        refreshNexusEvents={refreshNexusEvents}
        latestInterviewId={latestInterviewId}
        latestOfferId={latestOfferId}
        nexusEvents={nexusEvents}
      />
    </div>
  );
}
