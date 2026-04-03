#!/usr/bin/env python3
"""
Regenerate .cursor/skills/*/SKILL.md from reference/gatling-skills/*/SKILL.md
with Cursor-oriented edits (extra upstream frontmatter keys, paths, /Gatling: refs, etc.).
Run from repo root: python3 scripts/adapt_upstream_skill_md.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def strip_upstream_only_frontmatter_keys(text: str) -> str:
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    in_fm = False
    for line in lines:
        stripped = line.strip()
        if stripped == "---":
            out.append(line)
            in_fm = not in_fm
            continue
        if in_fm and stripped.startswith(("user-invocable:", "mcp-server:")):
            continue
        out.append(line)
    return "".join(out)


def adapt_bootstrap(s: str) -> str:
    s = strip_upstream_only_frontmatter_keys(s)
    s = s.replace("./resources/", "./references/")
    s = s.replace(
        "When ready to deploy to Gatling Enterprise, use the /Gatling:gatling-build-tools skill for guidance.",
        "When ready to deploy to Gatling Enterprise, follow the skill **gatling-build-tools** (in `.cursor/skills/gatling-build-tools`) for guidance.",
    )
    return s


def adapt_build_tools(s: str) -> str:
    s = strip_upstream_only_frontmatter_keys(s)
    insert = (
        "When the **gatling** MCP server is configured in Cursor, use its tools for "
        "Gatling Enterprise API operations when they help the workflow (listing resources, "
        "validating account data, etc.).\n\n"
    )
    s = s.replace(
        "# Gatling Enterprise - Build Tools\n\n## Instructions",
        "# Gatling Enterprise - Build Tools\n\n" + insert + "## Instructions",
    )
    s = s.replace(
        "help the user create it using the Configuration as Code skill.",
        "help the user create it using the skill **gatling-configuration-as-code** "
        "(`.cursor/skills/gatling-configuration-as-code`).",
    )
    return s


def adapt_configuration_as_code(s: str) -> str:
    s = strip_upstream_only_frontmatter_keys(s)
    insert = (
        "\nWhen the **gatling** MCP server is configured in Cursor, use its tools to fetch "
        "teams, locations, packages, and simulations from the user's Gatling Enterprise account "
        "before authoring or updating `package.conf`.\n"
    )
    s = s.replace(
        "deploying tests to Gatling Enterprise.\n\n## Instructions",
        "deploying tests to Gatling Enterprise." + insert + "\n## Instructions",
    )
    s = s.replace(
        "4. Ask the user what they need with the `AskUserQuestion` tool.\n"
        "   If a list has >4 items, output the full list as markdown in a text message and ask the user to specify their choice(s) by name.",
        "4. Ask the user what they need in the chat (clear questions with listed options when helpful).\n"
        "   If a list has >4 items, output the full list as markdown in a message and ask the user to specify their choice(s) by name.",
    )
    return s


def adapt_convert_jmeter(s: str) -> str:
    s = strip_upstream_only_frontmatter_keys(s)
    s = s.replace(
        "- Try to find an existing project with the /Gatling:gatling-detect-existing-project skill.",
        "- Try to find an existing project using the skill **gatling-detect-existing-project** "
        "(`.cursor/skills/gatling-detect-existing-project`).",
    )
    s = s.replace(
        "- If no existing project is found, offer to create a new one with the /Gatling:gatling-bootstrap-project skill.",
        "- If no existing project is found, offer to create a new one with the skill **gatling-bootstrap-project** "
        "(`.cursor/skills/gatling-bootstrap-project`).",
    )
    # Replace broken jmesPath code fence (upstream uses typographic apostrophe in "doesn't")
    jmespath_section = re.compile(
        r"Note that the check will then fail (?:is|if) the actual value doesn.t match the expected type\.\r?\n\r?\n```\r?\n[\s\S]*?\r?\n```",
        re.MULTILINE,
    )
    new_block = (
        "Note that the check will then fail if the actual value doesn't match the expected type.\n\n"
        "The `jmesPath` check supports type refinements: `ofString()`, `ofBoolean()`, `ofInt()`, "
        "`ofLong()`, `ofDouble()`, `ofList()`, `ofMap()`, `ofObject()` — pick the one that matches "
        "the expected JSON type."
    )
    s, n = jmespath_section.subn(new_block, s, count=1)
    if n == 0:
        print("warn: jmesPath block pattern did not match; edit adapt_convert_jmeter()", file=sys.stderr)
    return s


def adapt_detect(s: str) -> str:
    return strip_upstream_only_frontmatter_keys(s)


ADAPTERS = {
    "gatling-bootstrap-project": adapt_bootstrap,
    "gatling-build-tools": adapt_build_tools,
    "gatling-configuration-as-code": adapt_configuration_as_code,
    "gatling-convert-from-jmeter": adapt_convert_jmeter,
    "gatling-detect-existing-project": adapt_detect,
}


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    src_root = root / "reference" / "gatling-skills"
    dst_root = root / ".cursor" / "skills"
    if not src_root.is_dir():
        print(f"error: missing {src_root}", file=sys.stderr)
        return 1
    dst_root.mkdir(parents=True, exist_ok=True)
    for name, fn in sorted(ADAPTERS.items()):
        src_file = src_root / name / "SKILL.md"
        if not src_file.is_file():
            print(f"warn: skip missing {src_file}", file=sys.stderr)
            continue
        raw = src_file.read_text(encoding="utf-8")
        out = fn(raw)
        out_path = dst_root / name / "SKILL.md"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(out, encoding="utf-8", newline="\n")
        print(f"wrote {out_path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
