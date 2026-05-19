type Props = {
  onOpenWorkspace: () => void;
};

const FLOW_STEPS = [
  {
    step: "01",
    title: "Resume in",
    body: "Upload PDF or DOCX. Sections are extracted with confidence scores and ATS-parse safety flags.",
  },
  {
    step: "02",
    title: "JD match + score",
    body: "Paste a job description. Get ATS-safe scoring and a placement-readiness snapshot tied to your profile.",
  },
  {
    step: "03",
    title: "Proof-linked rewrite",
    body: "AI rewrites only what your resume can support. Unsupported claims are flagged — never invented.",
  },
  {
    step: "04",
    title: "Officer cohort view",
    body: "Placement officers see batch readiness heatmaps and intervention queues (Week 4 surface).",
  },
];

const PILLARS = [
  {
    title: "Campus-native",
    body: "Built for Indian college placement cycles — batches, TPO workflows, and cohort visibility.",
  },
  {
    title: "ATS-first",
    body: "Parse safety, format penalties, and keyword alignment before students chase the wrong roles.",
  },
  {
    title: "Intel-measured",
    body: "OpenVINO and sklearnex benchmarks quantify latency wins on scoring and matching workloads.",
  },
  {
    title: "Governed AI",
    body: "No fabricated internships, metrics, or certifications. Evidence stays linked to source bullets.",
  },
];

const NOT_LIST = [
  "Not a job board or LinkedIn scraper",
  "Not a recruiter marketplace",
  "Not a billing or payments product",
];

export function HeroPage({ onOpenWorkspace }: Props) {
  return (
    <div className="hero-page">
      <section className="hero-panel" aria-labelledby="hero-heading">
        <div className="hero-copy">
          <p className="eyebrow">Intel-optimized placement readiness</p>
          <h1 id="hero-heading">The operating layer for campus placements</h1>
          <p className="hero-lead">
            CareerOS Campus AI helps students ship ATS-safe resumes, match real job descriptions, and
            improve with proof-linked feedback — while placement officers get cohort-level readiness signals.
          </p>
          <div className="hero-actions">
            <button type="button" className="btn-primary" onClick={onOpenWorkspace}>
              Open student workspace
            </button>
            <a className="btn-ghost" href="#how-it-works">
              See how it works
            </a>
          </div>
          <ul className="hero-not-list">
            {NOT_LIST.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>

        <aside className="hero-aside" aria-label="Demo loop summary">
          <div className="hero-card">
            <p className="hero-card-label">Live demo loop (Week 1–2)</p>
            <ul className="hero-loop">
              <li>
                <span>Parse</span>
                <strong>pdfplumber + section extractor</strong>
              </li>
              <li>
                <span>Score</span>
                <strong>ATS engine + readiness metrics</strong>
              </li>
              <li>
                <span>Export</span>
                <strong>PDF via async worker</strong>
              </li>
              <li>
                <span>Match</span>
                <strong className="muted-inline">TF-IDF + embeddings (Week 2)</strong>
              </li>
            </ul>
          </div>
          <div className="hero-stats">
            <div>
              <strong>6</strong>
              <span>readiness dimensions</span>
            </div>
            <div>
              <strong>3</strong>
              <span>workspace tabs</span>
            </div>
            <div>
              <strong>1</strong>
              <span>shared scoring package</span>
            </div>
          </div>
        </aside>
      </section>

      <section className="feature-strip" aria-labelledby="pillars-heading">
        <h2 id="pillars-heading" className="section-heading">
          Why colleges adopt CareerOS
        </h2>
        <div className="feature-grid">
          {PILLARS.map((pillar) => (
            <article key={pillar.title} className="feature-card">
              <h3>{pillar.title}</h3>
              <p>{pillar.body}</p>
            </article>
          ))}
        </div>
      </section>

      <section id="how-it-works" className="workflow-section" aria-labelledby="workflow-heading">
        <h2 id="workflow-heading" className="section-heading">
          End-to-end placement readiness
        </h2>
        <ol className="workflow-steps">
          {FLOW_STEPS.map((item) => (
            <li key={item.step} className="workflow-step">
              <span className="workflow-index">{item.step}</span>
              <div>
                <h3>{item.title}</h3>
                <p>{item.body}</p>
              </div>
            </li>
          ))}
        </ol>
        <div className="workflow-cta">
          <button type="button" className="btn-primary" onClick={onOpenWorkspace}>
            Start in workspace
          </button>
        </div>
      </section>
    </div>
  );
}
