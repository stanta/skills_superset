#!/usr/bin/env python3
"""Deterministic admission scanner for agent skill packages.

This scanner is intentionally dependency-free. It performs conservative static checks and
is designed to complement, not replace, sandboxed execution, SAST/SCA, malware scanning,
and adversarial LLM evaluation.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import tarfile
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable

SEVERITY_RANK = {"info": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}
TEXT_EXTENSIONS = {
    ".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf",
    ".py", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".sh", ".bash", ".zsh",
    ".ps1", ".rb", ".go", ".rs", ".java", ".kt", ".php", ".sql", ".xml", ".html",
    ".css", ".scss", ".env", ".properties", ".lock",
}
EXECUTABLE_EXTENSIONS = {".exe", ".dll", ".so", ".dylib", ".com", ".scr", ".msi", ".apk", ".appimage"}
ARCHIVE_EXTENSIONS = {".zip", ".tar", ".tgz", ".gz", ".bz2", ".xz"}
INVISIBLE_OR_BIDI = {
    "\u200b": "ZERO WIDTH SPACE",
    "\u200c": "ZERO WIDTH NON-JOINER",
    "\u200d": "ZERO WIDTH JOINER",
    "\u2060": "WORD JOINER",
    "\ufeff": "ZERO WIDTH NO-BREAK SPACE/BOM",
    "\u202a": "LEFT-TO-RIGHT EMBEDDING",
    "\u202b": "RIGHT-TO-LEFT EMBEDDING",
    "\u202d": "LEFT-TO-RIGHT OVERRIDE",
    "\u202e": "RIGHT-TO-LEFT OVERRIDE",
    "\u2066": "LEFT-TO-RIGHT ISOLATE",
    "\u2067": "RIGHT-TO-LEFT ISOLATE",
    "\u2068": "FIRST STRONG ISOLATE",
    "\u2069": "POP DIRECTIONAL ISOLATE",
}

@dataclass
class Finding:
    rule_id: str
    severity: str
    path: str
    line: int | None
    message: str
    evidence: str | None = None

def add(findings: list[Finding], rule_id: str, severity: str, path: Path | str,
        message: str, line: int | None = None, evidence: str | None = None) -> None:
    findings.append(Finding(rule_id, severity, str(path), line, message, evidence))

def load_rules(script_path: Path) -> list[dict]:
    rules_path = script_path.parent.parent / "rules" / "instruction-patterns.json"
    try:
        data = json.loads(rules_path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"Unable to load rule set {rules_path}: {exc}")
    for rule in data:
        try:
            re.compile(rule["pattern"])
            if rule["severity"] not in SEVERITY_RANK:
                raise ValueError(f"invalid severity {rule['severity']}")
        except Exception as exc:
            raise SystemExit(f"Invalid rule {rule.get('id')}: {exc}")
    return data

def is_text_candidate(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTENSIONS or path.name in {
        "Dockerfile", "Makefile", "requirements.txt", "requirements-dev.txt", "AGENTS.md", "CLAUDE.md"
    }

def safe_read_text(path: Path, max_bytes: int = 2_000_000) -> str | None:
    try:
        if path.stat().st_size > max_bytes:
            return None
        raw = path.read_bytes()
    except OSError:
        return None
    if b"\x00" in raw:
        return None
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return None

def line_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1

def scan_frontmatter(skill_dir: Path, findings: list[Finding]) -> None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        add(findings, "SKILL_MD_MISSING", "critical", skill_md, "Skill package has no SKILL.md.")
        return
    text = safe_read_text(skill_md)
    if text is None:
        add(findings, "SKILL_MD_UNREADABLE", "high", skill_md, "SKILL.md is not valid small UTF-8 text.")
        return
    if not text.startswith("---\n"):
        add(findings, "FRONTMATTER_MISSING", "high", skill_md, "SKILL.md must start with YAML frontmatter.")
        return
    end = text.find("\n---", 4)
    if end < 0:
        add(findings, "FRONTMATTER_BROKEN", "high", skill_md, "SKILL.md frontmatter is not terminated.")
        return
    frontmatter = text[4:end]
    if not re.search(r"(?m)^name:\s*\S+", frontmatter):
        add(findings, "SKILL_NAME_MISSING", "high", skill_md, "Frontmatter is missing a non-empty name.")
    if not re.search(r"(?m)^description:\s*\S+", frontmatter):
        add(findings, "SKILL_DESCRIPTION_MISSING", "high", skill_md, "Frontmatter is missing a non-empty description.")

def scan_unicode(path: Path, text: str, findings: list[Finding]) -> None:
    for char, name in INVISIBLE_OR_BIDI.items():
        start = 0
        while True:
            pos = text.find(char, start)
            if pos < 0:
                break
            severity = "high" if "OVERRIDE" in name or "EMBEDDING" in name or "ISOLATE" in name else "medium"
            add(findings, "SUSPICIOUS_UNICODE", severity, path,
                f"Suspicious invisible/bidirectional Unicode character: {name}.",
                line=line_for_offset(text, pos), evidence=f"U+{ord(char):04X}")
            start = pos + 1

def scan_rules(path: Path, text: str, rules: list[dict], findings: list[Finding]) -> None:
    if path.as_posix().endswith("skill-security-auditor/rules/instruction-patterns.json"):
        return
    for rule in rules:
        scope = rule.get("scope", "text")
        if scope == "python" and path.suffix.lower() != ".py":
            continue
        if scope not in {"text", "python"}:
            continue
        regex = re.compile(rule["pattern"])
        for match in regex.finditer(text):
            evidence = match.group(0).replace("\n", " ")[:220]
            severity = rule["severity"]
            if scope == "text" and path.suffix.lower() in {".py", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java", ".kt", ".php"}:
                if severity == "critical":
                    severity = "high"
                elif severity == "high":
                    severity = "medium"
            add(findings, rule["id"], severity, path, rule["message"],
                line=line_for_offset(text, match.start()), evidence=evidence)

def scan_package_json(path: Path, findings: list[Finding]) -> None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        add(findings, "PACKAGE_JSON_INVALID", "medium", path, f"Invalid package.json: {exc}")
        return
    scripts = data.get("scripts") or {}
    for hook in ("preinstall", "install", "postinstall", "prepare"):
        if hook in scripts:
            add(findings, "NPM_INSTALL_HOOK", "high", path,
                f"npm lifecycle hook '{hook}' executes during install/build and requires manual review.",
                evidence=str(scripts[hook])[:220])
    for section in ("dependencies", "devDependencies", "optionalDependencies"):
        deps = data.get(section) or {}
        for name, spec in deps.items():
            spec_s = str(spec).strip()
            if spec_s in {"*", "latest", "next"}:
                add(findings, "UNPINNED_DEPENDENCY", "medium", path,
                    f"Dependency {name} uses mutable/unbounded specifier '{spec_s}'.")
            if re.match(r"(?i)^(git\+|git://|https?://|github:)", spec_s):
                add(findings, "REMOTE_DEPENDENCY", "medium", path,
                    f"Dependency {name} is fetched from a remote VCS/URL specifier; verify immutable revision and provenance.",
                    evidence=spec_s[:220])

def scan_requirements(path: Path, text: str, findings: list[Finding]) -> None:
    for i, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("-"):
            continue
        if re.match(r"(?i)(git\+|https?://)", line):
            add(findings, "REMOTE_DEPENDENCY", "medium", path,
                "Python dependency is fetched directly from VCS/URL; verify immutable revision and provenance.", i, line[:220])
        elif "==" not in line and not re.search(r"\s*@\s*", line):
            add(findings, "UNPINNED_DEPENDENCY", "medium", path,
                "Python dependency is not exactly pinned with '=='.", i, line[:220])

def binary_kind(raw: bytes) -> str | None:
    if raw.startswith(b"MZ"):
        return "PE/Windows executable"
    if raw.startswith(b"\x7fELF"):
        return "ELF executable/shared object"
    if raw[:4] in {b"\xfe\xed\xfa\xce", b"\xce\xfa\xed\xfe", b"\xfe\xed\xfa\xcf", b"\xcf\xfa\xed\xfe"}:
        return "Mach-O executable/shared object"
    return None

def archive_member_bad(name: str) -> bool:
    p = PurePosixPath(name.replace("\\", "/"))
    return p.is_absolute() or any(part == ".." for part in p.parts)

def scan_zip(path: Path, findings: list[Finding]) -> None:
    try:
        with zipfile.ZipFile(path) as zf:
            total = 0
            compressed = 0
            for info in zf.infolist():
                total += info.file_size
                compressed += max(info.compress_size, 1)
                if archive_member_bad(info.filename):
                    add(findings, "ARCHIVE_PATH_TRAVERSAL", "critical", path,
                        "Archive contains absolute/parent-traversal member.", evidence=info.filename[:220])
                if Path(info.filename).suffix.lower() in EXECUTABLE_EXTENSIONS:
                    add(findings, "ARCHIVE_EXECUTABLE", "high", path,
                        "Archive contains an executable/library payload requiring independent review.", evidence=info.filename[:220])
            if total > 100_000_000 or (compressed and total / compressed > 200):
                add(findings, "ARCHIVE_BOMB_RISK", "high", path,
                    "Archive expansion ratio/size is suspicious and may cause resource exhaustion.",
                    evidence=f"uncompressed={total} compressed={compressed}")
    except zipfile.BadZipFile:
        add(findings, "ARCHIVE_INVALID", "medium", path, "Invalid ZIP archive.")

def scan_tar(path: Path, findings: list[Finding]) -> None:
    try:
        with tarfile.open(path, mode="r:*") as tf:
            total = 0
            for member in tf.getmembers():
                total += max(member.size, 0)
                if archive_member_bad(member.name):
                    add(findings, "ARCHIVE_PATH_TRAVERSAL", "critical", path,
                        "Archive contains absolute/parent-traversal member.", evidence=member.name[:220])
                if member.issym() or member.islnk():
                    if archive_member_bad(member.linkname) or member.linkname.startswith("/"):
                        add(findings, "ARCHIVE_SYMLINK_ESCAPE", "critical", path,
                            "Archive contains a link that may escape extraction root.",
                            evidence=f"{member.name} -> {member.linkname}"[:220])
                if Path(member.name).suffix.lower() in EXECUTABLE_EXTENSIONS:
                    add(findings, "ARCHIVE_EXECUTABLE", "high", path,
                        "Archive contains an executable/library payload requiring independent review.", evidence=member.name[:220])
            if total > 100_000_000:
                add(findings, "ARCHIVE_BOMB_RISK", "high", path,
                    "Archive expands to a large payload and may cause resource exhaustion.", evidence=f"uncompressed={total}")
    except (tarfile.TarError, OSError):
        add(findings, "ARCHIVE_INVALID", "medium", path, "Invalid/unreadable TAR-compatible archive.")

def scan_archive(path: Path, findings: list[Finding]) -> None:
    lower = path.name.lower()
    if lower.endswith(".zip"):
        scan_zip(path, findings)
    elif lower.endswith((".tar", ".tgz", ".tar.gz", ".tar.bz2", ".tar.xz")):
        scan_tar(path, findings)
    elif path.suffix.lower() in {".gz", ".bz2", ".xz"}:
        add(findings, "OPAQUE_COMPRESSED_FILE", "medium", path,
            "Compressed single-file payload is not deeply inspected by this scanner; inspect before execution/use.")

def scan_manifest(skill_dir: Path, findings: list[Finding]) -> None:
    path = skill_dir / "security-manifest.json"
    if not path.exists():
        add(findings, "SECURITY_MANIFEST_MISSING", "info", path,
            "No security-manifest.json. Consider declaring intended capabilities for S1-S3 skills.")
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        add(findings, "SECURITY_MANIFEST_INVALID", "high", path, f"Invalid JSON manifest: {exc}")
        return
    if data.get("version") != 1:
        add(findings, "SECURITY_MANIFEST_VERSION", "medium", path, "Manifest version must be 1.")
    if data.get("risk_tier") not in {"S0", "S1", "S2", "S3"}:
        add(findings, "SECURITY_MANIFEST_TIER", "high", path, "risk_tier must be one of S0/S1/S2/S3.")
    caps = data.get("capabilities")
    if not isinstance(caps, dict):
        add(findings, "SECURITY_MANIFEST_CAPS", "high", path, "capabilities must be an object.")
        return
    network = caps.get("network_hosts", [])
    if network == ["*"] or "*" in network:
        add(findings, "MANIFEST_WILDCARD_NETWORK", "high", path, "Wildcard network access violates least privilege.")
    shell = caps.get("shell_commands", [])
    if shell == ["*"] or "*" in shell:
        add(findings, "MANIFEST_WILDCARD_SHELL", "high", path, "Wildcard shell access violates least privilege.")
    for key in ("filesystem_read", "filesystem_write"):
        vals = caps.get(key, [])
        if isinstance(vals, list) and any(v in {"/", "/**", "~/**", "**"} for v in vals):
            add(findings, "MANIFEST_BROAD_FILESYSTEM", "high", path, f"{key} grants overly broad filesystem scope.")

def scan_symlink(skill_dir: Path, path: Path, findings: list[Finding]) -> None:
    if not path.is_symlink():
        return
    try:
        path.resolve(strict=False).relative_to(skill_dir.resolve(strict=False))
    except (OSError, ValueError):
        add(findings, "SYMLINK_ESCAPE", "critical", path, "Symlink resolves outside the skill package.")

def scan_skill(skill_dir: Path, rules: list[dict]) -> list[Finding]:
    findings: list[Finding] = []
    if not skill_dir.is_dir():
        add(findings, "SKILL_PATH_INVALID", "critical", skill_dir, "Skill path is not a directory.")
        return findings
    scan_frontmatter(skill_dir, findings)
    scan_manifest(skill_dir, findings)
    for path in sorted(skill_dir.rglob("*")):
        if any(part in {".git", "__pycache__", ".venv", "node_modules"} for part in path.parts):
            continue
        scan_symlink(skill_dir, path, findings)
        if path.is_dir() or path.is_symlink():
            continue
        try:
            raw_head = path.read_bytes()[:16]
        except OSError as exc:
            add(findings, "FILE_UNREADABLE", "medium", path, f"Unable to read file: {exc}")
            continue
        kind = binary_kind(raw_head)
        if kind or path.suffix.lower() in EXECUTABLE_EXTENSIONS:
            add(findings, "EXECUTABLE_ARTIFACT", "high", path,
                f"Executable/binary artifact detected ({kind or path.suffix}); require malware scan and provenance verification.")
        lower_name = path.name.lower()
        if any(lower_name.endswith(ext) for ext in ARCHIVE_EXTENSIONS):
            scan_archive(path, findings)
        text = safe_read_text(path) if is_text_candidate(path) else None
        if text is None:
            continue
        scan_unicode(path, text, findings)
        scan_rules(path, text, rules, findings)
        if path.name == "package.json":
            scan_package_json(path, findings)
        if path.name.startswith("requirements") and path.suffix == ".txt":
            scan_requirements(path, text, findings)
    return findings

def git_changed_skill_dirs(repo_root: Path, base: str, head: str) -> list[Path]:
    cmd = ["git", "-C", str(repo_root), "diff", "--name-only", "--diff-filter=ACMR", base, head, "--", "skills"]
    try:
        proc = subprocess.run(cmd, check=True, capture_output=True, text=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f"Unable to determine changed skills with git: {exc}")
    names: set[str] = set()
    for raw in proc.stdout.splitlines():
        parts = Path(raw.strip()).parts
        if len(parts) >= 2 and parts[0] == "skills":
            names.add(parts[1])
    return [repo_root / "skills" / name for name in sorted(names) if (repo_root / "skills" / name).is_dir()]

def relative_findings(findings: Iterable[Finding], root: Path) -> list[Finding]:
    out: list[Finding] = []
    root = root.resolve()
    for f in findings:
        p = Path(f.path)
        try:
            f.path = p.resolve().relative_to(root).as_posix()
        except (OSError, ValueError):
            pass
        out.append(f)
    return out

def main() -> int:
    parser = argparse.ArgumentParser(description="Audit agent skill packages for security admission risks.")
    parser.add_argument("skills", nargs="*", help="Skill directories to scan")
    parser.add_argument("--repo-root", default=".", help="Repository root for changed-skill mode and relative reporting")
    parser.add_argument("--changed-from", help="Base git revision; scans changed skills between base and head")
    parser.add_argument("--changed-to", default="HEAD", help="Head git revision for changed-skill mode")
    parser.add_argument("--fail-on", choices=list(SEVERITY_RANK), default="high", help="Minimum severity that fails the command")
    parser.add_argument("--report", help="Write JSON report to this path")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    rules = load_rules(Path(__file__).resolve())
    skill_dirs = [Path(p).resolve() for p in args.skills]
    if args.changed_from:
        skill_dirs.extend(git_changed_skill_dirs(repo_root, args.changed_from, args.changed_to))
    seen: set[Path] = set()
    skill_dirs = [p for p in skill_dirs if not (p in seen or seen.add(p))]
    if not skill_dirs:
        print("No skill directories selected; nothing to audit.")
        return 0

    all_findings: list[Finding] = []
    for skill_dir in skill_dirs:
        print(f"\n== Auditing {skill_dir} ==")
        current = scan_skill(skill_dir, rules)
        all_findings.extend(current)
        for f in sorted(current, key=lambda x: (-SEVERITY_RANK[x.severity], x.path, x.line or 0, x.rule_id)):
            loc = f"{f.path}:{f.line}" if f.line else f.path
            print(f"[{f.severity.upper():8}] {f.rule_id:28} {loc} — {f.message}")
            if f.evidence:
                print(f"           evidence: {f.evidence}")

    all_findings = relative_findings(all_findings, repo_root)
    counts = {sev: sum(1 for f in all_findings if f.severity == sev) for sev in SEVERITY_RANK}
    report = {
        "scanner": "skill-security-auditor",
        "fail_on": args.fail_on,
        "skills": [str(p) for p in skill_dirs],
        "counts": counts,
        "findings": [asdict(f) for f in all_findings],
    }
    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"\nReport: {report_path}")

    print("\nSummary: " + ", ".join(f"{k}={v}" for k, v in counts.items()))
    threshold = SEVERITY_RANK[args.fail_on]
    blockers = [f for f in all_findings if SEVERITY_RANK[f.severity] >= threshold]
    if blockers:
        print(f"Admission gate: FAIL ({len(blockers)} finding(s) >= {args.fail_on})")
        return 2
    print("Admission gate: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
