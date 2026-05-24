from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class AssistantChatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message: str = Field(min_length=1, max_length=2000)


class SuggestedAction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    label: str
    href: str


class AssistantChatResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    answer: str
    sources: list[str] = Field(default_factory=list)
    suggested_actions: list[SuggestedAction] = Field(default_factory=list)
    score_summary: str | None = None
    provider: str = "faq"
