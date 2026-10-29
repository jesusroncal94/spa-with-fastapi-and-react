#!/usr/bin/env bash
# The one check agents and CI run before calling a change done.
set -euo pipefail
cd "$(dirname "$0")/.."

docker compose --profile test run --rm --build tests uv run ruff check src tests
docker compose --profile test run --rm --build tests
docker compose run --rm --no-deps --build web npm run typecheck
