# Gatling AI Extensions — Cursor

[<picture><source media="(prefers-color-scheme: dark)" srcset="https://docs.gatling.io/images/logo-gatling.svg"><img src="https://docs.gatling.io/images/logo-gatling-noir.svg" alt="Gatling" width="50%"></picture>](https://gatling.io)

**Cursor** pack for Gatling Enterprise: **Agent Skills** (`.cursor/skills/`) and the **MCP server** (`@gatling.io/gatling-mcp-server`). MCP server source lives in [`mcp-servers/gatling`](mcp-servers/gatling).

This repository is a **fork** of Gatling’s official **[gatling-ai-extensions](https://github.com/gatling/gatling-ai-extensions)** project, which targets **Claude Code** (marketplace plugin, skills, and MCP). Here the same capabilities are adapted for **Cursor** (Agent Skills, rules, VSIX pack) while retaining the upstream MCP server sources and reference skills.

> Skill definitions aligned with the official repo are kept under [`reference/gatling-skills`](reference/gatling-skills) for syncing and regenerating Cursor `SKILL.md` files.

## Sharing the pack (VSIX file)

The extension in [`vscode-gatling-cursor-pack/`](vscode-gatling-cursor-pack/) produces a `.vsix` for Cursor or VS Code. It copies `.cursor/`, `mcp.json.example`, and `AGENTS.md` into the open workspace via a command palette action.

**You do not need to clone the repository** to install the extension: download only the `.vsix` (see below), then install it in Cursor.

### Install the VSIX in Cursor (no repo clone)

1. Download the `.vsix` file using **either** option below.
2. Install it in **Cursor** (the Extensions sidebar is often marketplace-only; use one of these instead):
   - **Command palette** (`Cmd+Shift+P` / `Ctrl+Shift+P`) → type **`Extensions: Install from VSIX...`** → choose the `.vsix` file; *or*
   - **Drag and drop** the `.vsix` file onto the **Extensions** side bar; *or*
   - **Terminal**: `cursor --install-extension /absolute/path/to/gatling-cursor-pack-0.1.0.vsix` (adjust path and filename; on some setups the binary is `cursor` from the CLI you installed with Cursor).
3. Open your **project folder** (**File → Open Folder**).
4. Command palette → **Gatling Cursor Pack: Install into workspace**.
5. Configure MCP using `AGENTS.md` and `mcp.json.example` in that project (and `GATLING_ENTERPRISE_API_TOKEN`).

If **`Extensions: Install from VSIX`** does not appear, update Cursor or see [Cursor forum — VSIX install](https://forum.cursor.com/t/how-to-install-vsix-format-extension/1667/).

### Where to get the `.vsix`

| Source | What it is |
|--------|------------|
| **Rolling “latest” VSIX** | Pre-release **`rolling-vsix`** (“Latest VSIX (rolling)”): updated when you **push a tag `v*`** (same workflow as below, same `.vsix` as that tag, file name `gatling-cursor-pack-<tag>.vsix`) *and* when [`.github/workflows/build-vsix.yml`](.github/workflows/build-vsix.yml) succeeds on **`main`/`master`** (then reflects the last **branch** build). Open **Releases** → that entry for a stable download without unzipping. |
| **Versioned GitHub Release** | Pushing a tag `v*` (e.g. `v0.1.0`) runs [`.github/workflows/release-vsix.yml`](.github/workflows/release-vsix.yml): creates the **Release for that tag** with **`gatling-cursor-pack-v0.1.0.vsix`** (name includes the tag) *and* refreshes **`rolling-vsix`** with the same file. |
| **Workflow artifact** | On each run, **Actions** → open that run → **Summary** → **Artifacts** → **`gatling-cursor-pack-vsix`** (zip; unzip for the `.vsix`). Handy if you need the file for a **specific** run; retention is limited (e.g. 90 days). |

**Maintainers — publish a Release:** push a tag `v*` (e.g. `git tag v0.1.0 && git push origin v0.1.0`). The [release workflow](.github/workflows/release-vsix.yml) sets `vscode-gatling-cursor-pack/package.json` **`version`** from the tag (`v0.1.0` → `0.1.0`) before packaging, so **Cursor shows that same version** for the installed extension. You can still bump `version` in the repo for local `npm run package`; CI overrides it on tag builds.

**Local build (optional):** your machine can keep `vscode-gatling-cursor-pack/pack/`, `node_modules/`, and `*.vsix`; those paths are in [`.gitignore`](.gitignore) so they are not pushed.

```bash
./scripts/bundle-vsix-pack.sh
cd vscode-gatling-cursor-pack && npm install && npm run package
```

See [`vscode-gatling-cursor-pack/README.md`](vscode-gatling-cursor-pack/README.md) for maintainer details.

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
- `./.github/workflows/` — `build-vsix.yml` (artifact `gatling-cursor-pack-vsix` on each run); `release-vsix.yml` (GitHub **Release** + attached `.vsix` on tag `v*`)

## Requirements

A valid `GATLING_ENTERPRISE_API_TOKEN` with at least the **Configure** role.

## Documentation

[Gatling — AI extensions](https://docs.gatling.io/integrations/ai/extensions/overview/)

## Help

[Gatling documentation](https://docs.gatling.io) · [Community forum](https://community.gatling.io) · [Gatling product issues](https://github.com/gatling/gatling/issues)
