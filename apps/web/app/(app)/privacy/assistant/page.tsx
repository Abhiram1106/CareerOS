export default function AssistantPrivacyPage() {
  return (
    <div className="content-card" style={{ maxWidth: 720, margin: "24px auto" }}>
      <div className="content-card-header">
        <h1 className="content-card-title">Campus Assistant — privacy</h1>
      </div>
      <div className="content-card-body" style={{ fontSize: "0.9rem", lineHeight: 1.6, color: "#414752" }}>
        <p>
          FAQ mode (default) runs entirely on CareerOS servers using static product documentation. No third-party
          LLM receives your data unless your campus operator configures an external API key.
        </p>
        <p>
          When LLM mode is enabled, we send FAQ excerpts, anonymized score bands (not resume text), and your question.
          We reject known prompt-injection patterns before any external call.
        </p>
        <p>
          Full policy text:{" "}
          <a href="https://github.com/Abhiram1106/CareerOS/blob/main/docs/privacy/assistant.md">docs/privacy/assistant.md</a>
        </p>
      </div>
    </div>
  );
}
