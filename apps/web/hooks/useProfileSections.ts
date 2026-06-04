"use client";

import { useCallback, useEffect, useState } from "react";
import { api, type Certification, type Education, type FullProfile, type Project, type Skill, type WorkExperience } from "../lib/api";
import { getStoredAuth } from "../lib/auth";
import { toErrorMessage } from "../lib/errors";

export type SectionKey = "work" | "education" | "skills" | "projects" | "certifications";

type State = {
  profile: FullProfile | null;
  loading: boolean;
  error: string | null;
  saving: Record<string, boolean>;
  saved: Record<string, boolean>;
};

function markSaved(setSaved: React.Dispatch<React.SetStateAction<Record<string, boolean>>>, key: string) {
  setSaved((p) => ({ ...p, [key]: true }));
  setTimeout(() => setSaved((p) => ({ ...p, [key]: false })), 2500);
}

export function useProfileSections() {
  const token = getStoredAuth()?.token ?? "";

  const [profile, setProfile] = useState<FullProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState<Record<string, boolean>>({});
  const [saved, setSaved] = useState<Record<string, boolean>>({});

  const reload = useCallback(async () => {
    if (!token) return;
    try {
      const data = await api.getFullProfile(token);
      setProfile(data);
    } catch (err) {
      setError(toErrorMessage(err, "Could not load profile"));
    } finally {
      setLoading(false);
    }
  }, [token]);

  useEffect(() => { void reload(); }, [reload]);

  // ── Work Experience ────────────────────────────────────────────────────────

  const addWorkExp = useCallback(async (payload: Omit<WorkExperience, "id" | "sort_order">) => {
    setSaving((p) => ({ ...p, work_add: true }));
    try {
      await api.addWorkExp(token, payload);
      await reload();
      markSaved(setSaved, "work_add");
    } catch (err) {
      setError(toErrorMessage(err, "Failed to add experience"));
    } finally {
      setSaving((p) => ({ ...p, work_add: false }));
    }
  }, [token, reload]);

  const updateWorkExp = useCallback(async (id: number, payload: Partial<Omit<WorkExperience, "id" | "sort_order">>) => {
    setSaving((p) => ({ ...p, [`work_${id}`]: true }));
    try {
      await api.updateWorkExp(token, id, payload);
      await reload();
      markSaved(setSaved, `work_${id}`);
    } catch (err) {
      setError(toErrorMessage(err, "Failed to update experience"));
    } finally {
      setSaving((p) => ({ ...p, [`work_${id}`]: false }));
    }
  }, [token, reload]);

  const deleteWorkExp = useCallback(async (id: number) => {
    try {
      await api.deleteWorkExp(token, id);
      await reload();
    } catch (err) {
      setError(toErrorMessage(err, "Failed to delete experience"));
    }
  }, [token, reload]);

  // ── Education ──────────────────────────────────────────────────────────────

  const addEducation = useCallback(async (payload: Omit<Education, "id" | "sort_order">) => {
    setSaving((p) => ({ ...p, edu_add: true }));
    try {
      await api.addEducation(token, payload);
      await reload();
      markSaved(setSaved, "edu_add");
    } catch (err) {
      setError(toErrorMessage(err, "Failed to add education"));
    } finally {
      setSaving((p) => ({ ...p, edu_add: false }));
    }
  }, [token, reload]);

  const updateEducation = useCallback(async (id: number, payload: Partial<Omit<Education, "id" | "sort_order">>) => {
    setSaving((p) => ({ ...p, [`edu_${id}`]: true }));
    try {
      await api.updateEducation(token, id, payload);
      await reload();
      markSaved(setSaved, `edu_${id}`);
    } catch (err) {
      setError(toErrorMessage(err, "Failed to update education"));
    } finally {
      setSaving((p) => ({ ...p, [`edu_${id}`]: false }));
    }
  }, [token, reload]);

  const deleteEducation = useCallback(async (id: number) => {
    try {
      await api.deleteEducation(token, id);
      await reload();
    } catch (err) {
      setError(toErrorMessage(err, "Failed to delete education"));
    }
  }, [token, reload]);

  // ── Skills ─────────────────────────────────────────────────────────────────

  const bulkSaveSkills = useCallback(async (skills: Omit<Skill, "id">[]) => {
    setSaving((p) => ({ ...p, skills: true }));
    try {
      await api.bulkUpsertSkills(token, skills);
      await reload();
      markSaved(setSaved, "skills");
    } catch (err) {
      setError(toErrorMessage(err, "Failed to save skills"));
    } finally {
      setSaving((p) => ({ ...p, skills: false }));
    }
  }, [token, reload]);

  const deleteSkill = useCallback(async (id: number) => {
    try {
      await api.deleteSkill(token, id);
      await reload();
    } catch (err) {
      setError(toErrorMessage(err, "Failed to delete skill"));
    }
  }, [token, reload]);

  // ── Projects ───────────────────────────────────────────────────────────────

  const addProject = useCallback(async (payload: Omit<Project, "id" | "sort_order">) => {
    setSaving((p) => ({ ...p, proj_add: true }));
    try {
      await api.addProject(token, payload);
      await reload();
      markSaved(setSaved, "proj_add");
    } catch (err) {
      setError(toErrorMessage(err, "Failed to add project"));
    } finally {
      setSaving((p) => ({ ...p, proj_add: false }));
    }
  }, [token, reload]);

  const updateProject = useCallback(async (id: number, payload: Partial<Omit<Project, "id" | "sort_order">>) => {
    setSaving((p) => ({ ...p, [`proj_${id}`]: true }));
    try {
      await api.updateProject(token, id, payload);
      await reload();
      markSaved(setSaved, `proj_${id}`);
    } catch (err) {
      setError(toErrorMessage(err, "Failed to update project"));
    } finally {
      setSaving((p) => ({ ...p, [`proj_${id}`]: false }));
    }
  }, [token, reload]);

  const deleteProject = useCallback(async (id: number) => {
    try {
      await api.deleteProject(token, id);
      await reload();
    } catch (err) {
      setError(toErrorMessage(err, "Failed to delete project"));
    }
  }, [token, reload]);

  // ── Certifications ─────────────────────────────────────────────────────────

  const addCertification = useCallback(async (payload: Omit<Certification, "id" | "sort_order">) => {
    setSaving((p) => ({ ...p, cert_add: true }));
    try {
      await api.addCertification(token, payload);
      await reload();
      markSaved(setSaved, "cert_add");
    } catch (err) {
      setError(toErrorMessage(err, "Failed to add certification"));
    } finally {
      setSaving((p) => ({ ...p, cert_add: false }));
    }
  }, [token, reload]);

  const deleteCertification = useCallback(async (id: number) => {
    try {
      await api.deleteCertification(token, id);
      await reload();
    } catch (err) {
      setError(toErrorMessage(err, "Failed to delete certification"));
    }
  }, [token, reload]);

  // ── Social links ───────────────────────────────────────────────────────────

  const saveLinks = useCallback(async (links: { phone: string; linkedin_url: string; github_url: string; portfolio_url: string }) => {
    setSaving((p) => ({ ...p, links: true }));
    try {
      await api.updateLinks(token, links);
      await reload();
      markSaved(setSaved, "links");
    } catch (err) {
      setError(toErrorMessage(err, "Failed to save links"));
    } finally {
      setSaving((p) => ({ ...p, links: false }));
    }
  }, [token, reload]);

  return {
    profile, loading, error, saving, saved,
    addWorkExp, updateWorkExp, deleteWorkExp,
    addEducation, updateEducation, deleteEducation,
    bulkSaveSkills, deleteSkill,
    addProject, updateProject, deleteProject,
    addCertification, deleteCertification,
    saveLinks,
    reload,
  };
}
