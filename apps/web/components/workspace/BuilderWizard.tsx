type Step = {
  id: string;
  title: string;
  description: string;
  done: boolean;
};

type Props = {
  steps: Step[];
};

export function BuilderWizard({ steps }: Props) {
  return (
    <section className="content-card">
      <div className="content-card-header">
        <h2 className="content-card-title">Resume Builder Wizard</h2>
      </div>
      <div className="content-card-body">
        <ol className="section-list">
          {steps.map((step) => (
            <li key={step.id} className="section-list-item">
              <div>
                <p className="section-list-name">{step.title}</p>
                <p className="scan-intro">{step.description}</p>
              </div>
              <span className={`section-conf-badge ${step.done ? "" : "chip-mono"}`}>
                {step.done ? "DONE" : "PENDING"}
              </span>
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
}
