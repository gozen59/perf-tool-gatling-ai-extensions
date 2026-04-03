# Gatling AI — agent context (Cursor)

This repository provides **Gatling Enterprise** integration for the Cursor agent: skills + MCP server.

**Code here:** [gozen59/perf-tool-gatling-ai-ext](https://github.com/gozen59/perf-tool-gatling-ai-ext) (**fork of** upstream [gatling/gatling-ai-extensions](https://github.com/gatling/gatling-ai-extensions)). See the root [README](README.md) for VSIX distribution and maintenance.

This file is also copied into workspaces when using the **Gatling Cursor Pack** VSIX (**Install into workspace** command).

## MCP server

- **Recommended name**: `gatling`
- **Package**: `@gatling.io/gatling-mcp-server` (via `npx`; see [`mcp.json.example`](mcp.json.example))
- **Authentication**: `GATLING_ENTERPRISE_API_TOKEN` environment variable (minimum **Configure** role)

## Skills (`.cursor/skills/`)

| Skill | Purpose |
|--------|---------|
| `gatling-bootstrap-project` | Create / bootstrap a Gatling project (language + build tool) |
| `gatling-build-tools` | Deploy and run tests on Gatling Enterprise (build-tool plugins) |
| `gatling-configuration-as-code` | Generate or update `.gatling/package.conf` |
| `gatling-convert-from-jmeter` | Convert JMeter plans (`.jmx`) to Gatling |
| `gatling-detect-existing-project` | Detect an existing Gatling project (language, build tool) |

For Gatling Enterprise API operations (teams, locations, packages, simulations), use **MCP tools** on the `gatling` server when it is enabled.

Product documentation: [Gatling AI extensions](https://docs.gatling.io/integrations/ai/extensions/overview/).

## Updating from upstream

1. Refresh [`reference/gatling-skills`](reference/gatling-skills) by copying the published skill bundles from [gatling/gatling-ai-extensions](https://github.com/gatling/gatling-ai-extensions) (the upstream “skills” layout).
2. `./scripts/sync-cursor-skills-from-upstream.sh` — copies ancillary files into `.cursor/skills/`.
3. `./scripts/regenerate-cursor-skill-md.sh` if reference `SKILL.md` files changed — review the diff.

## Other repositories

To use the same skills in a project that is not this repo: copy the `gatling-*` folders from `.cursor/skills/` to `~/.cursor/skills/`.
