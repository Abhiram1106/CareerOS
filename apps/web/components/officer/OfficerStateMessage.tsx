"use client";

type OfficerStateMessageProps = {
  loading?: boolean;
  error?: string | null;
  empty?: boolean;
  emptyLabel?: string;
};

export function OfficerStateMessage({
  loading,
  error,
  empty,
  emptyLabel = "No data yet.",
}: OfficerStateMessageProps) {
  if (loading) {
    return (
      <p style={{ fontFamily: "var(--font-mono)", fontSize: "0.82rem", color: "#717783" }}>
        Loading…
      </p>
    );
  }
  if (error) {
    return (
      <p style={{ fontFamily: "var(--font-mono)", fontSize: "0.82rem", color: "#ba1a1a" }} role="alert">
        {error}
      </p>
    );
  }
  if (empty) {
    return (
      <p style={{ fontFamily: "var(--font-mono)", fontSize: "0.82rem", color: "#717783" }}>
        {emptyLabel}
      </p>
    );
  }
  return null;
}
