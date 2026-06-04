"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import type { Certification, Education, Project, Skill, WorkExperience } from "../../../lib/api";
import { api } from "../../../lib/api";
import { getStoredAuth } from "../../../lib/auth";
import { toErrorMessage } from "../../../lib/errors";
import { useProfileSections } from "../../../hooks/useProfileSections";

// ── Reusable primitives ────────────────────────────────────────────────────

function Field({ label, id, children }: { label: string; id: string; children: React.ReactNode }) {
  return (
    <div className="auth-field">
      <label className="auth-label" htmlFor={id}>{label}</label>
      {children}
    </div>
  );
}

function SectionCard({ title, badge, children }: { title: string; badge?: string; children: React.ReactNode }) {
  return (
    <div className="content-card" style={{ marginBottom: 20 }}>
      <div className="content-card-header">
        <h2 className="content-card-title">{title}</h2>
        {badge ? <span className="chip chip-mono">{badge}</span> : null}
      </div>
      <div className="content-card-body">{children}</div>
    </div>
  );
}

function SaveRow({ saving, saved, label = "Save" }: { saving: boolean; saved: boolean; label?: string }) {
  return (
    <div style={{ display: "flex", gap: 10, alignItems: "center", marginTop: 14 }}>
      <button type="submit" className="btn-primary" disabled={saving}>
        {saving ? "Saving…" : label}
      </button>
      {saved && <span style={{ color: "#16a34a", fontSize: "0.85rem", fontWeight: 600 }}>✓ Saved</span>}
    </div>
  );
}

function DeleteBtn({ onClick }: { onClick: () => void }) {
  return (
    <button
      type="button"
      className="btn-secondary"
      style={{ color: "#93000a", borderColor: "#f4b8bb", fontSize: "0.8rem", padding: "4px 10px" }}
      onClick={onClick}
    >
      Remove
    </button>
  );
}

function EntryCard({ children, onDelete }: { children: React.ReactNode; onDelete: () => void }) {
  return (
    <div style={{ border: "1px solid rgba(192,199,211,0.45)", borderRadius: 10, padding: "14px 16px", marginBottom: 12, position: "relative", background: "#fafbfc" }}>
      {children}
      <div style={{ display: "flex", justifyContent: "flex-end", marginTop: 8 }}>
        <DeleteBtn onClick={onDelete} />
      </div>
    </div>
  );
}

// ── Work Experience ────────────────────────────────────────────────────────

const EMPTY_WORK: Omit<WorkExperience, "id" | "sort_order"> = {
  company: "", title: "", employment_type: "Internship", location: "",
  start_date: "", end_date: "", is_current: false, bullets: [""],
};

