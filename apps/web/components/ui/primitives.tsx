import { ReactNode } from "react";

type CardSectionProps = {
  title: string;
  subtitle?: string;
  children: ReactNode;
};

type FormFieldProps = {
  label: string;
  children: ReactNode;
};

type MetricTileProps = {
  label: string;
  value: string | number;
};

export function CardSection({ title, subtitle, children }: CardSectionProps) {
  return (
    <section className="card">
      <h2>{title}</h2>
      {subtitle ? <p className="muted">{subtitle}</p> : null}
      {children}
    </section>
  );
}

export function FormField({ label, children }: FormFieldProps) {
  return (
    <label>
      <span>{label}</span>
      {children}
    </label>
  );
}

export function MetricTile({ label, value }: MetricTileProps) {
  return (
    <div className="metric">
      <p>{label}</p>
      <strong>{value}</strong>
    </div>
  );
}
