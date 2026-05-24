from __future__ import annotations

import re

from sqlalchemy.orm import Session

from ....adapter.db.persistence.assistant.assistant_view import AssistantView
from ....models.entities import User
from ....config import LLM_API_KEY
from ..dto.assistant_dto import AssistantChatRequest, AssistantChatResponse, SuggestedAction
from ..rag.faq_retriever import FaqRetriever
from ..services.llm_client import complete_chat

_RETRIEVER: FaqRetriever | None = None


def _retriever() -> FaqRetriever:
    global _RETRIEVER
    if _RETRIEVER is None:
        _RETRIEVER = FaqRetriever()
    return _RETRIEVER


def _sanitize_user_message(message: str) -> str:
    cleaned = message.strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned[:2000]


def _score_summary(scorecard) -> str | None:
    if scorecard is None:
        return None
    return (
        f"Latest scorecard #{scorecard.id}: overall {round(scorecard.overall_score)} "
        f"({scorecard.bucket}), JD match {round(scorecard.jd_match)}, "
        f"ATS safety {round(scorecard.ats_safety)}."
    )


def _suggested_actions(message: str) -> list[SuggestedAction]:
    lower = message.lower()
    actions: list[SuggestedAction] = []
    if any(k in lower for k in ("upload", "resume", "parse")):
        actions.append(SuggestedAction(label="Upload resume", href="/workspace?tab=resume"))
    if any(k in lower for k in ("jd", "match", "scan", "job description")):
        actions.append(SuggestedAction(label="JD Match Scan", href="/workspace?tab=scan"))
    if any(k in lower for k in ("rewrite", "proof", "bullet")):
        actions.append(SuggestedAction(label="Proof-linked rewrite", href="/workspace?tab=rewrite"))
    if any(k in lower for k in ("job", "apply", "opening")):
        actions.append(SuggestedAction(label="Browse jobs", href="/workspace?tab=jobs"))
    if any(k in lower for k in ("build", "wizard", "fresher")):
        actions.append(SuggestedAction(label="Builder wizard", href="/workspace?tab=builder"))
    if not actions:
        actions.append(SuggestedAction(label="Open workspace", href="/workspace"))
    return actions


def _faq_answer(chunks: list[tuple[str, str]], score_summary: str | None) -> str:
    parts = [text for _, text in chunks]
    body = " ".join(parts) if parts else "I can help with resume upload, JD matching, rewrites, jobs, and readiness scores."
    if score_summary:
        return f"{body} {score_summary}"
    return body


_SYSTEM_PROMPT = (
    "You are CareerOS Campus Assistant for Indian college placement prep. "
    "Answer using ONLY the provided FAQ excerpts and the student's own score summary. "
    "Do not invent scores or claim fabrications are allowed. "
    "Keep answers under 120 words. Suggest workspace tabs when relevant."
)


class ChatHandler:
    def __init__(self, db: Session) -> None:
        self._view = AssistantView(db)

    async def execute(self, user: User, payload: AssistantChatRequest) -> AssistantChatResponse:
        message = _sanitize_user_message(payload.message)
        scorecard = self._view.latest_scorecard_for_user(user.id)
        summary = _score_summary(scorecard)
        chunks = _retriever().retrieve(message)
        sources = [chunk_id for chunk_id, _ in chunks]
        actions = _suggested_actions(message)

        if LLM_API_KEY:
            context = "\n".join(f"- {text}" for _, text in chunks)
            user_prompt = f"FAQ:\n{context}\n\nStudent score: {summary or 'none yet'}\n\nQuestion: {message}"
            answer = await complete_chat(system=_SYSTEM_PROMPT, user=user_prompt)
            return AssistantChatResponse(
                answer=answer,
                sources=sources,
                suggested_actions=actions,
                score_summary=summary,
                provider="llm",
            )

        return AssistantChatResponse(
            answer=_faq_answer(chunks, summary),
            sources=sources,
            suggested_actions=actions,
            score_summary=summary,
            provider="faq",
        )
