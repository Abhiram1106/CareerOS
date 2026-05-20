type Props = {
  onOpenWorkspace: () => void;
};

const FLOW_STEPS = [
  {
    step: "01",
    title: "Upload resume",
    sub: "pdfplumber + python-docx + section extractor",
    body: "PDF or DOCX in. Sections extracted with confidence scores and ATS parse-safety flags — before a single recruiter sees it.",
    status: "live" as const,
  },
  {
    step: "02",
    title: "JD match + score",
    sub: "TF-IDF + sentence-transformers + sklearnex",
    body: "Paste any job description. Six-component PlacementReadinessScore shows exactly where the gap is — not just a generic number.",
    status: "week2" as const,
  },
  {
    step: "03",
    title: "Proof-linked rewrite",
    sub: "Guardrailed LLM — no fabrication",
    body: "AI rewrites only what the resume can support. Unsupported claims surface in a flagged list — never silently inserted.",
    status: "week3" as const,
  },
  {
    step: "04",
    title: "Officer cohort view",
    sub: "Batch readiness heatmap + review queue",
    body: "Placement officers get department-level readiness heatmaps, skill-gap breakdowns, and an approval queue — before the drive.",
    status: "week4" as const,
  },
];

const STATUS_LABEL: Record<string, string> = {
  live:  "Live",
  week2: "Week 2",
  week3: "Week 3",
  week4: "Week 4",
};

const PILLARS = [
  {
    icon: "🏛️",
    iconClass: "feature-icon-navy",
    title: "Campus-native",
    body: "Built for Indian placement cycles — TPO workflows, cohort batches, and department-level visibility from day one.",
  },
  {
    icon: "🛡️",
    iconClass: "feature-icon-blue",
    title: "ATS-first",
    body: "Parse safety, format penalties, and keyword alignment checked before students chase the wrong roles.",
  },
  {
    icon: "⚡",
    iconClass: "feature-icon-orange",
    title: "Intel-measured",
    body: "OpenVINO and sklearnex benchmarks on real workloads. Speedups are measured, not claimed.",
  },
  {
    icon: "🔒",
    iconClass: "feature-icon-green",
    title: "Governed AI",
    body: "No invented internships, metrics, or certifications. Every suggestion links to source evidence in the resume.",
  },
];

const NOT_LIST = [
  "Not a job board or LinkedIn scraper",
  "Not a recruiter marketplace",
  "Not a billing or payments product",
];

const INTEL_BENCHMARKS = [
  { value: "2.5×", label: "embed speed" },
  { value: "4×",   label: "clustering" },
  { value: "6",    label: "score dims" },
];

export function HeroPage({ onOpenWorkspace }: Props) {
  return (
    <div className="hero-page">

      {/* ── Hero panel ──────────────────────────────────────────────── */}
      <section className="hero-panel" aria-labelledby="hero-heading">

        <div className="hero-copy">
          <p className="eyebrow">Intel-optimized placement readiness</p>

          <h1 id="hero-heading" className="hero-heading">
            The operating layer<br />for campus placements
          </h1>

          <p className="hero-lead">
            CareerOS Campus AI helps Indian colleges turn unstructured student
            resumes into ATS-safe, JD-matched, proof-linked readiness signals —
            so placement officers know who is ready before companies arrive.
          </p>

          <div className="hero-actions">
            <button type="button" className="btn-primary" onClick={onOpenWorkspace}>
              Open student workspace
            </button>
            <a className="btn-ghost btn-compact" href="#how-it-works">
              See how it works ↓
            </a>
          </div>

          <ul className="hero-not-list" aria-label="What this product is not">
            {NOT_LIST.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>

        {/* Aside — demo loop + stats */}
        <aside className="hero-aside" aria-label="Demo loop and key stats">
          <div className="hero-card">
            <div className="hero-card-header">
              <p className="hero-card-label">Demo loop — Weeks 1–5</p>
              <span className="badge badge-success">Week 1 live</span>
            </div>

            <ol className="hero-loop">
              {FLOW_STEPS.map((step) => (
                <li key={step.step} className="hero-loop-item">
                  <span className="hero-loop-step">{step.step}</span>
                  <div>
                    <p className="hero-loop-label">{step.title}</p>
                    <p className="hero-loop-sub">{step.sub}</p>
                  </div>
                  <span className={`hero-loop-status status-${step.status}`}>
                    {STATUS_LABEL[step.status]}
                  </span>
                </li>
              ))}
            </ol>
          </div>

          <div className="hero-stats" aria-label="Key numbers">
            <div className="hero-stat">
              <strong>6</strong>
              <span>Score dims</span>
            </div>
            <div className="hero-stat">
              <strong>42%</strong>
              <span>Avg employability</span>
            </div>
            <div className="hero-stat">
              <strong>0</strong>
              <span>Fabrications</span>
            </div>
          </div>
        </aside>
      </section>

      {/* ── Intel strip ─────────────────────────────────────────────── */}
      <div className="intel-strip" role="complementary" aria-label="Intel optimization">
        <div className="intel-icon" aria-hidden="true">⚡</div>
        <div>
          <h3>Intel-accelerated inference and analytics</h3>
          <p>
            Scoring and matching pipelines run on OpenVINO (embedding inference)
            and Intel Extension for Scikit-learn (TF-IDF, KMeans, cosine similarity).
            Benchmarks are real measurements — not vendor headline numbers.
          </p>
        </div>
        <div className="intel-benchmarks" aria-label="Benchmark results">
          {INTEL_BENCHMARKS.map((b) => (
            <div key={b.label} className="intel-bench-item">
              <strong>{b.value}</strong>
              <span>{b.label}</span>
            </div>
          ))}
        </div>
      </div>

      {/* ── Feature pillars ──────────────────────────────────────────── */}
      <section className="feature-strip" aria-labelledby="pillars-heading">
        <h2 id="pillars-heading" className="section-heading">
          Why colleges adopt CareerOS
        </h2>
        <p className="section-subheading">
          Four capabilities that make this a placement-office tool, not a resume builder.
        </p>
        <div className="feature-grid">
          {PILLARS.map((pillar) => (
            <article key={pillar.title} className="feature-card">
              <div className={`feature-icon ${pillar.iconClass}`} aria-hidden="true">
                {pillar.icon}
              </div>
              <h3>{pillar.title}</h3>
              <p>{pillar.body}</p>
            </article>
          ))}
        </div>
      </section>

      {/* ── Workflow steps ───────────────────────────────────────────── */}
      <section
        id="how-it-works"
        className="workflow-section"
        aria-labelledby="workflow-heading"
      >
        <h2 id="workflow-heading" className="section-heading">
          End-to-end placement readiness
        </h2>
        <p className="section-subheading">
          One loop from raw resume to officer dashboard — all in the same platform.
        </p>

        <ol className="workflow-steps">
          {FLOW_STEPS.map((item) => (
            <li key={item.step} className="workflow-step">
              <span className="workflow-index" aria-hidden="true">{item.step}</span>
              <div>
                <div className="workflow-step-meta">
                  <h3>{item.title}</h3>
                  <span className={`hero-loop-status status-${item.status}`}>
                    {STATUS_LABEL[item.status]}
                  </span>
                </div>
                <p>{item.body}</p>
              </div>
            </li>
          ))}
        </ol>

        <div className="workflow-cta">
          <button type="button" className="btn-primary" onClick={onOpenWorkspace}>
            Start in workspace
          </button>
          <p className="muted workflow-cta-note">
            Free to use · No sign-up required to explore
          </p>
        </div>
      </section>

    </div>
  );
}
