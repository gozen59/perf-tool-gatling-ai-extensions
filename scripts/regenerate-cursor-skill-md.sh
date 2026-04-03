#!/usr/bin/env bash
# Overwrite .cursor/skills/*/SKILL.md from reference/gatling-skills using adapt_upstream_skill_md.py
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"
python3 scripts/adapt_upstream_skill_md.py
echo "Review git diff on .cursor/skills/*/SKILL.md before committing."
