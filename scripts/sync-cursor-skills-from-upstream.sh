#!/usr/bin/env bash
# Sync non-SKILL assets from reference/gatling-skills → .cursor/skills (references/, assets/, LICENSE).
# Source tree mirrors upstream SKILL bundles; keeps Cursor-specific SKILL.md unless you regenerate.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$REPO_ROOT/reference/gatling-skills"
DST="$REPO_ROOT/.cursor/skills"

if [[ ! -d "$SRC" ]]; then
  echo "error: missing $SRC (copy skills from gatling/gatling-ai-extensions or restore reference/gatling-skills)" >&2
  exit 1
fi

mkdir -p "$DST"
for dir in "$SRC"/*; do
  [[ -d "$dir" ]] || continue
  name="$(basename "$dir")"
  mkdir -p "$DST/$name"
  rsync -a --delete --exclude=SKILL.md "$dir/" "$DST/$name/"
done

echo "OK: synced references/, assets/, LICENSE into $DST (SKILL.md files unchanged)."
