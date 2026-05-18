import { History, Scan, StateSetter } from "../types";
import { CardSection, FormField, MetricTile } from "../../ui/primitives";

type Props = {
  jdText: string;
  setJdText: StateSetter<string>;
  onScan: () => Promise<void>;
  scan: Scan;
  history: History[];
};

export function AtsScanCard({ jdText, setJdText, onScan, scan, history }: Props) {
  return (
    <CardSection title="ATS Scan">
      <FormField label="Job Description"><textarea rows={6} value={jdText} onChange={(e) => setJdText(e.target.value)} /></FormField>
      <button onClick={onScan}>Run Scan</button>
      <div className="metric-grid" style={{ marginTop: 12 }}>
        <MetricTile label="Composite" value={scan?.composite ?? "-"} />
        <MetricTile label="Keyword" value={scan?.keyword ?? "-"} />
        <MetricTile label="Format" value={scan?.format ?? "-"} />
        <MetricTile label="Quality" value={scan?.quality ?? "-"} />
        <MetricTile label="Complete" value={scan?.complete ?? "-"} />
        <MetricTile label="Contact" value={scan?.contact ?? "-"} />
      </div>
      <h3>ATS History</h3>
      {history.slice(0, 5).map((h) => <p key={h.id} className="muted">#{h.id} | {h.composite_score} | {new Date(h.created_at).toLocaleString()}</p>)}
    </CardSection>
  );
}
