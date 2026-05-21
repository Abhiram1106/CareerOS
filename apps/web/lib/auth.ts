"use client";

export type UserRole = "student" | "officer" | "admin";

export interface AuthUser {
  token: string;
  email: string;
  full_name: string;
  role: UserRole;
}

const KEY = "cos_auth";

export function getStoredAuth(): AuthUser | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return null;
    return JSON.parse(raw) as AuthUser;
  } catch {
    return null;
  }
}

export function storeAuth(user: AuthUser): void {
  localStorage.setItem(KEY, JSON.stringify(user));
}

export function clearAuth(): void {
  localStorage.removeItem(KEY);
}

export function isAuthenticated(): boolean {
  return getStoredAuth() !== null;
}

/** Demo users for testing (bypasses real API when NEXT_PUBLIC_DEMO=true) */
export const DEMO_USERS: Record<string, AuthUser> = {
  "student@demo.cos": {
    token: "demo-student-token",
    email: "student@demo.cos",
    full_name: "Priya Sharma (Demo)",
    role: "student",
  },
  "officer@demo.cos": {
    token: "demo-officer-token",
    email: "officer@demo.cos",
    full_name: "Mr. Ramesh TPO (Demo)",
    role: "officer",
  },
};
