#!/usr/bin/env python3
"""Export core-api OpenAPI schema to packages/contracts/openapi/."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CORE_API = ROOT / "services" / "core-api"
OUT = ROOT / "packages" / "contracts" / "openapi" / "core-api.openapi.json"

if str(CORE_API) not in sys.path:
    sys.path.insert(0, str(CORE_API))

from app.main import app  # noqa: E402


def main() -> None:
    schema = app.openapi()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(schema, indent=2), encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
