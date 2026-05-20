"use client";

import { useRef } from "react";
import { m, useScroll, useTransform } from "motion/react";
import {
  Zap, Shield, BarChart3, Building2, XCircle, ArrowRight,
  Brain, Upload, FileSearch, Users, TrendingUp,
} from "lucide-react";
import { TextReveal } from "../ui/TextReveal";
import { AnimatedCounter } from "../ui/AnimatedCounter";
import { TiltCard } from "../ui/TiltCard";

type Props = { onOpenWorkspace: () => void };

const STEPS = [
  { step: "01", icon: Upload,      label: "Upload resume",       sub: "pdfplumber + python-docx",          status: "live"  },
  { step: "02", icon: FileSearch,  label: "JD match + score",    sub: "TF-IDF + sentence-transformers",    status: "week2" },
  { step: "03", icon: Brain,       label: "Proof-linked rewrite", sub: "Guardrailed LLM · no fabrication", status: "week3" },
  { step: "04", icon: Users,       label: "Officer cohort view",  sub: "Batch heatmap · review queue",     status: "week4" },
] as const;

const STATUS_LABEL: Record<string, string> = {
  live: "Live", week2: "Week 2", week3: "Week 3", week4: "Week 4",
};

const COUNTERS = [
  { end: 6,   suffix: "",  label: "Readiness dimensions"     },
  { end: 42,  suffix: "%", label: "Avg employability gap"    },
  { end: 100, suffix: "%", label: "Zero fabrications"        },
  { end: 4,   suffix: "×", label: "Intel clustering speedup" },
];

const PILLARS = [
  { icon: Building2,  iconClass: "icon-navy",   title: "Campus-native",         body: "Built for Indian placement cycles — TPO workflows, cohort batches, and department-level visibility from day one.",                                                                                     span: 1, dark: false },
  { icon: Shield,     iconClass: "icon-intel",  title: "ATS-first",             body: "Parse safety, format penalties, and keyword alignment checked before students chase the wrong roles.",                                                                                              span: 1, dark: false },
  { icon: Zap,        iconClass: "icon-orange", title: "Intel-measured",        body: "OpenVINO and sklearnex benchmarks on real workloads — p50 latency tracked at 500 / 5 000 / 20 000 resumes. Speedups measured, not claimed.",                                                      span: 2, dark: false },
  { icon: Brain,      iconClass: "icon-green",  title: "Governed AI",           body: "No invented internships, metrics, or certifications. Every suggestion links to source evidence in the resume.",                                                                                    span: 2, dark: true  },
  { icon: BarChart3,  iconClass: "icon-sky",    title: "Placement intelligence", body: "Officers see who is ready, who is at risk, and what skills the entire batch is missing — before company drives.",                                                                                  span: 1, dark: false },
  { icon: TrendingUp, iconClass: "icon-purple", title: "Outcome moat",          body: "Event logging from upload → shortlist → offer builds the outcome data that makes CareerOS defensible over time.",                                                                                  span: 1, dark: false },
] as const;

const WORKFLOW_STEPS = [
  { step: "01", icon: Upload,     title: "Upload resume",         body: "PDF or DOCX in. Sections extracted with confidence scores and ATS parse-safety flags — before a single recruiter sees it.",                     status: "live"  },
  { step: "02", icon: FileSearch, title: "JD match + score",      body: "Paste any company JD. Six-component PlacementReadinessScore shows exactly where the gap is — not just a generic number.",                      status: "week2" },
  { step: "03", icon: Brain,      title: "Proof-linked rewrite",  body: "AI rewrites only what the resume can support. Unsupported claims surface in a flagged list — never silently inserted.",                        status: "week3" },
  { step: "04", icon: Users,      title: "Officer cohort view",   body: "Placement officers get department-level heatmaps, skill-gap breakdowns, and an approval queue — before the drive.",                            status: "week4" },
] as const;

const containerVariants = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.1, delayChildren: 0.05 } },
};

const CARD_EASE = [0.16, 1, 0.3, 1] as [number, number, number, number];

