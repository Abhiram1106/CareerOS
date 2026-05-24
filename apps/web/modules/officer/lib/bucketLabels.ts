const BUCKET_ALIASES: Record<string, string> = {
  strong: "strong",
  ready: "ready",
  borderline: "borderline",
  risk: "risk",
  "high-risk": "risk",
};

export function bucketPresentation(bucket: string): { label: string; className: string } {
  const key = BUCKET_ALIASES[bucket] ?? "risk";
  const labels: Record<string, string> = {
    strong: "Strong",
    ready: "Ready",
    borderline: "Borderline",
    risk: "High Risk",
  };
  return { label: labels[key] ?? bucket, className: `bucket-${key}` };
}