function WorkSection({ ps }: { ps: ReturnType<typeof useProfileSections> }) {
  const [form, setForm] = useState({ ...EMPTY_WORK });
  const [adding, setAdding] = useState(false);

  const set = (k: keyof typeof form) => (v: unknown) =>
    setForm((p) => ({ ...p, [k]: v }));

  const setBullet = (i: number, v: string) =>
    setForm((p) => {
      const b = [...p.bullets]; b[i] = v; return { ...p, bullets: b };
    });

  const addBullet = () =>
    setForm((p) => ({ ...p, bullets: p.bullets.length < 8 ? [...p.bullets, ""] : p.bullets }));

  const removeBullet = (i: number) =>
    setForm((p) => ({ ...p, bullets: p.bullets.filter((_, j) => j !== i) }));

  async function handleAdd(e: React.FormEvent) {
    e.preventDefault();
    if (!form.company || !form.title || !form.start_date) return;
    setAdding(true);
    await ps.addWorkExp({ ...form, bullets: form.bullets.filter(Boolean) });
    setForm({ ...EMPTY_WORK });
    setAdding(false);
  }

  return (
    <SectionCard title="Work Experience & Internships">
      {(ps.profile?.work_experiences ?? []).map((w) => (
        <EntryCard key={w.id} onDelete={() => void ps.deleteWorkExp(w.id)}>
          <p style={{ fontWeight: 700, fontSize: "0.95rem", marginBottom: 2 }}>{w.title} — {w.company}</p>
          <p style={{ fontSize: "0.82rem", color: "#5c6570" }}>{w.employment_type} · {w.location} · {w.start_date}–{w.is_current ? "Present" : w.end_date}</p>
          {w.bullets.filter(Boolean).map((b, i) => (
            <p key={i} style={{ fontSize: "0.82rem", color: "#3a4350", marginTop: 4 }}>• {b}</p>
          ))}
        </EntryCard>
      ))}

      <form onSubmit={handleAdd}>
        <p style={{ fontSize: "0.85rem", fontWeight: 600, color: "#414752", marginBottom: 10 }}>
          Add experience
        </p>
        <div className="settings-grid">
          <Field label="Company *" id="we-co">
            <input id="we-co" className="auth-input" value={form.company} onChange={(e) => set("company")(e.target.value)} placeholder="Razorpay" required />
          </Field>
          <Field label="Role/Title *" id="we-ti">
            <input id="we-ti" className="auth-input" value={form.title} onChange={(e) => set("title")(e.target.value)} placeholder="Software Engineering Intern" required />
          </Field>
          <Field label="Type" id="we-et">
            <select id="we-et" className="auth-input workspace-select" value={form.employment_type} onChange={(e) => set("employment_type")(e.target.value)}>
              {["Internship", "Full-time", "Part-time", "Contract", "Freelance"].map((t) => <option key={t}>{t}</option>)}
            </select>
          </Field>
          <Field label="Location" id="we-loc">
            <input id="we-loc" className="auth-input" value={form.location} onChange={(e) => set("location")(e.target.value)} placeholder="Bengaluru" />
          </Field>
          <Field label="Start *" id="we-sd">
            <input id="we-sd" className="auth-input" value={form.start_date} onChange={(e) => set("start_date")(e.target.value)} placeholder="Jun 2024" required />
          </Field>
          <Field label="End (blank if current)" id="we-ed">
            <input id="we-ed" className="auth-input" value={form.end_date} onChange={(e) => set("end_date")(e.target.value)} placeholder="Aug 2024" />
          </Field>
        </div>
        <div style={{ marginTop: 12 }}>
          <p className="auth-label" style={{ marginBottom: 6 }}>Bullets (start with an action verb)</p>
          {form.bullets.map((b, i) => (
            <div key={i} style={{ display: "flex", gap: 8, marginBottom: 6 }}>
              <input className="auth-input" style={{ flex: 1 }} value={b} onChange={(e) => setBullet(i, e.target.value)} placeholder="Built payment API in Python, reducing latency by 40%" />
              {form.bullets.length > 1 && (
                <button type="button" className="btn-secondary" style={{ padding: "0 10px" }} onClick={() => removeBullet(i)}>✕</button>
              )}
            </div>
          ))}
          {form.bullets.length < 8 && (
            <button type="button" className="btn-secondary" style={{ fontSize: "0.8rem", marginTop: 4 }} onClick={addBullet}>+ Add bullet</button>
          )}
        </div>
        <SaveRow saving={adding} saved={!!ps.saved.work_add} label="Add experience" />
      </form>
    </SectionCard>
  );
}

// ── Education ──────────────────────────────────────────────────────────────

const EMPTY_EDU: Omit<Education, "id" | "sort_order"> = {
  institution: "", degree: "", field: "", start_year: null,
  end_year: null, cgpa: null, percentage: null, coursework: "",
};

