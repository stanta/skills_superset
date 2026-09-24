#!/usr/bin/env python3
"""CI/maintainer validation; agents only SEARCH and READ static Markdown files."""
from collections import defaultdict
import json
import os
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
META = ROOT / "skills"
ATOMIC = ROOT / "atomic-skills"
ATOMIC_PREFIX = re.compile(r"(?:\.\./)*atomic-skills/")


def resolve_atomic_reference(source: Path, raw: str,
                             atomic_root: Path = ATOMIC) -> Path:
    """Resolve a child path relative to its CONTAINING FILE, never the repo root.

    Assert the shortest canonical relative prefix to the atomic directory and
    forbid path traversal inside that directory. The target must be a real file.
    """
    origin = source.parent.resolve(strict=True)
    root = atomic_root.resolve(strict=True)
    expected = os.path.relpath(root, origin).replace(os.sep, "/") + "/"
    if raw.startswith("/") or "\\" in raw or not raw.startswith(expected):
        raise AssertionError(
            f"Wrong relative prefix in {source}: {raw!r}; expected {expected!r}"
        )
    suffix = raw[len(expected):]
    if (not suffix or any(part in {".", "..", ""} for part in suffix.split("/"))
            or not suffix.endswith("/SKILL.md")):
        raise AssertionError(f"Invalid atomic skill path in {source}: {raw!r}")
    try:
        target = (origin / raw).resolve(strict=True)
        target.relative_to(root)
    except (ValueError, OSError) as exc:
        raise AssertionError(f"Atomic reference escapes root or is missing: {raw}") from exc
    if not target.is_file() or target.is_symlink() or target.name != "SKILL.md":
        raise AssertionError(f"Atomic reference is not a regular SKILL.md: {raw}")
    return target


def _markdown_target(line: str) -> str:
    value = line.rsplit(" — ", 1)[-1]
    tick = chr(96)
    if not value.startswith(tick) or not value.endswith(tick) or value.count(tick) != 2:
        raise AssertionError(f"Malformed Markdown path: {line[:200]}")
    return value[1:-1]


