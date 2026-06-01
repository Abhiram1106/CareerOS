"use client";

import { useCallback, useEffect, useState } from "react";

import { getStoredAuth } from "../../lib/auth";
import { toErrorMessage } from "../../lib/errors";
import { sendAssistantMessage } from "./assistantService";
import type { AssistantChatResult } from "./types";

type ChatMessage = {
  role: "user" | "assistant";
  text: string;
  meta?: AssistantChatResult;
};

const CHAT_KEY = "cos_assistant_chat_v1";

export function useAssistantChat() {
  const token = getStoredAuth()?.token ?? "";
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (typeof window === "undefined") return;
    try {
      const raw = localStorage.getItem(CHAT_KEY);
      if (!raw) return;
      const parsed = JSON.parse(raw) as ChatMessage[];
      setMessages(parsed.slice(-20));
    } catch {
      setMessages([]);
    }
  }, []);

  useEffect(() => {
    if (typeof window === "undefined") return;
    try {
      localStorage.setItem(CHAT_KEY, JSON.stringify(messages.slice(-20)));
    } catch {
      // noop
    }
  }, [messages]);

  const send = useCallback(
    async (message: string) => {
      if (!token || !message.trim()) return;
      setLoading(true);
      setError(null);
      setMessages((prev) => [...prev, { role: "user", text: message.trim() }]);
      try {
        const result = await sendAssistantMessage(token, message.trim());
        setMessages((prev) => [...prev, { role: "assistant", text: result.answer, meta: result }]);
      } catch (err) {
        setError(toErrorMessage(err, "Assistant unavailable"));
      } finally {
        setLoading(false);
      }
    },
    [token]
  );

  return { messages, loading, error, send, canChat: Boolean(token) };
}
