"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useAssistantChat } from "../../modules/assistant/useAssistantChat";

const STARTERS = [
  "How do I upload my resume?",
  "What does my readiness score mean?",
  "How does proof-linked rewrite work?",
];

export function AssistantPanel() {
  const { messages, loading, error, send, canChat } = useAssistantChat();
  const [draft, setDraft] = useState("");
  const [lastScore, setLastScore] = useState<number | null>(null);

  useEffect(() => {
    try {
      const raw = localStorage.getItem("cos_workspace_state_v1");
      if (!raw) return;
      const parsed = JSON.parse(raw) as { score_snapshot?: { overall_score?: number } };
      setLastScore(parsed.score_snapshot?.overall_score ?? null);
    } catch {
      setLastScore(null);
    }
  }, []);

  const onSubmit = () => {
    if (!draft.trim() || loading) return;
    void send(draft);
    setDraft("");
  };

  return (
    <div className="content-card">
      <div className="content-card-header">
        <h2 className="content-card-title">Student Assistant</h2>
        <span className="chip chip-primary">Grounded · no fabrication</span>
      </div>
      <div className="content-card-body">
        <p style={{ fontSize: "0.84rem", color: "var(--muted)", marginBottom: 12, lineHeight: 1.55 }}>
          Ask about uploads, JD matching, rewrites, and readiness scores. Answers use product FAQ plus your latest
          scorecard summary only.
        </p>
        {lastScore !== null ? (
          <p className="assistant-score-context">Your latest readiness score is {lastScore}.</p>
        ) : null}

        <p
          style={{
            fontSize: "0.78rem",
            color: "#717783",
            marginBottom: 12,
            lineHeight: 1.5,
            padding: "8px 10px",
            borderRadius: 8,
            background: "rgba(0,113,197,0.06)",
            border: "1px solid rgba(0,113,197,0.15)",
          }}
        >
          Privacy: messages stay on our servers. If an external LLM key is configured, only FAQ excerpts and
          anonymized score bands are sent, never your full resume text. See{" "}
          <a href="/privacy/assistant" style={{ color: "#0071c5" }}>
            assistant privacy notice
          </a>
          .
        </p>

        {!canChat && <p style={{ color: "var(--danger)", fontSize: "0.82rem" }}>Sign in to use the assistant.</p>}

        <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 14 }}>
          {STARTERS.map((prompt) => (
            <button
              key={prompt}
              type="button"
              className="btn-secondary"
              style={{ fontSize: "0.78rem", padding: "6px 10px" }}
              disabled={!canChat || loading}
              onClick={() => void send(prompt)}
            >
              {prompt}
            </button>
          ))}
        </div>

        <div
          style={{
            border: "1px solid var(--line)",
            borderRadius: "var(--radius-md)",
            padding: 12,
            minHeight: 180,
            maxHeight: 320,
            overflowY: "auto",
            background: "var(--surface-soft)",
            marginBottom: 12,
          }}
        >
          {messages.length === 0 ? (
            <p style={{ fontSize: "0.82rem", color: "#717783", margin: 0 }}>No messages yet.</p>
          ) : (
            messages.map((msg, idx) => (
              <div key={`${msg.role}-${idx}`} style={{ marginBottom: 10, textAlign: msg.role === "user" ? "right" : "left" }}>
                <span
                  style={{
                    display: "inline-block",
                    maxWidth: "92%",
                    padding: "8px 12px",
                    borderRadius: 10,
                    fontSize: "0.84rem",
                    lineHeight: 1.55,
                    background: msg.role === "user" ? "var(--accent-soft)" : "var(--surface)",
                    border: "1px solid var(--line)",
                    color: "var(--ink)",
                  }}
                >
                  {msg.text}
                </span>
                {msg.meta?.suggested_actions?.length ? (
                  <div style={{ marginTop: 6, display: "flex", flexWrap: "wrap", gap: 6 }}>
                    {msg.meta.suggested_actions.map((action) => (
                      <Link key={action.href} href={action.href} className="chip chip-mono">
                        {action.label}
                      </Link>
                    ))}
                  </div>
                ) : null}
              </div>
            ))
          )}
          {loading ? (
            <div className="typing-indicator" aria-label="Assistant is typing">
              <span />
              <span />
              <span />
            </div>
          ) : null}
          {error ? <p style={{ fontSize: "0.78rem", color: "var(--danger)" }}>{error}</p> : null}
        </div>

        <div style={{ display: "flex", gap: 8 }}>
          <input
            className="auth-input"
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            placeholder="Ask about readiness, ATS, or next steps..."
            disabled={!canChat || loading}
            onKeyDown={(e) => {
              if (e.key === "Enter") onSubmit();
            }}
          />
          <button type="button" className="btn-primary" disabled={!canChat || loading || !draft.trim()} onClick={onSubmit}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
