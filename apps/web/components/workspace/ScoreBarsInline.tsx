import { SCORE_COMPONENTS, readinessBucket } from "../../lib/placement";

export function ScoreBarsInline({
  barScores,
  overallScore,
  scoreBucket,
}: {
  barScores: Record<string, number>;
  overallScore: number;
  scoreBucket: string | null;
}) {
  const bucket = readinessBucket(overallScore);
  return (
    <div>
      {SCORE_COMPONENTS.map((sc) => {
        const val = barScores[sc.key] ?? 0;
        return (
          <div key={sc.key} className="score-inline-row">
            <span className="score-inline-label">
              {sc.label} <span className="score-inline-weight">({sc.weight})</span>
            </span>
            <div className="score-inline-track">
              <div className="score-inline-fill" style={{ width: `${val}%`, background: sc.color }} />
            </div>
            <span className="score-inline-value" style={{ color: sc.color }}>
              {Math.round(val)}
            </span>
          </div>
        );
      })}
      <div className="score-inline-total">
        <span>Placement Readiness</span>
        <div className="score-inline-total-end">
          <span className="score-inline-total-num">{overallScore}</span>
          <span className={`bucket-badge ${bucket.cls}`}>{scoreBucket ?? bucket.label}</span>
        </div>
      </div>
    </div>
  );
}

export function SkillLists({ matched, missing }: { matched: string[]; missing: string[] }) {
  if (matched.length === 0 && missing.length === 0) return null;
  return (
    <div className="skill-lists">
      {matched.length > 0 && (
        <p>
          <strong>Matched skills:</strong> {matched.join(", ")}
        </p>
      )}
      {missing.length > 0 && (
        <p className="skill-lists-missing">
          <strong>Missing required:</strong> {missing.join(", ")}
        </p>
      )}
    </div>
  );
}