const cardVariants = {
  hidden:  { opacity: 0, y: 28 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.55, ease: CARD_EASE } },
};

export function HeroPage({ onOpenWorkspace }: Props) {
  const frameRef = useRef<HTMLDivElement>(null);
  const { scrollY } = useScroll();
  const cardY = useTransform(scrollY, [0, 500], [0, -70]);

  return (
    <div className="hero-page">

      {/* ── Full-width centered hero ─────────────────────────────── */}
      <section className="hero-centered" aria-labelledby="hero-heading">
        <div className="hero-mesh-bg" aria-hidden="true" />

        {/* Eyebrow pill */}
        <m.div
          className="hero-eyebrow-row"
          initial={{ opacity: 0, y: -12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <span className="hero-eyebrow-pill">
            <span className="hero-eyebrow-dot" />
            Intel-optimized · Week 1 live
          </span>
        </m.div>

        {/* Headline — word-by-word reveal */}
        <m.div
          className="hero-title-block"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.1 }}
        >
          <h1 id="hero-heading">
            <TextReveal text="The placement-readiness" as="span" />
            {" "}
            <TextReveal text="operating layer" as="span" className="gradient-text" delay={0.35} />
            {" "}
            <TextReveal text="for Indian colleges" as="span" delay={0.6} />
          </h1>
          <m.p
            className="hero-subtitle"
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.9, duration: 0.55 }}
          >
            CareerOS Campus AI turns unstructured student resumes into ATS-safe,
            JD-matched, proof-linked readiness signals — so placement officers know
            exactly who is ready before companies arrive.
          </m.p>
        </m.div>

        {/* CTAs */}
        <m.div
          className="hero-cta-row"
          initial={{ opacity: 0, y: 14 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.05, duration: 0.5 }}
        >
          <button type="button" className="btn-primary btn-glow" onClick={onOpenWorkspace}>
            Open student workspace <ArrowRight size={16} />
          </button>
          <a className="btn-ghost" href="#how-it-works">
            See how it works
          </a>
        </m.div>

        {/* Not-list */}
        <m.div
          className="hero-not-row"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.2, duration: 0.5 }}
          aria-label="What this product is not"
        >
          {["Not a job board", "Not a LinkedIn scraper", "Not a recruiter marketplace"].map((item) => (
            <span key={item} className="hero-not-item">
              <XCircle size={13} color="var(--warn)" /> {item}
            </span>
          ))}
        </m.div>

        {/* Animated counter row */}
        <m.div
          className="hero-counter-row"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.3, duration: 0.55 }}
          aria-label="Key numbers"
        >
          {COUNTERS.map((c) => (
            <div key={c.label} className="hero-counter-item">
              <span className="hero-counter-value gradient-text">
                <AnimatedCounter end={c.end} suffix={c.suffix} />
              </span>
              <span className="hero-counter-label">{c.label}</span>
            </div>
          ))}
        </m.div>

        {/* Demo card — parallax on scroll */}
        <m.div
          ref={frameRef}
          className="hero-product-frame"
          style={{ y: cardY }}
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.5, duration: 0.7, ease: [0.16, 1, 0.3, 1] }}
        >
          <div className="hero-product-card glass">
            {/* Window chrome */}
            <div className="demo-chrome">
              <div className="demo-card-dots"><span /><span /><span /></div>
              <span className="badge badge-success">Week 1 — Live</span>
            </div>

            {/* Steps */}
            <div className="demo-steps">
              {STEPS.map((step, idx) => {
                const Icon = step.icon;
                return (
                  <m.div
                    key={step.step}
                    className="demo-step-row"
                    initial={{ opacity: 0, x: -12 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 1.7 + idx * 0.12, duration: 0.4 }}
                  >
                    <span className="demo-step-num">{step.step}</span>
                    <Icon size={16} color="var(--intel)" />
                    <div>
                      <p className="demo-step-label">{step.label}</p>
                      <p className="demo-step-sub">{step.sub}</p>
                    </div>
                    <span className={`hero-loop-status status-${step.status} demo-step-status`}>
                      {STATUS_LABEL[step.status]}
                    </span>
                  </m.div>
                );
              })}
            </div>
          </div>
        </m.div>
      </section>

      {/* ── Bento feature grid ───────────────────────────────────── */}
      <section aria-labelledby="pillars-heading">
        <m.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.5 }}
          className="section-intro"
        >
          <h2 id="pillars-heading" className="section-heading">Why colleges adopt CareerOS</h2>
          <p className="section-subheading">Four capabilities that make this a placement-office tool, not a resume builder.</p>
        </m.div>

        <m.div
          className="bento-grid"
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-60px" }}
        >
          {PILLARS.map((pillar) => {
            const Icon = pillar.icon;
            return (
              <m.div key={pillar.title} variants={cardVariants} className={pillar.span === 2 ? "span-2" : ""}>
                <TiltCard className={pillar.dark ? "bento-dark" : ""}>
                  <div className={`bento-card-icon ${pillar.iconClass}`}>
                    <m.div
                      className="icon-wrapper"
                      whileHover={{ scale: 1.18, rotate: 8 }}
                      transition={{ type: "spring", stiffness: 400, damping: 20 }}
                    >
                      <Icon size={20} color={pillar.dark ? "#fff" : undefined} />
                    </m.div>
                  </div>
                  <h3>{pillar.title}</h3>
                  <p>{pillar.body}</p>
                </TiltCard>
              </m.div>
            );
          })}
        </m.div>
      </section>

      {/* ── Intel strip ──────────────────────────────────────────── */}
      <m.div
        className="intel-strip"
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: "-60px" }}
        transition={{ duration: 0.55 }}
        role="complementary"
        aria-label="Intel optimization"
      >
        <m.div
          className="intel-icon"
          whileHover={{ scale: 1.1, rotate: 6 }}
          transition={{ type: "spring", stiffness: 300 }}
          aria-hidden="true"
        >
          <Zap size={22} color="#fff" />
        </m.div>
        <div>
          <h3>Intel-accelerated inference and analytics</h3>
          <p>OpenVINO for embedding inference, sklearnex for TF-IDF and KMeans. Real benchmarks at three dataset sizes — not vendor claims.</p>
        </div>
        <div className="intel-benchmarks" aria-label="Benchmark results">
          {[{ value: "2.5×", label: "embed speed" }, { value: "4×", label: "clustering" }, { value: "6", label: "score dims" }].map((b) => (
            <div key={b.label} className="intel-bench-item">
              <strong>{b.value}</strong><span>{b.label}</span>
            </div>
          ))}
        </div>
      </m.div>

      {/* ── Workflow steps ───────────────────────────────────────── */}
      <section id="how-it-works" className="workflow-section" aria-labelledby="workflow-heading">
        <m.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-60px" }}
          transition={{ duration: 0.5 }}
        >
          <h2 id="workflow-heading" className="section-heading">End-to-end placement readiness</h2>
          <p className="section-subheading">One loop from raw resume to officer dashboard — all in the same platform.</p>
        </m.div>

        <m.ol
          className="workflow-steps"
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-60px" }}
        >
          {WORKFLOW_STEPS.map((item) => {
            const Icon = item.icon;
            return (
              <m.li key={item.step} variants={cardVariants} className="workflow-step">
                <div className="workflow-index" aria-hidden="true">
                  <Icon size={18} color="var(--accent-ink)" />
                </div>
                <div>
                  <div className="workflow-step-meta">
                    <h3>{item.title}</h3>
                    <span className={`hero-loop-status status-${item.status}`}>{STATUS_LABEL[item.status]}</span>
                  </div>
                  <p>{item.body}</p>
                </div>
              </m.li>
            );
          })}
        </m.ol>

        <m.div
          className="workflow-cta"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
        >
          <button type="button" className="btn-primary btn-glow" onClick={onOpenWorkspace}>
            Start in workspace <ArrowRight size={16} />
          </button>
          <p className="muted workflow-cta-note">Free to use · No sign-up required to explore</p>
        </m.div>
      </section>

    </div>
  );
}
