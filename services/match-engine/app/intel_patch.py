"""sklearnex must patch sklearn before any sklearn import."""

from __future__ import annotations

import os


def patch_sklearn_if_available() -> None:
    if os.getenv("SKLEARNEX_DISABLE", "false").lower() == "true":
        return
    try:
        from sklearnex import patch_sklearn

        patch_sklearn()
    except ImportError:
        pass
