from __future__ import annotations

import json
from pathlib import Path

from .....config import BENCHMARK_ARTIFACT_PATH


class IntelBenchArtifactView:
    """Read-only view over measured benchmark JSON (no DB)."""

    def load_artifact(self) -> dict | None:
        path = Path(BENCHMARK_ARTIFACT_PATH)
        if not path.is_file():
            return None
        return json.loads(path.read_text(encoding="utf-8"))
