#!/usr/bin/env python3
"""CI/maintainer-only check. Agents do NOT run scripts for skill discovery."""
from collections import defaultdict
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
META = ROOT / "skills"
ATOMIC = ROOT / "atomic-skills"


def validate() -> dict:
    if "Use the existing file-search tool on the exact path" not in (ROOT / "README.md").read_text(encoding="utf-8"):
        raise AssertionError("Missing scoped file-search guidance in README")
    public = sorted(META.rglob("SKILL.md"))
    atoms = sorted(ATOMIC.rglob("SKILL.md"))
    if len(public) != 26 or not atoms:
        raise AssertionError("Missing first-level or atomic skills")
    if any(p.parent.parent != META or not p.parent.name.startswith("meta-")
           for p in public):
        raise AssertionError("Atomic SKILL.md leaked into public skills/ directory")
    if any(p.is_symlink() for p in public + atoms):
        raise AssertionError("Symlinked SKILL.md is not allowed")
    atomic_paths = {p.relative_to(ROOT).as_posix() for p in atoms}
    membership = defaultdict(set)
    total_entries = 0
    for meta_file in public:
        name = meta_file.parent.name
        content = meta_file.read_text(encoding="utf-8")
        if not content.startswith("---\nname: " + name + "\ndescription:"):
            raise AssertionError("Invalid standard skill frontmatter: " + name)
        if "Use the existing file-search tool on the exact path" not in content:
            raise AssertionError("Missing scoped file-search guidance in meta skill: " + name)
        if "python discovery/" in content or "discovery/metaskill_cli.py" in content:
            raise AssertionError("Meta skill requires an agent-time script: " + name)
        catalog = meta_file.parent / "references" / "members.md"
        if not catalog.is_file():
            raise AssertionError("Missing static child catalog: " + name)
        local_seen = set()
        for line in catalog.read_text(encoding="utf-8").splitlines():
            if not line.startswith("- **"):
                continue
            name_end = line.find("**", 4)
            if name_end < 0 or " — " not in line:
                raise AssertionError("Malformed member entry: " + line[:100])
            identifier = line[4:name_end]
            last = line.rsplit(" — ", 1)[-1]
            path = last.removeprefix(chr(96)).removesuffix(chr(96))
            if path not in atomic_paths:
                raise AssertionError("Broken child reference: " + path)
            inferred = path[len("atomic-skills/"):-len("/SKILL.md")]
            if identifier != inferred or path in local_seen:
                raise AssertionError("Duplicate or incorrect child ID: " + identifier)
            local_seen.add(path)
            membership[path].add(name)
            total_entries += 1
    missing = atomic_paths - membership.keys()
    if missing:
        raise AssertionError("Atomic skills without any meta: " + repr(sorted(missing)[:20]))
    if any(len(metas) > 2 for metas in membership.values()):
        raise AssertionError("More than two assigned meta-skills for an atomic skill")
    registry = META / "meta-specialist-catalog" / "references" / "legacy-names.md"
    if not registry.is_file():
        raise AssertionError("Missing static direct-lookup registry")
    direct_paths = []
    for line in registry.read_text(encoding="utf-8").splitlines():
        if line.startswith("- **"):
            if " — " not in line:
                raise AssertionError("Malformed legacy registry row")
            path = line.rsplit(" — ", 1)[-1].removeprefix(chr(96)).removesuffix(chr(96))
            direct_paths.append(path)
    if len(direct_paths) != len(set(direct_paths)) or set(direct_paths) != atomic_paths:
        raise AssertionError("Legacy direct-lookup registry incomplete or duplicated")
    smoke = {
        "meta-frontend-web": "react-expert",
        "meta-agent-systems": "rlm-roec-context-reasoning",
        "meta-devops-cloud": "sentry-glitchtip-observability",
        "meta-web3-blockchain": "ton-smart-contracts-specialist",
    }
    for group, child in smoke.items():
        path = META / group / "references" / "members.md"
        if not any(line.startswith("- **" + child + "** — ")
                   for line in path.read_text(encoding="utf-8").splitlines()):
            raise AssertionError("Missing smoke child: " + group + " / " + child)
    return {
        "meta_skills": len(public),
        "atomic_skills": len(atoms),
        "member_catalogs": len(public),
        "membership_entries": total_entries,
        "overlapping_atomic_skills": sum(len(m) == 2 for m in membership.values()),
        "exact_legacy_names": len(direct_paths),
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
