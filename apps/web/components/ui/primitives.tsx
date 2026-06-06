import { ReactNode } from "react";

// ── CardSection ───────────────────────────────────────────────────────────

type CardSectionProps = {
  title: string;
  subtitle?: string;
  badge?: ReactNode;
  action?: ReactNode;
  children: ReactNode;
};

export function CardSection({ title, subtitle, badge, action, children }: CardSectionProps) {
  return (
    <section className="card">
      <div className="card-header">
        <div className="card-header-left">
          <h2>{title}</h2>
          {badge ? <span className="card-badge">{badge}</span> : null}
        </div>
        {action ? <div className="card-action">{action}</div> : null}
      </div>
      {subtitle ? <p className="card-subtitle muted">{subtitle}</p> : null}
      {children}
    </section>
  );
}

// ── FormField ─────────────────────────────────────────────────────────────

type FormFieldProps = {
  label: string;
  hint?: string;
  children: ReactNode;
};

export function FormField({ label, hint, children }: FormFieldProps) {
  return (
    <label>
      <span>{label}{hint ? <span className="field-hint">{hint}</span> : null}</span>
      {children}
    </label>
  );
}

// ── MetricTile ────────────────────────────────────────────────────────────

type MetricTileProps = {
  label: string;
  value: string | number;
  sub?: string;
  variant?: "default" | "success" | "warn" | "danger" | "intel";
};

const VARIANT_CLASS: Record<NonNullable<MetricTileProps["variant"]>, string> = {
  default: "",
  success: "metric-success",
  warn:    "metric-warn",
  danger:  "metric-danger",
  intel:   "metric-intel",
};

export function MetricTile({ label, value, sub, variant = "default" }: MetricTileProps) {
  return (
    <div className={`metric ${VARIANT_CLASS[variant]}`}>
      <p style={{ fontSize: "0.68rem", fontWeight: 800, textTransform: "uppercase", letterSpacing: "0.06em", color: "var(--muted-2)", marginBottom: 8 }}>
        {label}
      </p>
      <strong style={{ display: "block", fontSize: "1.8rem", fontFamily: "var(--font-mono)", fontWeight: 500, letterSpacing: "-0.04em", lineHeight: 1 }}>
        {value}
      </strong>
      {sub ? <span className="metric-sub" style={{ display: "block", fontSize: "0.72rem", color: "var(--muted-2)", marginTop: 4 }}>{sub}</span> : null}
    </div>
  );
}

// ── Divider ───────────────────────────────────────────────────────────────

export function Divider({ soft }: { soft?: boolean }) {
  return <hr className={soft ? "divider-soft" : "divider"} />;
}
