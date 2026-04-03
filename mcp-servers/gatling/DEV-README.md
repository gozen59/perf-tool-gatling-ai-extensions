# MCP server - TypeScript/Node.js with official MCP SDK - STDIO communication

## Setup

```shell
npm install
```

Other commands:

- Clean (delete compiled code): `npm run clean`
- Format code: `npm run format`
- Compile: `npm run build`
- Run the application: `npm run start`

Inspect the server with MCP Inspector: run the server with `npm run start` and launch the inspector with `npx @modelcontextprotocol/inspector`.

## Configure MCP server

The configurations below require exporting `GATLING_ENTERPRISE_API_TOKEN` before starting the LLM client.

In non-production environments, also export `GATLING_ENTERPRISE_API_URL`.

### With `npm` (from local project)

`mcpServers` configuration:

```json
{
  "type": "stdio",
  "command": "npm",
  "args": [
    "run",
    "--prefix",
    "<path-to-gatling-ai-extensions>/mcp-servers/gatling",
    "start"
  ],
  "env": {
    "GATLING_ENTERPRISE_API_TOKEN": "${GATLING_ENTERPRISE_API_TOKEN}"
  }
}
```

### With Cursor

In **Cursor Settings → MCP**, add a `gatling` entry pointing at this server (stdio), or merge into `~/.cursor/mcp.json` a block like:

```json
{
  "mcpServers": {
    "gatling": {
      "command": "npm",
      "args": ["run", "--prefix", "<path-to-repo>/mcp-servers/gatling", "start"],
      "env": {
        "GATLING_ENTERPRISE_API_TOKEN": "${GATLING_ENTERPRISE_API_TOKEN}"
      }
    }
  }
}
```

For use without a local clone, prefer the published package: see the repository root `mcp.json.example` (`npx @gatling.io/gatling-mcp-server`).

### With Docker

Build the Docker image:

```shell
npm run build
docker build --tag gatlingcorp/gatling-mcp-server:<tag> .  
```

`mcpServers` configuration:

```json
{
  "type": "stdio",
  "command": "docker",
  "args": [
    "run",
    "--rm",
    "-i",
    "-e",
    "GATLING_ENTERPRISE_API_TOKEN=${GATLING_ENTERPRISE_API_TOKEN}",
    "<local-image-tag>"
  ],
  "env": {
    "GATLING_ENTERPRISE_API_TOKEN": "${GATLING_ENTERPRISE_API_TOKEN}"
  }
}
```

### Docker + Cursor

Same idea: declare a stdio `docker run ...` command in Cursor’s MCP config with `-e GATLING_ENTERPRISE_API_TOKEN=...`, following the JSON pattern above.