function EducationSection({ ps }: { ps: ReturnType<typeof useProfileSections> }) {
  const [form, setForm] = useState({ ...EMPTY_EDU });
  const [adding, setAdding] = useState(false);

  const set = (k: keyof typeof form) => (v: unknown) =>
    setForm((p) => ({ ...p, [k]: v }));

  const num = (k: keyof typeof form) => (e: React.ChangeEvent<HTMLInputElement>) =>
    set(k)(e.target.value === "" ? null : Number(e.target.value));

  async function handleAdd(e: React.FormEvent) {
    e.preventDefault();
    if (!form.institution || !form.degree || !form.field) return;
    setAdding(true);
    await ps.addEducation(form);
    setForm({ ...EMPTY_EDU });
    setAdding(false);
  }

  return (
    <SectionCard title="Education">
      {(ps.profile?.educations ?? []).map((e) => (
        <EntryCard key={e.id} onDelete={() => void ps.deleteEducation(e.id)}>
          <p style={{ fontWeight: 700, fontSize: "0.95rem", marginBottom: 2 }}>{e.degree} in {e.field}</p>
          <p style={{ fontSize: "0.82rem", color: "#5c6570" }}>
            {e.institution} · {e.start_year}–{e.end_year}
            {e.cgpa ? ` · CGPA ${e.cgpa}` : ""}
            {e.percentage ? ` · ${e.percentage}%` : ""}
          </p>
        </EntryCard>
      ))}

      <form onSubmit={handleAdd}>
        <p style={{ fontSize: "0.85rem", fontWeight: 600, color: "#414752", marginBottom: 10 }}>Add education</p>
        <div className="settings-grid">
          <Field label="Institution *" id="ed-inst">
            <input id="ed-inst" className="auth-input" value={form.institution} onChange={(e) => set("institution")(e.target.value)} placeholder="NIT Trichy" required />
          </Field>
          <Field label="Degree *" id="ed-deg">
            <input id="ed-deg" className="auth-input" value={form.degree} onChange={(e) => set("degree")(e.target.value)} placeholder="B.Tech" required />
          </Field>
          <Field label="Field of study *" id="ed-fld">
            <input id="ed-fld" className="auth-input" value={form.field} onChange={(e) => set("field")(e.target.value)} placeholder="Computer Science" required />
          </Field>
          <Field label="Start year" id="ed-sy">
            <input id="ed-sy" type="number" min="2000" max="2030" className="auth-input" value={form.start_year ?? ""} onChange={num("start_year")} placeholder="2021" />
          </Field>
          <Field label="End year" id="ed-ey">
            <input id="ed-ey" type="number" min="2000" max="2030" className="auth-input" value={form.end_year ?? ""} onChange={num("end_year")} placeholder="2025" />
          </Field>
          <Field label="CGPA (out of 10)" id="ed-cg">
            <input id="ed-cg" type="number" step="0.01" min="0" max="10" className="auth-input" value={form.cgpa ?? ""} onChange={num("cgpa")} placeholder="8.4" />
          </Field>
        </div>
        <SaveRow saving={adding} saved={!!ps.saved.edu_add} label="Add education" />
      </form>
    </SectionCard>
  );
}

// ── Skills ─────────────────────────────────────────────────────────────────

const CATEGORIES = ["technical", "soft", "tool", "language"] as const;
const PROFICIENCIES = ["beginner", "intermediate", "advanced", "expert"] as const;

