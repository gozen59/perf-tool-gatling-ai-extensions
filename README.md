# Gatling AI Extensions — Cursor

[<picture><source media="(prefers-color-scheme: dark)" srcset="https://docs.gatling.io/images/logo-gatling.svg"><img src="https://docs.gatling.io/images/logo-gatling-noir.svg" alt="Gatling" width="50%"></picture>](https://gatling.io)

**Cursor** pack for Gatling Enterprise: **Agent Skills** (`.cursor/skills/`) and the **MCP server** (`@gatling.io/gatling-mcp-server`). MCP server source lives in [`mcp-servers/gatling`](mcp-servers/gatling).

This repository is a **fork** of Gatling’s official **[gatling-ai-extensions](https://github.com/gatling/gatling-ai-extensions)** project, which targets **Claude Code** (marketplace plugin, skills, and MCP). Here the same capabilities are adapted for **Cursor** (Agent Skills, rules, VSIX pack) while retaining the upstream MCP server sources and reference skills.

> Skill definitions aligned with the official repo are kept under [`reference/gatling-skills`](reference/gatling-skills) for syncing and regenerating Cursor `SKILL.md` files.

## Sharing the pack (VSIX file)

The extension in [`vscode-gatling-cursor-pack/`](vscode-gatling-cursor-pack/) produces a `.vsix` for Cursor or VS Code. It copies `.cursor/`, `mcp.json.example`, and `AGENTS.md` into the open workspace via a command palette action.

**Official build (recommended):** GitHub Actions workflow [`.github/workflows/build-vsix.yml`](.github/workflows/build-vsix.yml) runs on push (when relevant paths change) and on **workflow_dispatch**. Download the **`gatling-cursor-pack-vsix`** artifact from the run’s **Summary** page.

**Local build (optional):** your machine keeps `vscode-gatling-cursor-pack/pack/`, `node_modules/`, and `*.vsix` for development; those paths are listed in [`.gitignore`](.gitignore) so they are **not pushed** to GitHub.

```bash
./scripts/bundle-vsix-pack.sh
cd vscode-gatling-cursor-pack && npm install && npm run package
```

Install the `.vsix` via **Extensions → Install from VSIX…**, then run **Gatling Cursor Pack: Install into workspace**. See [`vscode-gatling-cursor-pack/README.md`](vscode-gatling-cursor-pack/README.md) for details.

> If `pack/` was ever committed before, stop tracking it once: `git rm -r --cached vscode-gatling-cursor-pack/pack` then commit.

## Installation (Cursor)

1. **Open this repository in Cursor** — project skills load from `.cursor/skills/`.
2. **Configure the Gatling MCP server**
   - Merge [`mcp.json.example`](mcp.json.example) into your Cursor MCP config (**Settings → MCP**, often `~/.cursor/mcp.json`) or add the `gatling` entry.
   - Replace `REPLACE_WITH_YOUR_TOKEN` with a valid token, or ensure `GATLING_ENTERPRISE_API_TOKEN` is set in the MCP process environment (never commit secrets).
   - Restart Cursor or reload MCP servers.
3. **Prerequisite** — `GATLING_ENTERPRISE_API_TOKEN` with at least the **Configure** role on Gatling Enterprise.

See [`AGENTS.md`](AGENTS.md) for the skill list and documentation links.

**Other repositories**: copy or symlink the `gatling-*` folders from `.cursor/skills/` into `~/.cursor/skills/` to enable them in another workspace.

## Maintenance

After updating skill bundles from [gatling/gatling-ai-extensions](https://github.com/gatling/gatling-ai-extensions) (copy into `reference/gatling-skills/`):

1. `./scripts/sync-cursor-skills-from-upstream.sh` — syncs `references/`, `assets/`, `LICENSE` into `.cursor/skills/` without overwriting `SKILL.md`.
2. `./scripts/regenerate-cursor-skill-md.sh` — regenerates Cursor `SKILL.md` files; review `git diff` before committing.

The rule [`.cursor/rules/gatling-enterprise.mdc`](.cursor/rules/gatling-enterprise.mdc) applies when matching **globs** are in context (`.gatling`, skills, `mcp-servers`, `reference/gatling-skills`).

## Repository layout

- `./.cursor/skills/gatling-*` — Cursor Agent Skills (derived from `reference/gatling-skills`)
- `./.cursor/rules/` — project rules (e.g. `gatling-enterprise.mdc`)
- `./reference/gatling-skills` — reference skill bundles aligned with upstream Gatling (for sync / regeneration)
- `./mcp-servers/gatling` — MCP server source published to npm
- `./scripts/` — sync, regeneration, and VSIX bundle (`bundle-vsix-pack.sh`, etc.)
- `./vscode-gatling-cursor-pack/` — VSIX extension **source** only (`extension.js`, `package.json`, …). Local `pack/`, `node_modules/`, and `*.vsix` are [gitignored](.gitignore); CI builds the VSIX via [`.github/workflows/build-vsix.yml`](.github/workflows/build-vsix.yml).
- `./.github/workflows/` — includes `build-vsix.yml` (artifact `gatling-cursor-pack-vsix`)

## Requirements

A valid `GATLING_ENTERPRISE_API_TOKEN` with at least the **Configure** role.

## Documentation

[Gatling — AI extensions](https://docs.gatling.io/integrations/ai/extensions/overview/)

## Help

[Gatling documentation](https://docs.gatling.io) · [Community forum](https://community.gatling.io) · [Gatling product issues](https://github.com/gatling/gatling/issues)
