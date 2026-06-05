"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useMemo, useRef, useState } from "react";
import {
  Bot,
  BriefcaseBusiness,
  ClipboardList,
  LayoutDashboard,
  PenLine,
  Settings,
  Sparkles,
  FileText,
  FlaskConical,
  LogOut,
} from "lucide-react";
import { api } from "../../lib/api";
import { clearAuth, getStoredAuth, type AuthUser } from "../../lib/auth";
import { useToast } from "../../components/ui/toast";

type NavItem = { href: string; label: string; icon: React.ReactNode; startsWith?: string };

const PRIMARY_NAV: NavItem[] = [
  { href: "/dashboard", label: "Dashboard", icon: <LayoutDashboard size={16} /> },
  { href: "/resume",    label: "Resume",    icon: <FileText size={16} /> },
  { href: "/match",     label: "JD Match",  icon: <Sparkles size={16} /> },
  { href: "/rewrite",   label: "Rewrite",   icon: <PenLine size={16} /> },
  { href: "/jobs",      label: "Jobs",      icon: <BriefcaseBusiness size={16} /> },
  { href: "/applications", label: "Applications", icon: <ClipboardList size={16} /> },
  { href: "/assistant", label: "Assistant", icon: <Bot size={16} /> },
];

const SECONDARY_NAV: NavItem[] = [
  { href: "/lab/intel", label: "Intel Lab", icon: <FlaskConical size={16} />, startsWith: "/lab" },
  { href: "/settings",  label: "Settings",  icon: <Settings size={16} /> },
];

export default function AppLayout({ children }: { children: React.ReactNode }) {
  const router   = useRouter();
  const pathname = usePathname();
  const { push } = useToast();

  // Read auth synchronously on first render — localStorage is sync.
  // This eliminates the useEffect round-trip and the blank "Loading..." flash.
  const initialAuth = useRef(getStoredAuth());
  const [user, setUser]           = useState<AuthUser | null>(initialAuth.current);
  const [completeness, setCompleteness] = useState(0);

  // Redirect if not authenticated — fires after paint so the shell is visible first
  useEffect(() => {
    if (!initialAuth.current) {
      router.replace("/login");
    }
  }, [router]);

  // Fetch completeness in the background — does not block shell render
  useEffect(() => {
    const token = user?.token;
    if (!token) return;
    void api
      .dashboard(token)
      .then((res) => {
        const info = res as { profile_completeness: number };
        setCompleteness(info.profile_completeness ?? 0);
      })
      .catch(() => { /* non-blocking — topbar still renders at 0% */ });
  }, [user?.token]);

  const initials = useMemo(
    () =>
      user?.full_name
        ?.split(" ")
        .map((w) => w[0])
        .join("")
        .slice(0, 2)
        .toUpperCase() ?? "??",
    [user?.full_name],
  );

  const isActive = (item: NavItem) => {
    const prefix = item.startsWith ?? item.href;
    if (item.href === "/dashboard") return pathname === "/dashboard" || pathname === "/";
    return pathname === item.href || pathname?.startsWith(prefix) === true;
  };

  async function handleSignOut() {
    try {
      if (user?.token) await api.logout(user.token);
    } catch {
      // noop
    } finally {
      clearAuth();
      setUser(null);
      push({ title: "Signed out", variant: "info" });
      router.replace("/login");
    }
  }

  // If definitely unauthenticated, show nothing (redirect in flight)
  if (!user) return null;

  return (
    <div className="app-shell-v2">
      <aside className="app-rail" aria-label="Primary navigation">
        <Link href="/dashboard" className="app-rail-brand" aria-label="CareerOS dashboard">
          <div className="app-rail-brand-icon">CO</div>
          <div className="app-rail-brand-text">
            <strong>CareerOS</strong>
            <span>Campus AI</span>
          </div>
        </Link>

        <nav className="app-rail-nav">
          {PRIMARY_NAV.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`app-rail-link${isActive(item) ? " active" : ""}`}
            >
              {item.icon}
              <span>{item.label}</span>
            </Link>
          ))}
        </nav>

        <div className="app-rail-divider" />

        <nav className="app-rail-nav app-rail-nav-secondary">
          {SECONDARY_NAV.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`app-rail-link${isActive(item) ? " active" : ""}`}
            >
              {item.icon}
              <span>{item.label}</span>
            </Link>
          ))}
        </nav>
      </aside>

      <div className="app-shell-main">
        <header className="app-topbar">
          <div className="app-topbar-complete">
            <div className="app-topbar-ring" style={{ ["--complete" as string]: `${completeness}` }}>
              <span>{completeness}%</span>
            </div>
            <p>Profile completeness</p>
          </div>
          <div className="app-topbar-actions">
            <div className="app-topbar-user-pill" title={user.email}>
              <div className="app-topbar-avatar">{initials}</div>
              <span>{user.full_name}</span>
            </div>
            <button
              type="button"
              className="app-topbar-signout"
              onClick={handleSignOut}
              aria-label="Sign out"
            >
              <LogOut size={15} />
              <span>Sign out</span>
            </button>
          </div>
        </header>

        <main className="app-shell-content">
          {children}
        </main>
      </div>

      <nav className="app-bottom-nav" aria-label="Mobile navigation">
        {PRIMARY_NAV.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={`app-bottom-link${isActive(item) ? " active" : ""}`}
          >
            {item.icon}
            <span>{item.label}</span>
          </Link>
        ))}
      </nav>
    </div>
  );
}