function SkillsSection({ ps }: { ps: ReturnType<typeof useProfileSections> }) {
  const [name, setName] = useState("");
  const [cat, setCat] = useState<"technical" | "soft" | "tool" | "language">("technical");
  const [prof, setProf] = useState<"beginner" | "intermediate" | "advanced" | "expert">("intermediate");

  const existing = ps.profile?.skills ?? [];

  async function handleAdd(e: React.FormEvent) {
    e.preventDefault();
    if (!name.trim()) return;
    const trimmed = name.trim();
    if (existing.some((s) => s.name.toLowerCase() === trimmed.toLowerCase())) return;
    const next = [...existing.map(({ id: _id, ...s }) => s), { name: trimmed, category: cat, proficiency: prof }];
    await ps.bulkSaveSkills(next);
    setName("");
  }

  return (
    <SectionCard title="Skills" badge="Used in JD skill recall scoring">
      <div style={{ display: "flex", flexWrap: "wrap", gap: 8, minHeight: 36, marginBottom: 16 }}>
        {existing.map((s) => (
          <span
            key={s.id}
            style={{
              display: "inline-flex", alignItems: "center", gap: 6,
              background: s.category === "technical" ? "#e0f0ff" : s.category === "tool" ? "#f0f4e0" : s.category === "language" ? "#f4e8ff" : "#f0f0f0",
              borderRadius: 9999, padding: "4px 10px 4px 12px", fontSize: "0.82rem",
              border: "1px solid rgba(0,0,0,0.08)",
            }}
          >
            <span style={{ fontWeight: 500 }}>{s.name}</span>
            <span style={{ fontSize: "0.72rem", color: "#717783" }}>{s.proficiency}</span>
            <button
              type="button"
              style={{ background: "none", border: "none", cursor: "pointer", color: "#717783", fontSize: "0.9rem", padding: 0, lineHeight: 1 }}
              onClick={() => void ps.deleteSkill(s.id)}
              aria-label={`Remove ${s.name}`}
            >
              ×
            </button>
          </span>
        ))}
        {existing.length === 0 && <span style={{ color: "#a0a8b0", fontSize: "0.85rem" }}>No skills added yet</span>}
      </div>

      <form onSubmit={handleAdd} style={{ display: "flex", gap: 8, flexWrap: "wrap", alignItems: "flex-end" }}>
        <div className="auth-field" style={{ flex: "2 1 160px", margin: 0 }}>
          <label className="auth-label" htmlFor="sk-name">Skill name</label>
          <input id="sk-name" className="auth-input" value={name} onChange={(e) => setName(e.target.value)} placeholder="Python, Docker, SQL…" />
        </div>
        <div className="auth-field" style={{ flex: "1 1 110px", margin: 0 }}>
          <label className="auth-label" htmlFor="sk-cat">Category</label>
          <select id="sk-cat" className="auth-input workspace-select" value={cat} onChange={(e) => setCat(e.target.value as typeof cat)}>
            {CATEGORIES.map((c) => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>
        <div className="auth-field" style={{ flex: "1 1 120px", margin: 0 }}>
          <label className="auth-label" htmlFor="sk-prof">Proficiency</label>
          <select id="sk-prof" className="auth-input workspace-select" value={prof} onChange={(e) => setProf(e.target.value as typeof prof)}>
            {PROFICIENCIES.map((p) => <option key={p} value={p}>{p}</option>)}
          </select>
        </div>
        <button type="submit" className="btn-primary" disabled={ps.saving.skills} style={{ marginBottom: 2 }}>
          {ps.saving.skills ? "Saving…" : "+ Add"}
        </button>
        {ps.saved.skills && <span style={{ color: "#16a34a", fontSize: "0.82rem", alignSelf: "center" }}>✓ Saved</span>}
      </form>
    </SectionCard>
  );
}

// ── Projects ───────────────────────────────────────────────────────────────

const EMPTY_PROJ: Omit<Project, "id" | "sort_order"> = {
  title: "", description: "", tech_stack: [], github_url: "", live_url: "", start_date: "", end_date: "",
};

function ProjectsSection({ ps }: { ps: ReturnType<typeof useProfileSections> }) {
  const [form, setForm] = useState({ ...EMPTY_PROJ, _tech: "" });
  const [adding, setAdding] = useState(false);

  const set = (k: string) => (v: unknown) =>
    setForm((p) => ({ ...p, [k]: v }));

  async function handleAdd(e: React.FormEvent) {
    e.preventDefault();
    if (!form.title) return;
    const tech = form._tech ? form._tech.split(",").map((t) => t.trim()).filter(Boolean) : form.tech_stack;
    setAdding(true);
    await ps.addProject({ title: form.title, description: form.description, tech_stack: tech, github_url: form.github_url, live_url: form.live_url, start_date: form.start_date, end_date: form.end_date });
    setForm({ ...EMPTY_PROJ, _tech: "" });
    setAdding(false);
  }

  return (
    <SectionCard title="Projects">
      {(ps.profile?.projects ?? []).map((p) => (
        <EntryCard key={p.id} onDelete={() => void ps.deleteProject(p.id)}>
          <p style={{ fontWeight: 700, fontSize: "0.95rem", marginBottom: 2 }}>{p.title}</p>
          {p.description && <p style={{ fontSize: "0.82rem", color: "#414752", marginBottom: 4 }}>{p.description}</p>}
          {p.tech_stack.length > 0 && (
            <p style={{ fontSize: "0.78rem", color: "#5c6570" }}>
              {p.tech_stack.join(" · ")}
              {p.github_url && <> · <a href={p.github_url} target="_blank" rel="noreferrer" style={{ color: "#0071c5" }}>GitHub</a></>}
            </p>
          )}
        </EntryCard>
      ))}

      <form onSubmit={handleAdd}>
        <p style={{ fontSize: "0.85rem", fontWeight: 600, color: "#414752", marginBottom: 10 }}>Add project</p>
        <div className="settings-grid">
          <Field label="Project title *" id="pr-ti">
            <input id="pr-ti" className="auth-input" value={form.title} onChange={(e) => set("title")(e.target.value)} placeholder="Distributed Cache" required />
          </Field>
          <Field label="Tech stack (comma-separated)" id="pr-ts">
            <input id="pr-ts" className="auth-input" value={form._tech} onChange={(e) => set("_tech")(e.target.value)} placeholder="Go, Redis, Docker" />
          </Field>
          <Field label="GitHub URL" id="pr-gh">
            <input id="pr-gh" className="auth-input" value={form.github_url} onChange={(e) => set("github_url")(e.target.value)} placeholder="https://github.com/you/repo" />
          </Field>
          <Field label="Live URL" id="pr-lu">
            <input id="pr-lu" className="auth-input" value={form.live_url} onChange={(e) => set("live_url")(e.target.value)} placeholder="https://demo.example.com" />
          </Field>
        </div>
        <div className="auth-field">
          <label className="auth-label" htmlFor="pr-desc">Description</label>
          <textarea id="pr-desc" className="jd-textarea" rows={2} value={form.description} onChange={(e) => set("description")(e.target.value)} placeholder="LRU cache in Go with Redis backing, handled 10k req/s" />
        </div>
        <SaveRow saving={adding} saved={!!ps.saved.proj_add} label="Add project" />
      </form>
    </SectionCard>
  );
}

// ── Certifications ─────────────────────────────────────────────────────────

const EMPTY_CERT: Omit<Certification, "id" | "sort_order"> = {
  name: "", issuer: "", issue_date: "", expiry_date: "", credential_id: "", credential_url: "",
};

function CertificationsSection({ ps }: { ps: ReturnType<typeof useProfileSections> }) {
  const [form, setForm] = useState({ ...EMPTY_CERT });
  const [adding, setAdding] = useState(false);

  const set = (k: keyof typeof form) => (v: string) =>
    setForm((p) => ({ ...p, [k]: v }));

  async function handleAdd(e: React.FormEvent) {
    e.preventDefault();
    if (!form.name || !form.issuer) return;
    setAdding(true);
    await ps.addCertification(form);
    setForm({ ...EMPTY_CERT });
    setAdding(false);
  }

  return (
    <SectionCard title="Certifications">
      {(ps.profile?.certifications ?? []).map((c) => (
        <EntryCard key={c.id} onDelete={() => void ps.deleteCertification(c.id)}>
          <p style={{ fontWeight: 700, fontSize: "0.95rem", marginBottom: 2 }}>{c.name}</p>
          <p style={{ fontSize: "0.82rem", color: "#5c6570" }}>
            {c.issuer}{c.issue_date ? ` · ${c.issue_date}` : ""}
            {c.credential_url && <> · <a href={c.credential_url} target="_blank" rel="noreferrer" style={{ color: "#0071c5" }}>Verify</a></>}
          </p>
        </EntryCard>
      ))}

      <form onSubmit={handleAdd}>
        <p style={{ fontSize: "0.85rem", fontWeight: 600, color: "#414752", marginBottom: 10 }}>Add certification</p>
        <div className="settings-grid">
          <Field label="Certification name *" id="ce-na">
            <input id="ce-na" className="auth-input" value={form.name} onChange={(e) => set("name")(e.target.value)} placeholder="AWS Solutions Architect" required />
          </Field>
          <Field label="Issuer *" id="ce-is">
            <input id="ce-is" className="auth-input" value={form.issuer} onChange={(e) => set("issuer")(e.target.value)} placeholder="Amazon Web Services" required />
          </Field>
          <Field label="Issue date" id="ce-id">
            <input id="ce-id" className="auth-input" value={form.issue_date} onChange={(e) => set("issue_date")(e.target.value)} placeholder="Jun 2024" />
          </Field>
          <Field label="Credential URL" id="ce-ur">
            <input id="ce-ur" className="auth-input" value={form.credential_url} onChange={(e) => set("credential_url")(e.target.value)} placeholder="https://verify.example.com/abc" />
          </Field>
        </div>
        <SaveRow saving={adding} saved={!!ps.saved.cert_add} label="Add certification" />
      </form>
    </SectionCard>
  );
}

// ── Social links ───────────────────────────────────────────────────────────

function LinksSection({ ps }: { ps: ReturnType<typeof useProfileSections> }) {
  const u = ps.profile?.user;
  const [links, setLinks] = useState({ phone: u?.phone ?? "", linkedin_url: u?.linkedin_url ?? "", github_url: u?.github_url ?? "", portfolio_url: u?.portfolio_url ?? "" });

  // Sync when profile loads
  const loaded = !!u;
  if (loaded && links.phone === "" && u.phone !== "") {
    setLinks({ phone: u.phone, linkedin_url: u.linkedin_url, github_url: u.github_url, portfolio_url: u.portfolio_url });
  }

  async function handleSave(e: React.FormEvent) {
    e.preventDefault();
    await ps.saveLinks(links);
  }

  return (
    <SectionCard title="Contact & Links">
      <form onSubmit={handleSave}>
        <div className="settings-grid">
          <Field label="Phone" id="lk-ph">
            <input id="lk-ph" className="auth-input" value={links.phone} onChange={(e) => setLinks((p) => ({ ...p, phone: e.target.value }))} placeholder="+91 9876543210" />
          </Field>
          <Field label="LinkedIn URL" id="lk-li">
            <input id="lk-li" className="auth-input" value={links.linkedin_url} onChange={(e) => setLinks((p) => ({ ...p, linkedin_url: e.target.value }))} placeholder="https://linkedin.com/in/yourname" />
          </Field>
          <Field label="GitHub URL" id="lk-gh">
            <input id="lk-gh" className="auth-input" value={links.github_url} onChange={(e) => setLinks((p) => ({ ...p, github_url: e.target.value }))} placeholder="https://github.com/yourname" />
          </Field>
          <Field label="Portfolio / Website" id="lk-po">
            <input id="lk-po" className="auth-input" value={links.portfolio_url} onChange={(e) => setLinks((p) => ({ ...p, portfolio_url: e.target.value }))} placeholder="https://yoursite.com" />
          </Field>
        </div>
        <SaveRow saving={!!ps.saving.links} saved={!!ps.saved.links} label="Save links" />
      </form>
    </SectionCard>
  );
}

// ── Basic profile (kept, simplified) ──────────────────────────────────────

const BRANCH_OPTIONS = ["CSE", "IT", "ECE", "EEE", "ME", "CE", "AIML", "Other"];

function BasicSection() {
  const token = getStoredAuth()?.token ?? "";
  const [data, setData] = useState({ city: "", target_role: "", professional_status: "Fresher", skills_csv: "", summary: "", experience_bullet: "", cgpa: "" as string | number, active_backlogs: 0, branch: "", grad_year: "" as string | number });
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    if (!token) return;
    void api.getProfile(token).then((p) => {
      const pr = p as typeof data & { cgpa: number | null; grad_year: number | null };
      setData({ ...pr, cgpa: pr.cgpa ?? "", grad_year: pr.grad_year ?? "" });
      setLoaded(true);
    });
  }, [token]);

  async function handleSave(e: React.FormEvent) {
    e.preventDefault();
    setSaving(true);
    try {
      await api.updateProfile(token, {
        ...data,
        cgpa: data.cgpa === "" ? null : Number(data.cgpa),
        grad_year: data.grad_year === "" ? null : Number(data.grad_year),
      });
      setSaved(true);
      setTimeout(() => setSaved(false), 2500);
    } finally {
      setSaving(false);
    }
  }

  if (!loaded) return null;

  return (
    <SectionCard title="Basic Information" badge="Used in eligibility scoring">
      <form onSubmit={handleSave}>
        <div className="settings-grid">
          <Field label="City" id="bi-ci"><input id="bi-ci" className="auth-input" value={data.city} onChange={(e) => setData((p) => ({ ...p, city: e.target.value }))} placeholder="Bengaluru" /></Field>
          <Field label="Target role" id="bi-tr"><input id="bi-tr" className="auth-input" value={data.target_role} onChange={(e) => setData((p) => ({ ...p, target_role: e.target.value }))} placeholder="Backend Engineer" /></Field>
          <Field label="CGPA (out of 10)" id="bi-cg"><input id="bi-cg" type="number" step="0.01" min="0" max="10" className="auth-input" value={data.cgpa} onChange={(e) => setData((p) => ({ ...p, cgpa: e.target.value }))} placeholder="8.4" /></Field>
          <Field label="Graduation year" id="bi-gy"><input id="bi-gy" type="number" min="2020" max="2030" className="auth-input" value={data.grad_year} onChange={(e) => setData((p) => ({ ...p, grad_year: e.target.value }))} placeholder="2025" /></Field>
          <Field label="Active backlogs" id="bi-bl"><input id="bi-bl" type="number" min="0" className="auth-input" value={data.active_backlogs} onChange={(e) => setData((p) => ({ ...p, active_backlogs: Number(e.target.value) }))} /></Field>
          <Field label="Branch" id="bi-br">
            <select id="bi-br" className="auth-input workspace-select" value={data.branch} onChange={(e) => setData((p) => ({ ...p, branch: e.target.value }))}>
              <option value="">— Select branch —</option>
              {BRANCH_OPTIONS.map((b) => <option key={b}>{b}</option>)}
            </select>
          </Field>
        </div>
        <div className="auth-field" style={{ marginTop: 12 }}>
          <label className="auth-label" htmlFor="bi-sm">Professional summary</label>
          <textarea id="bi-sm" className="jd-textarea" rows={3} value={data.summary} onChange={(e) => setData((p) => ({ ...p, summary: e.target.value }))} placeholder="2–3 sentences about your background and strongest skills." />
        </div>
        <SaveRow saving={saving} saved={saved} />
      </form>
    </SectionCard>
  );
}

