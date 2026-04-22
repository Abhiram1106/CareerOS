import { NexusReq, NexusReqFormState, StateSetter } from "../types";
import { CardSection, FormField } from "../../ui/primitives";

type Props = {
  nexusReqForm: NexusReqFormState;
  setNexusReqForm: StateSetter<NexusReqFormState>;
  onCreateNexusReq: () => Promise<void>;
  refreshNexusReqs: () => Promise<void>;
  nexusReqs: NexusReq[];
};

export function NexusRequisitionCard({ nexusReqForm, setNexusReqForm, onCreateNexusReq, refreshNexusReqs, nexusReqs }: Props) {
  return (
    <CardSection title="NEXUS ATS Workspace" subtitle="Built from your ATS folder blueprint (requisition to candidate to application).">
      <h3>Create Requisition</h3>
      <FormField label="Title"><input value={nexusReqForm.title} onChange={(e) => setNexusReqForm({ ...nexusReqForm, title: e.target.value })} /></FormField>
      <FormField label="Department"><input value={nexusReqForm.department} onChange={(e) => setNexusReqForm({ ...nexusReqForm, department: e.target.value })} /></FormField>
      <FormField label="Required Skills CSV"><input value={nexusReqForm.required_skills_csv} onChange={(e) => setNexusReqForm({ ...nexusReqForm, required_skills_csv: e.target.value })} /></FormField>
      <div className="row">
        <button onClick={onCreateNexusReq}>Create Requisition</button>
        <button onClick={refreshNexusReqs}>Refresh Requisitions</button>
      </div>
      {nexusReqs.slice(0, 5).map((r) => <p key={r.id} className="muted">{r.req_number} | {r.title} | {r.status} | active {r.active_candidate_count}</p>)}
    </CardSection>
  );
}
