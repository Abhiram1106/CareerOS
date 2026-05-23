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
