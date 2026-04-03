#!/usr/bin/env bash
# Refresh vscode-gatling-cursor-pack/pack/ from the repo root (before vsce package).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EXT="$ROOT/vscode-gatling-cursor-pack"
mkdir -p "$EXT/pack"
rsync -a --delete "$ROOT/.cursor/" "$EXT/pack/.cursor/"
cp "$ROOT/mcp.json.example" "$ROOT/AGENTS.md" "$EXT/pack/"
echo "OK: $EXT/pack is ready — run npm run package in vscode-gatling-cursor-pack."
