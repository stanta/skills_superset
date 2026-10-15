#!/usr/bin/env python3
"""One-time maintainer edit; remove after verification. Not agent discovery."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
ID = "apple-app-store-publishing"
OWNERS = ("meta-mobile-desktop", "meta-devops-cloud")
UPDATES = {}


def read(relative):
    path = ROOT / relative
    if not path.is_file() or path.is_symlink():
        raise RuntimeError("Expected regular existing file: " + relative)
    path.resolve().relative_to(ROOT.resolve())
    return path.read_text(encoding="utf-8")


def append_section(relative, title, body):
    text = UPDATES.get(relative, read(relative))
    section = title + "\n\n" + body.strip() + "\n"
    if title in text:
        if section not in text:
            raise RuntimeError("Unexpected existing section: " + relative)
        return
    UPDATES[relative] = text.rstrip() + "\n\n" + section


def add_catalog_entry(relative, entry, counted):
    text = read(relative)
    lines = text.splitlines()
    prefix = "- **" + ID + "**"
    existing = [line for line in lines if line.startswith(prefix)]
    if existing and existing != [entry]:
        raise RuntimeError("Conflicting skill entry: " + relative)
    if not existing:
        at = len(lines)
        for index, line in enumerate(lines):
            if line.startswith("- **"):
                identity = line.split("**", 2)[1]
                if identity > ID:
                    at = index
                    break
        lines.insert(at, entry)
    updated = "\n".join(lines) + "\n"
    if counted:
        count = sum(line.startswith("- **") for line in lines)
        updated, n = re.subn(r"(?m)^\d+ atomic skills\.", str(count) + " atomic skills.", updated)
        if n != 1:
            raise RuntimeError("Missing unique count header: " + relative)
    UPDATES[relative] = updated


def add_meta_scope(meta, scope, route):
    relative = "skills/" + meta + "/SKILL.md"
    text = read(relative)
    end = text.find("\n---\n", 4)
    if not text.startswith("---\nname: " + meta + "\ndescription: >\n") or end < 0:
        raise RuntimeError("Unexpected meta frontmatter: " + meta)
    descriptor = text[:end].split("description: >\n", 1)[1]
    if any(line and not line.startswith("  ") for line in descriptor.splitlines()):
        raise RuntimeError("Unexpected fields after description: " + meta)
    line = "  App Store scope: " + scope
    if line not in text[:end]:
        text = text[:end] + "\n" + line + text[end:]
    UPDATES[relative] = text
    append_section(relative, "## Apple App Store publishing", route)


def main():
    target = ROOT / "atomic-skills" / ID / "SKILL.md"
    if not target.is_file() or target.is_symlink():
        raise RuntimeError("Missing new atomic skill")
    description = "Universal Apple App Store readiness, signing, privacy, payments, TestFlight, review, release and optimization across native and cross-platform projects."
    for owner in OWNERS:
        add_catalog_entry(
            "skills/" + owner + "/references/members.md",
            "- **" + ID + "** — " + description + " — `../../../atomic-skills/" + ID + "/SKILL.md`",
            True,
        )
    add_catalog_entry(
        "skills/meta-specialist-catalog/references/legacy-names.md",
        "- **" + ID + "** — " + ", ".join(OWNERS) + " — `../../../atomic-skills/" + ID + "/SKILL.md`",
        False,
    )
    atomic = "`../../atomic-skills/" + ID + "/SKILL.md`"
    add_meta_scope("meta-mobile-desktop", "App Store publication, AppleStore, TestFlight, review readiness and Apple-platform releases; публикация в App Store.",
        "Start with " + atomic + " for App Store publication or rejection remediation. Add only the actual framework specialist for implementation. Use the skill's evidence and authority gates before upload, submission or public release.")
    add_meta_scope("meta-devops-cloud", "App Store release pipelines, signing, App Store Connect, TestFlight, staged updates and release evidence.",
        "For Apple release automation, start with " + atomic + ". Add CI/security or observability children only where needed. Separate build, upload, review and release states; preserve signing secrets and public-release authorization.")
    add_meta_scope("meta-security-compliance", "App Store privacy declarations, SDK manifests, tracking, account deletion and conditional store compliance.",
        "For App Store submission-specific policy gates, follow " + atomic + " through meta-mobile-desktop or meta-devops-cloud. Add this domain's specialists for privacy or regulatory findings. This is a cross-domain route, not a third catalog ownership assignment.")
    add_meta_scope("meta-marketing-growth", "App Store optimization (ASO), localized product pages, store conversion and truthful release metadata.",
        "For ASO and App Store product-page work, follow " + atomic + " through meta-mobile-desktop or meta-devops-cloud, then read its optimization reference. Add marketing specialists for campaign strategy; keep ranking claims and measured conversion separate. This is a cross-domain route, not a third catalog ownership assignment.")
    append_section("README.md", "## Apple App Store publishing",
        "For App Store publication (including AppleStore queries), TestFlight, review readiness, signing/privacy/payment gates, release operations and ASO, use [apple-app-store-publishing](atomic-skills/apple-app-store-publishing/SKILL.md). It is project- and framework-neutral, with reusable agent/reviewer templates, a dated primary-source ledger and evaluation cases. Discover it through [meta-mobile-desktop](skills/meta-mobile-desktop/SKILL.md) or [meta-devops-cloud](skills/meta-devops-cloud/SKILL.md); security and marketing meta-skills provide cross-domain routes.")
    append_section("docs/metaskills.md", "## Apple App Store publishing route",
        "The project-neutral [apple-app-store-publishing](../atomic-skills/apple-app-store-publishing/SKILL.md) atomic skill belongs to meta-mobile-desktop and meta-devops-cloud. Their child catalogs and the exact-name registry include it. Meta-security-compliance and meta-marketing-growth provide cross-domain routing without additional membership. Read the skill's references selectively; no runtime script or proprietary agent host is required.")
    append_section("atomic-skills/README.md", "## Apple App Store publishing",
        "[apple-app-store-publishing](apple-app-store-publishing/SKILL.md) covers project-neutral App Store readiness, submission, release and optimization. Initial discovery remains through meta-mobile-desktop or meta-devops-cloud, not a repository-wide atomic scan.")
    for relative, content in sorted(UPDATES.items()):
        path = ROOT / relative
        if path.read_text(encoding="utf-8") != content:
            path.write_text(content, encoding="utf-8")
            print(relative)


if __name__ == "__main__":
    main()
