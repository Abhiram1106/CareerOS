import { SCORE_COMPONENTS } from "../../lib/placement";
import type { ScoreComponentKey } from "../../lib/placement";

type Props = {
  barScores: Record<ScoreComponentKey, number>;
  overallScore: number;
  scoreBucket: string | null;
  semanticMethod?: string | null;
};

const SEMANTIC_METHOD_LABEL: Record<string, string> = {
  char_ngram_proxy: "Char-n-gram TF-IDF (lexical proxy — no model)",
  sentence_embedding: "MiniLM sentence embedding (PyTorch CPU)",
  sentence_embedding_openvino: "MiniLM sentence embedding (OpenVINO-accelerated)",
};

const JD_MATCH_TOOLTIP =
  "JD Match = 0.35·TF-IDF cosine + 0.35·semantic cosine + 0.20·skill recall + 0.10·eligibility. " +
  "Semantic method shown below — sentence embeddings when available, char-n-gram proxy otherwise.";

export function ScoreBreakdown({ barScores, overallScore, scoreBucket, semanticMethod }: Props) {
  const methodLabel = semanticMethod ? SEMANTIC_METHOD_LABEL[semanticMethod] ?? semanticMethod : null;

  return (
    <div className="score-breakdown">
      <div className="score-overall">
        <span className="score-overall-value">{overallScore}</span>
        <span className="score-overall-label">Placement Readiness</span>
        {scoreBucket ? <span className="score-bucket-pill">{scoreBucket}</span> : null}
      </div>
      <ul className="score-bars" aria-label="Score components">
        {SCORE_COMPONENTS.map(({ key, label, weight, color }) => {
          const value = barScores[key];
          const isJdMatch = key === "jd_match";
          return (
            <li key={key} className="score-bar-row">
              <div className="score-bar-meta">
                <span title={isJdMatch ? JD_MATCH_TOOLTIP : undefined}>
                  {label}
                  {isJdMatch ? <span aria-hidden="true"> ⓘ</span> : null}
                </span>
                <span className="score-bar-weight">{weight}</span>
              </div>
              <div className="score-bar-track" role="presentation">
                <div
                  className="score-bar-fill"
                  style={{ width: `${Math.min(100, Math.max(0, value))}%`, background: color }}
                />
              </div>
              <span className="score-bar-value">{Math.round(value)}</span>
            </li>
          );
        })}
      </ul>
      {methodLabel ? (
        <p className="score-method-note" title={JD_MATCH_TOOLTIP}>
          JD-match semantic signal: <strong>{methodLabel}</strong>
        </p>
      ) : null}
    </div>
  );
}