// ── Completeness ring ──────────────────────────────────────────────────────

function CompletenessRing({ profile }: { profile: ReturnType<typeof useProfileSections>["profile"] }) {
  const sections = [
    { label: "Work experience", done: (profile?.work_experiences.length ?? 0) > 0 },
    { label: "Education", done: (profile?.educations.length ?? 0) > 0 },
    { label: "Skills", done: (profile?.skills.length ?? 0) >= 3 },
    { label: "Projects", done: (profile?.projects.length ?? 0) > 0 },
    { label: "Contact links", done: !!(profile?.user.linkedin_url || profile?.user.github_url) },
  ];
  const done = sections.filter((s) => s.done).length;
  const pct = Math.round((done / sections.length) * 100);
  const r = 28; const c = 2 * Math.PI * r; const d = c - (pct / 100) * c;
  return (
    <div className="content-card" style={{ marginBottom: 20 }}>
      <div className="content-card-header">
        <h2 className="content-card-title">Profile completeness</h2>
        <span className="chip chip-primary">{pct}%</span>
      </div>
      <div className="content-card-body">
        <div style={{ display: "flex", gap: 20, alignItems: "center" }}>
          <svg width="70" height="70" viewBox="0 0 70 70" aria-label={`Profile ${pct}% complete`}>
            <circle cx="35" cy="35" r={r} fill="none" stroke="#e8ecf2" strokeWidth="7" />
            <circle cx="35" cy="35" r={r} fill="none" stroke="#0071c5" strokeWidth="7" strokeLinecap="round" strokeDasharray={c} strokeDashoffset={d} transform="rotate(-90 35 35)" />
            <text x="35" y="39" textAnchor="middle" fontSize="13" fontWeight="700" fill="#00589c">{pct}%</text>
          </svg>
          <div style={{ flex: 1 }}>
            {sections.map((s) => (
              <div key={s.label} style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 4, fontSize: "0.83rem" }}>
                <span style={{ color: s.done ? "#16a34a" : "#a0a8b0", fontWeight: 700 }}>{s.done ? "✓" : "○"}</span>
                <span style={{ color: s.done ? "#1a1c20" : "#717783" }}>{s.label}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

// ── Page root ──────────────────────────────────────────────────────────────

export default function SettingsPage() {
  const ps = useProfileSections();

  if (ps.loading) {
    return (
      <div className="page-canvas">
        <div className="content-card"><div className="content-card-body">Loading profile…</div></div>
      </div>
    );
  }

  return (
    <div className="page-canvas">
      <div className="page-title-row">
        <div>
          <h1 className="page-title">Profile</h1>
          <p className="page-subtitle">Build your career profile. Every section improves your placement score.</p>
        </div>
      </div>

      {ps.error && (
        <div className="content-card" style={{ marginBottom: 16 }}>
          <div className="content-card-body" style={{ color: "#93000a" }}>{ps.error}</div>
        </div>
      )}

      <CompletenessRing profile={ps.profile} />
      <BasicSection />
      <LinksSection ps={ps} />
      <WorkSection ps={ps} />
      <EducationSection ps={ps} />
      <SkillsSection ps={ps} />
      <ProjectsSection ps={ps} />
      <CertificationsSection ps={ps} />

      <div className="content-card" style={{ marginTop: 8 }}>
        <div className="content-card-header"><h2 className="content-card-title">Privacy</h2></div>
        <div className="content-card-body">
          <Link href="/privacy/assistant" className="btn-secondary">Assistant privacy notice</Link>
        </div>
      </div>
    </div>
  );
}
