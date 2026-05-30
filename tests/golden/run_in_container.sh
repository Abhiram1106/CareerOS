#!/usr/bin/env bash
# Run the golden discrimination suite inside the core-api container, where
# careeros_scoring and its runtime deps are installed.
#
# Usage (from repo root):
#   bash tests/golden/run_in_container.sh
#
# The repo is not bind-mounted into the container, so we copy the golden tests
# in and execute a self-contained runner. This keeps the gate reproducible
# without adding a pytest dependency to the production image.
set -euo pipefail

SVC="${GOLDEN_SVC:-core-api}"

docker compose cp tests/golden/corpus.py "${SVC}:/tmp/corpus.py"
docker compose cp tests/golden/_runner.py "${SVC}:/tmp/_runner.py"
# Double slash stops Git Bash / MSYS from rewriting the container-side path.
docker compose exec -T "${SVC}" python //tmp/_runner.py
