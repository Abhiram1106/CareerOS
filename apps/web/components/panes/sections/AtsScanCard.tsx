import { History, Scan, StateSetter } from "../types";
import { CardSection, FormField, MetricTile } from "../../ui/primitives";

type Props = {
  jdText: string;
  setJdText: StateSetter<string>;
  onScan: () => Promise<void>;
  scan: Scan;
  history: History[];
};

function scoreVariant(val: number | string): "success" | "warn" | "danger" | "default" {
  const n = typeof val === "number" ? val : parseFloat(String(val));
  if (isNaN(n)) return "default";
  if (n >= 75) return "success";
  if (n >= 50) return "warn";
  return "danger";
}

export function AtsScanCard({ jdText, setJdText, onScan, scan, history }: Props) {
  return (
    <CardSection
      title="ATS Scan"
      subtitle="Paste a job description and run to see how well your resume matches."
    >
      <FormField label="Job Description" hint="paste full JD text">
        <textarea
          rows={6}
          value={jdText}
          placeholder="Paste job description here…"
          onChange={(e) => setJdText(e.target.value)}
        />
      </FormField>
      <div className="row">
        <button type="button" onClick={onScan}>Run ATS scan</button>
      </div>

      {scan ? (
        <div className="metric-grid">
          <MetricTile label="Composite" value={scan.composite} variant={scoreVariant(scan.composite)} />
          <MetricTile label="Keyword"   value={scan.keyword}   variant={scoreVariant(scan.keyword)} />
          <MetricTile label="Format"    value={scan.format}    variant={scoreVariant(scan.format)} />
          <MetricTile label="Quality"   value={scan.quality}   variant={scoreVariant(scan.quality)} />
          <MetricTile label="Complete"  value={scan.complete}  variant={scoreVariant(scan.complete)} />
          <MetricTile label="Contact"   value={scan.contact}   variant={scoreVariant(scan.contact)} />
        </div>
      ) : (
        <p className="muted scan-empty-hint">
          Run a scan to see your scores.
        </p>
      )}

      {history.length > 0 && (
        <>
          <p className="card-subtitle muted scan-history-label">Recent scans</p>
          {history.slice(0, 5).map((h) => (
            <p key={h.id} className="muted scan-history-row">
              #{h.id} · score {h.composite_score} · {new Date(h.created_at).toLocaleString()}
            </p>
          ))}
        </>
      )}
    </CardSection>
  );
}
