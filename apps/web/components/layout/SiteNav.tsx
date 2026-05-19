import type { AppView } from "../panes/types";

type Props = {
  activeView: AppView;
  onChange: (view: AppView) => void;
};

const LINKS: { id: AppView; label: string; hint: string }[] = [
  { id: "overview", label: "Overview", hint: "What CareerOS is" },
  { id: "workspace", label: "Workspace", hint: "Student console" },
];

export function SiteNav({ activeView, onChange }: Props) {
  return (
    <nav className="site-nav" aria-label="Primary">
      {LINKS.map((link) => (
        <button
          key={link.id}
          type="button"
          className={activeView === link.id ? "site-nav-link active" : "site-nav-link"}
          aria-current={activeView === link.id ? "page" : undefined}
          onClick={() => onChange(link.id)}
        >
          <span className="site-nav-label">{link.label}</span>
          <span className="site-nav-hint">{link.hint}</span>
        </button>
      ))}
    </nav>
  );
}
