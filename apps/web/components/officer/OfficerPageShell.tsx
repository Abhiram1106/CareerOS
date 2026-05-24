"use client";

import type { ReactNode } from "react";

type OfficerPageShellProps = {
  title: string;
  subtitle: string;
  children: ReactNode;
};

export function OfficerPageShell({ title, subtitle, children }: OfficerPageShellProps) {
  return (
    <div className="page-canvas">
      <div className="page-title-row">
        <div>
          <h1 className="page-title">{title}</h1>
          <p className="page-subtitle">{subtitle}</p>
        </div>
        <div style={{ display: "flex", gap: 8 }}>
          <span
            style={{
              background: "#001c38",
              color: "#fff",
              borderRadius: 9999,
              padding: "5px 12px",
              fontFamily: "var(--font-mono)",
              fontSize: "0.72rem",
              fontWeight: 500,
              display: "flex",
              alignItems: "center",
              gap: 6,
            }}
          >
            Week 4
          </span>
          <span
            style={{
              background: "#f2f4f7",
              border: "1px solid rgba(192,199,211,0.3)",
              borderRadius: 9999,
              padding: "5px 12px",
              fontFamily: "var(--font-mono)",
              fontSize: "0.72rem",
              fontWeight: 500,
              color: "#16a34a",
              display: "flex",
              alignItems: "center",
              gap: 6,
            }}
          >
            <span
              style={{
                width: 7,
                height: 7,
                borderRadius: "50%",
                background: "#16a34a",
                display: "inline-block",
              }}
              className="icon-shimmer"
            />
            Live
          </span>
        </div>
      </div>
      {children}
    </div>
  );
}
