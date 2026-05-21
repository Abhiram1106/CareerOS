"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { getStoredAuth, clearAuth, type AuthUser } from "../../lib/auth";

const DEMO = process.env.NEXT_PUBLIC_DEMO === "true";

export default function AppLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const [user, setUser] = useState<AuthUser | null>(null);
  const [checked, setChecked] = useState(false);

  useEffect(() => {
    const stored = getStoredAuth();
    if (!stored) {
      router.replace("/login");
      return;
    }
    setUser(stored);
    setChecked(true);
  }, [router]);

  function handleSignOut() {
    clearAuth();
    router.replace("/login");
  }

  if (!checked) {
    return (
      <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", background: "#f7f9fc" }}>
        <div style={{ fontFamily: "var(--font-mono)", fontSize: "0.8rem", color: "#717783" }}>Loading…</div>
      </div>
    );
  }

  const isOfficer = user?.role === "officer";
  const initials = user?.full_name?.split(" ").map(w => w[0]).join("").slice(0, 2).toUpperCase() ?? "??";

  const navLinks = isOfficer
    ? [
        { href: "/officer", label: "Dashboard" },
        { href: "/officer/batches", label: "Batches" },
        { href: "/officer/review", label: "Review Queue" },
        { href: "/lab", label: "Intel Lab" },
      ]
    : [
        { href: "/", label: "Overview" },
        { href: "/workspace", label: "Workspace" },
        { href: "/lab", label: "Intel Lab" },
      ];

  return (
    <div className="app-shell">
      {DEMO && (
        <div className="demo-banner">
          <span className="demo-banner-pill">Demo</span>
          <span>Running in demo mode — all data is synthetic. No real resumes or API calls.</span>
          <button type="button" onClick={handleSignOut} style={{ marginLeft: "auto", background: "rgba(255,255,255,0.2)", border: "none", borderRadius: 6, color: "#fff", padding: "4px 12px", cursor: "pointer", fontWeight: 700, fontSize: "0.78rem" }}>
            Exit Demo
          </button>
        </div>
      )}

      <nav className="app-nav" aria-label="Main navigation">
        <div className="app-nav-inner">
          <Link href="/" className="app-nav-brand" aria-label="CareerOS home">
            <div className="app-nav-brand-icon">CO</div>
            <span className="app-nav-brand-text">CareerOS Campus AI</span>
          </Link>

          <div className="app-nav-links" role="navigation">
            {navLinks.map(({ href, label }) => (
              <Link
                key={href}
                href={href}
                className={`app-nav-link${pathname === href ? " active" : ""}`}
              >
                {label}
              </Link>
            ))}
          </div>

          <div className="app-nav-end">
            <div className="app-nav-user-pill" title={user?.email}>
              <div className="app-nav-user-avatar" aria-hidden="true">{initials}</div>
              <span style={{ maxWidth: 140, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                {user?.full_name}
              </span>
              {user?.role === "officer" && (
                <span style={{ background: "#d3e4ff", color: "#00589c", borderRadius: 9999, padding: "1px 7px", fontSize: "0.68rem", fontWeight: 700, flexShrink: 0 }}>TPO</span>
              )}
            </div>
            <button type="button" className="app-nav-signout" onClick={handleSignOut} aria-label="Sign out">
              Sign out
            </button>
          </div>
        </div>
      </nav>

      <main style={{ flex: 1 }}>
        {children}
      </main>
    </div>
  );
}
