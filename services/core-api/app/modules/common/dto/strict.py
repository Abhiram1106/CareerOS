from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class StrictModel(BaseModel):
    """Reject unknown JSON fields on inbound API payloads."""

    model_config = ConfigDict(extra="forbid")
