import { AssistantPanel } from "../../../components/workspace/AssistantPanel";

export default function AssistantPage() {
  return (
    <div className="page-canvas">
      <div className="page-title-row">
        <div>
          <h1 className="page-title">Assistant</h1>
          <p className="page-subtitle">Grounded guidance based on product FAQ and your recent scoring context.</p>
        </div>
      </div>
      <AssistantPanel />
    </div>
  );
}
