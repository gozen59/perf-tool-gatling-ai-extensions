# Gatling Cursor Pack (VS Code / Cursor extension)

Installs Gatling **Agent Skills** (`.cursor/skills/`), the **rule** under `.cursor/rules/`, plus `mcp.json.example` and `AGENTS.md` into an open workspace.

## For end users

1. In **Cursor** or **VS Code**: Extensions → `…` → **Install from VSIX…** → select the `.vsix` file.
2. Open the target project folder (**File → Open Folder**).
3. Command palette (`Cmd+Shift+P` / `Ctrl+Shift+P`) → **Gatling Cursor Pack: Install into workspace**.
4. Follow `AGENTS.md` and `mcp.json.example` to configure the `gatling` MCP server and `GATLING_ENTERPRISE_API_TOKEN`.

## Rebuilding the VSIX (maintainers)

`pack/` is **not** in Git (see [`.gitignore`](../.gitignore)). After a fresh clone, create it from the repo root first:

```bash
# from repository root
./scripts/bundle-vsix-pack.sh
```

Then, from **this** directory:

```bash
npm install   # or npm ci if you rely on package-lock.json only
npm run package
```

This produces `gatling-cursor-pack-<version>.vsix` here (version matches `package.json`, e.g. `0.1.0`). Whenever root `.cursor/`, `AGENTS.md`, or `mcp.json.example` change, run `bundle-vsix-pack.sh` again before packaging.

Bump `"version"` in `package.json` before publishing a new VSIX.

## Git vs GitHub Actions

- **Commit to Git**: extension source only (`extension.js`, `package.json`, `package-lock.json`, `README.md`, `LICENSE`).
- **Ignored locally (not pushed)**: `pack/`, `node_modules/`, `*.vsix` — see [`.gitignore`](../.gitignore). Run `./scripts/bundle-vsix-pack.sh` and `npm run package` locally when you need a VSIX on disk; CI produces the same without polluting the remote repo.
- **GitHub Actions**: [`.github/workflows/build-vsix.yml`](../.github/workflows/build-vsix.yml) bundles `pack/` from the repo root, packages the VSIX, and uploads the **`gatling-cursor-pack-vsix`** artifact — that is the preferred binary for colleagues.

If `pack/` was tracked before: `git rm -r --cached vscode-gatling-cursor-pack/pack` then commit.

## Marketplace publisher

Before publishing to the Marketplace, change `"publisher": "local"` in `package.json` and register a Microsoft publisher account.
