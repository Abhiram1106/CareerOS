export type SuggestedAction = {
  label: string;
  href: string;
};

export type AssistantChatResult = {
  answer: string;
  sources: string[];
  suggested_actions: SuggestedAction[];
  score_summary: string | null;
  provider: "faq" | "llm" | string;
};