def validate() -> dict:
    readme = ROOT / "README.md"
    doc = ROOT / "docs" / "metaskills.md"
    if "Use the existing file-search tool on the exact path" not in readme.read_text(encoding="utf-8"):
        raise AssertionError("Missing scoped file-search guidance in README")
    # These examples are interpreted from their own containing file locations.
    resolve_atomic_reference(readme, "atomic-skills/react-expert/SKILL.md")
    resolve_atomic_reference(doc, "../atomic-skills/agent-evals-lab/SKILL.md")

    public = sorted(META.rglob("SKILL.md"))
    atoms = sorted(ATOMIC.rglob("SKILL.md"))
    if len(public) != 26 or not atoms:
        raise AssertionError("Missing first-level or atomic skills")
    if any(p.parent.parent != META or not p.parent.name.startswith("meta-")
           for p in public):
        raise AssertionError("Atomic SKILL.md leaked into public skills/ directory")
    if any(p.is_symlink() for p in public + atoms):
        raise AssertionError("Symlinked SKILL.md is not allowed")
    atomic_paths = {p.resolve(strict=True) for p in atoms}
    membership = defaultdict(set)
    catalog_links = 0

    for meta_file in public:
        name = meta_file.parent.name
        body = meta_file.read_text(encoding="utf-8")
        if not body.startswith("---\nname: " + name + "\ndescription:"):
            raise AssertionError("Invalid standard skill frontmatter: " + name)
        if "Use the existing file-search tool on the exact path" not in body:
            raise AssertionError("Missing scoped file-search guidance in meta skill: " + name)
        if "python discovery/" in body or "discovery/metaskill_cli.py" in body:
            raise AssertionError("Meta skill requires an agent-time script: " + name)
        expected_meta_prefix = os.path.relpath(ATOMIC, meta_file.parent).replace(os.sep, "/") + "/"
        if expected_meta_prefix != "../../atomic-skills/":
            raise AssertionError("Unexpected meta skill directory depth: " + name)
        if expected_meta_prefix not in body:
            raise AssertionError("Meta skill omits its own relative atomic root: " + name)
        # Documenting the catalog's prefix is allowed; all other variants fail.
        for prefix in ATOMIC_PREFIX.findall(body):
            if prefix not in {"../../atomic-skills/", "../../../atomic-skills/"}:
                raise AssertionError(f"Wrong atomic root in {meta_file}: {prefix}")
        for segment in body.split(chr(96))[1::2]:
            if segment.startswith("../../atomic-skills/") and segment.endswith("/SKILL.md"):
                if "<" not in segment and ">" not in segment:
                    resolve_atomic_reference(meta_file, segment)
        registry_ref = ("references/legacy-names.md" if name == "meta-specialist-catalog"
                        else "../meta-specialist-catalog/references/legacy-names.md")
        if registry_ref not in body or not (meta_file.parent / registry_ref).is_file():
            raise AssertionError("Broken relative legacy lookup from meta: " + name)

        catalog = meta_file.parent / "references" / "members.md"
        if not catalog.is_file():
            raise AssertionError("Missing static child catalog: " + name)
        local_seen = set()
        for line in catalog.read_text(encoding="utf-8").splitlines():
            if not line.startswith("- **"):
                continue
            name_end = line.find("**", 4)
            if name_end < 0 or " — " not in line:
                raise AssertionError("Malformed catalog entry: " + line[:200])
            identifier = line[4:name_end]
            raw = _markdown_target(line)
            target = resolve_atomic_reference(catalog, raw)
            if target not in atomic_paths:
                raise AssertionError(f"Catalog links to unknown atomic skill: {raw}")
            expected_id = target.parent.relative_to(ATOMIC.resolve()).as_posix()
            if identifier != expected_id or target in local_seen:
                raise AssertionError("Duplicate or incorrect child ID: " + identifier)
            local_seen.add(target)
            membership[target].add(name)
            catalog_links += 1
        refs = ATOMIC_PREFIX.findall(catalog.read_text(encoding="utf-8"))
        if any(prefix != "../../../atomic-skills/" for prefix in refs):
            raise AssertionError("Wrong atomic root prefix in child catalog: " + str(catalog))

    missing = atomic_paths - membership.keys()
    if missing:
        raise AssertionError("Atomic skills without any meta: " +
                             repr(sorted(str(path) for path in missing)[:20]))
    if any(len(groups) > 2 for groups in membership.values()):
        raise AssertionError("More than two assigned meta-skills for an atomic skill")
    registry = META / "meta-specialist-catalog" / "references" / "legacy-names.md"
    if not registry.is_file():
        raise AssertionError("Missing static direct-lookup registry")
    registered = set()
    registry_links = 0
    for line in registry.read_text(encoding="utf-8").splitlines():
        if not line.startswith("- **"):
            continue
        id_end = line.find("**", 4)
        if id_end < 0:
            raise AssertionError("Malformed legacy registry ID")
        identity = line[4:id_end]
        raw = _markdown_target(line)
        target = resolve_atomic_reference(registry, raw)
        expected_id = target.parent.relative_to(ATOMIC.resolve()).as_posix()
        if identity != expected_id or target in registered:
            raise AssertionError("Duplicate or incorrect legacy ID: " + identity)
        owners = line[id_end + 2:].strip().split(" — ")
        if len(owners) != 3 or set(owners[1].split(", ")) != membership[target]:
            raise AssertionError("Wrong owning meta-skills in legacy registry: " + identity)
        registered.add(target)
        registry_links += 1
    if registered != atomic_paths:
        raise AssertionError("Exact legacy lookup is incomplete or duplicated")
    if any(prefix != "../../../atomic-skills/"
           for prefix in ATOMIC_PREFIX.findall(registry.read_text(encoding="utf-8"))):
        raise AssertionError("Wrong relative atomic root in legacy registry")

    examples = {
        "meta-frontend-web": "react-expert",
        "meta-agent-systems": "rlm-roec-context-reasoning",
        "meta-devops-cloud": "sentry-glitchtip-observability",
        "meta-web3-blockchain": "ton-smart-contracts-specialist",
    }
    for group, child in examples.items():
        catalog = META / group / "references" / "members.md"
        expected = catalog.parent / ("../../../atomic-skills/" + child + "/SKILL.md")
        resolve_atomic_reference(catalog, "../../../atomic-skills/" + child + "/SKILL.md")
        if expected.resolve() not in membership:
            raise AssertionError(f"Missing smoke child: {group} / {child}")

    return {
        "meta_skills": len(public),
        "atomic_skills": len(atoms),
        "member_catalogs": len(public),
        "resolved_catalog_paths": catalog_links,
        "resolved_legacy_paths": registry_links,
        "overlapping_atomic_skills": sum(len(groups) == 2 for groups in membership.values()),
        "unassigned": 0,
        "first_level_atomic_leakage": 0,
        "agent_discovery_scripts": 0,
        "status": "PASS",
    }


if __name__ == "__main__":
    try:
        print(json.dumps(validate(), ensure_ascii=False, indent=2))
    except (AssertionError, OSError) as exc:
        print("Meta discovery validation failed: " + str(exc), file=sys.stderr)
        sys.exit(1)
