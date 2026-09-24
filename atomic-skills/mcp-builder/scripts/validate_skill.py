#!/usr/bin/env python3
"""Validate the mcp-builder skill structure and internal references."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
REQUIRED_REFERENCES = {
    "reference/mcp_best_practices.md",
    "reference/python_mcp_server.md",
    "reference/node_mcp_server.md",
    "reference/evaluation.md",
    "reference/research_sources.md",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def parse_frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        fail("SKILL.md must start with YAML frontmatter")
    try:
        _, frontmatter, _ = text.split("---", 2)
    except ValueError:
        fail("SKILL.md frontmatter is not closed")
    return frontmatter


def main() -> None:
    if not SKILL.is_file():
        fail("SKILL.md is missing")

    text = SKILL.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(text)

    for key in ("name", "description"):
        if not re.search(rf"(?m)^{key}:\s*\S", frontmatter):
            fail(f"frontmatter field {key!r} is missing or empty")

    if not re.search(r"(?m)^name:\s*mcp-builder\s*$", frontmatter):
        fail("frontmatter name must be mcp-builder")

    missing = [path for path in sorted(REQUIRED_REFERENCES) if not (ROOT / path).is_file()]
    if missing:
        fail(f"required references missing: {', '.join(missing)}")

    referenced = set(re.findall(r"`((?:reference|scripts)/[^`]+)`", text))
    broken = [path for path in sorted(referenced) if not (ROOT / path).exists()]
    if broken:
        fail(f"broken relative references in SKILL.md: {', '.join(broken)}")

    for path in [SKILL, *(ROOT / item for item in REQUIRED_REFERENCES)]:
        value = path.read_text(encoding="utf-8")
        if "\x00" in value:
            fail(f"NUL byte found in {path.relative_to(ROOT)}")
        if len(value.strip()) == 0:
            fail(f"empty file: {path.relative_to(ROOT)}")

    print(
        "OK: mcp-builder skill has valid frontmatter, required references, "
        "and no broken backtick-linked local paths"
    )


if __name__ == "__main__":
    main()
