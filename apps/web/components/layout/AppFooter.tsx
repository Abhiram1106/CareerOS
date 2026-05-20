const TECH_BADGES = [
  { label: "Next.js 14",            cls: "badge-neutral" },
  { label: "FastAPI",               cls: "badge-neutral" },
  { label: "PostgreSQL",            cls: "badge-neutral" },
  { label: "OpenVINO",              cls: "badge-intel"   },
  { label: "Intel sklearnex",       cls: "badge-intel"   },
];

const ROADMAP = [
  "JD match engine (Week 2)",
  "Proof-linked rewriter (Week 3)",
  "Officer dashboard (Week 4)",
  "Intel benchmark panel (Week 5)",
];

export function AppFooter() {
  return (
    <footer className="app-footer">
      <div className="app-footer-inner">
        <div className="footer-brand">
          <strong>CareerOS Campus AI</strong>
          <p>
            Placement-readiness operating layer for Indian colleges.
            Scoring formula: <code className="inline-code">packages/scoring/</code> — never duplicated.
          </p>
          <p className="muted footer-roadmap">
            Roadmap: {ROADMAP.join(" · ")}
          </p>
        </div>

        <div className="footer-badges" aria-label="Technology stack">
          {TECH_BADGES.map((b) => (
            <span key={b.label} className={`badge ${b.cls}`}>{b.label}</span>
          ))}
        </div>
      </div>
    </footer>
  );
}
