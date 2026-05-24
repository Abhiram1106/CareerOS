"use client";

import Link from "next/link";
import { useState } from "react";

import { useAssistantChat } from "../../modules/assistant/hooks/useAssistantChat";

const STARTERS = [
  "How do I upload my resume?",
  "What does my readiness score mean?",
  "How does proof-linked rewrite work?",
];

export function AssistantPanel() {
  const { messages, loading, error, send, canChat } = useAssistantChat();
  const [draft, setDraft] = useState("");

  const onSubmit = () => {
    if (!draft.trim() || loading) return;
    void send(draft);
    setDraft("");
  };

  return (
    <div className="content-card">
      <div className="content-card-header">
        <h2 className="content-card-title">Campus Assistant</h2>
        <span className="chip chip-primary">Grounded · no fabrication</span>
      </div>
      <div className="content-card-body">
        <p style={{ fontSize: "0.84rem", color: "#414752", marginBottom: 12, lineHeight: 1.55 }}>
          Ask about uploads, JD matching, rewrites, and readiness scores. Answers use product FAQ plus your latest
          scorecard summary only.
        </p>

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
          anonymized score bands are sent — never your full resume text. See{" "}
          <a href="/privacy/assistant" style={{ color: "#0071c5" }}>
            assistant privacy notice
          </a>
          .
        </p>

        {!canChat && <p style={{ color: "#93000a", fontSize: "0.82rem" }}>Sign in to use the assistant.</p>}

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
            border: "1px solid rgba(192,199,211,0.35)",
            borderRadius: 10,
            padding: 12,
            minHeight: 180,
            maxHeight: 320,
            overflowY: "auto",
            background: "#fafbfc",
            marginBottom: 12,
          }}
        >
          {messages.length === 0 ? (
            <p style={{ fontSize: "0.82rem", color: "#717783", margin: 0 }}>No messages yet.</p>
          ) : (
            messages.map((msg, idx) => (
              <div
                key={`${msg.role}-${idx}`}
                style={{ marginBottom: 10, textAlign: msg.role === "user" ? "right" : "left" }}
              >
                <span
                  style={{
                    display: "inline-block",
                    maxWidth: "92%",
                    padding: "8px 12px",
                    borderRadius: 10,
                    fontSize: "0.84rem",
                    lineHeight: 1.55,
                    background: msg.role === "user" ? "#d3e4ff" : "#fff",
                    border: "1px solid rgba(192,199,211,0.35)",
                    color: "#1a1c20",
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
          {loading ? <p style={{ fontSize: "0.78rem", color: "#717783" }}>Thinking…</p> : null}
          {error ? <p style={{ fontSize: "0.78rem", color: "#93000a" }}>{error}</p> : null}
        </div>

        <div style={{ display: "flex", gap: 8 }}>
          <input
            className="auth-input"
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            placeholder="Ask about readiness, ATS, or next steps…"
            disabled={!canChat || loading}
            onKeyDown={(e) => {
              if (e.key === "Enter") onSubmit();
            }}
          />
          <button
            type="button"
            className="btn-primary"
            disabled={!canChat || loading || !draft.trim()}
            onClick={onSubmit}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
