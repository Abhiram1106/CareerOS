"""sklearnex must patch sklearn before any sklearn import."""

from __future__ import annotations


def patch_sklearn_if_available() -> None:
    try:
        from sklearnex import patch_sklearn

        patch_sklearn()
    except ImportError:
        pass
