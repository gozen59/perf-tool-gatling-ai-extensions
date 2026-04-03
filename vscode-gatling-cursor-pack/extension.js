"use strict";

const vscode = require("vscode");
const fs = require("fs");
const path = require("path");

/**
 * @param {string} src
 * @param {string} dest
 */
function copyRecursive(src, dest) {
  const stat = fs.statSync(src);
  if (stat.isDirectory()) {
    fs.mkdirSync(dest, { recursive: true });
    for (const name of fs.readdirSync(src)) {
      copyRecursive(path.join(src, name), path.join(dest, name));
    }
  } else {
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.copyFileSync(src, dest);
  }
}

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
  const disposable = vscode.commands.registerCommand(
    "gatlingCursorPack.installToWorkspace",
    async () => {
      const folder = vscode.workspace.workspaceFolders?.[0];
      if (!folder) {
        vscode.window.showErrorMessage(
          "Gatling Cursor Pack: open a folder (File → Open Folder), then run this command again.",
        );
        return;
      }
      const root = folder.uri.fsPath;
      const packDir = path.join(context.extensionPath, "pack");
      if (!fs.existsSync(packDir)) {
        vscode.window.showErrorMessage("Gatling Cursor Pack: missing pack/ folder in the extension.");
        return;
      }

      const dotCursorSrc = path.join(packDir, ".cursor");
      if (fs.existsSync(dotCursorSrc)) {
        const dotCursorDest = path.join(root, ".cursor");
        copyRecursive(dotCursorSrc, dotCursorDest);
      }

      for (const file of ["mcp.json.example", "AGENTS.md"]) {
        const src = path.join(packDir, file);
        if (fs.existsSync(src)) {
          fs.copyFileSync(src, path.join(root, file));
        }
      }

      vscode.window.showInformationMessage(
        "Gatling Cursor Pack: files copied into the workspace. Configure MCP (see AGENTS.md and mcp.json.example) and GATLING_ENTERPRISE_API_TOKEN.",
      );
    },
  );
  context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = { activate, deactivate };
