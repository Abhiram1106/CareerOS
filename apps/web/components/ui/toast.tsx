"use client";

import { CheckCircle2, Info, X, XCircle } from "lucide-react";
import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from "react";

type ToastVariant = "success" | "error" | "info";

type ToastItem = {
  id: number;
  title: string;
  message?: string;
  variant: ToastVariant;
};

type ToastInput = {
  title: string;
  message?: string;
  variant?: ToastVariant;
};

type ToastContextValue = {
  push: (input: ToastInput) => void;
};

const ToastContext = createContext<ToastContextValue | null>(null);

function ToastIcon({ variant }: { variant: ToastVariant }) {
  if (variant === "success") return <CheckCircle2 size={16} aria-hidden="true" />;
  if (variant === "error") return <XCircle size={16} aria-hidden="true" />;
  return <Info size={16} aria-hidden="true" />;
}

export function ToastProvider({ children }: { children: ReactNode }) {
  const idRef = useRef(1);
  const [toasts, setToasts] = useState<ToastItem[]>([]);

  const removeToast = useCallback((id: number) => {
    setToasts((prev) => prev.filter((toast) => toast.id !== id));
  }, []);

  const push = useCallback(
    (input: ToastInput) => {
      const id = idRef.current++;
      const toast: ToastItem = {
        id,
        title: input.title,
        message: input.message,
        variant: input.variant ?? "info",
      };
      setToasts((prev) => [toast, ...prev].slice(0, 4));
      window.setTimeout(() => removeToast(id), 3500);
    },
    [removeToast]
  );

  const value = useMemo(() => ({ push }), [push]);

  return (
    <ToastContext.Provider value={value}>
      {children}
      <div className="toast-stack" aria-live="polite" aria-atomic="false">
        {toasts.map((toast) => (
          <div key={toast.id} className={`toast-item toast-item-${toast.variant}`} role="status">
            <div className="toast-item-head">
              <span className="toast-item-icon">
                <ToastIcon variant={toast.variant} />
              </span>
              <p className="toast-item-title">{toast.title}</p>
              <button
                type="button"
                className="toast-item-close"
                aria-label="Dismiss notification"
                onClick={() => removeToast(toast.id)}
              >
                <X size={14} />
              </button>
            </div>
            {toast.message ? <p className="toast-item-message">{toast.message}</p> : null}
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}

export function useToast() {
  const ctx = useContext(ToastContext);
  if (!ctx) {
    throw new Error("useToast must be used inside ToastProvider");
  }
  return ctx;
}
