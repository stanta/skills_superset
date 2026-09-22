#!/usr/bin/env python3
"""Conservative static admission lint for skill packages.

This script is intentionally dependency-free and does not execute the skill.
It is a first-line gate, not a substitute for sandboxed behavioral testing.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

TEXT_EXT = {
    ".md", ".txt", ".py", ".js", ".ts", ".tsx", ".jsx", ".sh", ".bash",
    ".yml", ".yaml", ".json", ".toml", ".ini", ".cfg", ".xml", ".html",
}

RULES = [
    ("policy_override", "HIGH", re.compile(r"(?i)ignore (all |any )?(previous|prior|system|developer) instructions|override (the )?(system|developer|policy)|bypass (safety|policy|guardrail|harness)")),
    ("secret_access", "CRITICAL", re.compile(r"(?i)(~\/\.ssh|\.aws\/credentials|id_rsa|id_ed25519|print .*environment variables|process\.env|secret.*exfil|credential.*upload)")),
    ("dangerous_pipe_shell", "CRITICAL", re.compile(r"(?i)(curl|wget)[^\n|]{0,240}\|\s*(bash|sh)")),
    ("destructive_shell", "CRITICAL", re.compile(r"(?i)rm\s+-rf\s+(~|/|\$HOME)")),
    ("persistence", "HIGH", re.compile(r"(?i)(\.bashrc|\.zshrc|crontab|git/hooks|systemd|launchd|startup).*?(write|append|install|persist|execute)")),
    ("audit_suppression", "HIGH", re.compile(r"(?i)(disable|delete|suppress|bypass).{0,80}(audit|log|confirmation|approval)")),
    ("metadata_ssrf", "CRITICAL", re.compile(r"169\.254\.169\.254|metadata\.google\.internal")),
    ("encoded_exec", "HIGH", re.compile(r"(?i)(base64\s+(-d|--decode)|eval\s*\(|exec\s*\()")),
    ("mutable_remote_exec", "HIGH", re.compile(r"(?i)(npx\s+[^\s]+@latest|pip\s+install\s+git\+https?://|git\s+clone\s+https?://)")),
]

INSTALL_HOOK_KEYS = {"preinstall", "install", "postinstall", "prepare"}

def iter_files(root: Path):
    for p in root.rglob("*"):
        if p.is_file():
            yield p

def scan_text(path: Path, text: str):
    findings = []
    for name, sev, rx in RULES:
        for m in rx.finditer(text):
            line = text.count("\n", 0, m.start()) + 1
            findings.append({
                "rule": name,
                "severity": sev,
                "file": str(path),
                "line": line,
                "match": m.group(0)[:200],
            })
    for i, ch in enumerate(text):
        cat = unicodedata.category(ch)
        if cat == "Cf" and ch not in {"\n", "\r", "\t"}:
            line = text.count("\n", 0, i) + 1
            findings.append({
                "rule": "format_control_unicode",
                "severity": "HIGH",
                "file": str(path),
                "line": line,
                "match": f"U+{ord(ch):04X} {unicodedata.name(ch, 'UNKNOWN')}",
            })
            break
    return findings

def scan_package_json(path: Path):
    findings = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return [{"rule":"invalid_package_json","severity":"MEDIUM","file":str(path),"line":1,"match":str(e)}]
    scripts = data.get("scripts", {}) or {}
    for key in INSTALL_HOOK_KEYS:
        if key in scripts:
            findings.append({
                "rule": "install_hook",
                "severity": "HIGH",
                "file": str(path),
                "line": 1,
                "match": f"{key}: {scripts[key]}",
            })
    return findings

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", nargs="?", default="skills")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    root = Path(args.path)
    if not root.exists():
        print(f"Path not found: {root}", file=sys.stderr)
        return 2

    findings = []
    binaries = []
    for path in iter_files(root):
        if path.name == "package.json":
            findings.extend(scan_package_json(path))
        if path.suffix.lower() in TEXT_EXT or path.name in {"SKILL.md", "Dockerfile"}:
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                binaries.append(str(path))
                continue
            findings.extend(scan_text(path, text))
        elif path.stat().st_size > 0:
            try:
                path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                binaries.append(str(path))

    for p in binaries:
        findings.append({
            "rule": "opaque_or_binary_file",
            "severity": "HIGH",
            "file": p,
            "line": 1,
            "match": "Manual provenance/malware review required",
        })

    rank = {"LOW":1, "MEDIUM":2, "HIGH":3, "CRITICAL":4}
    findings.sort(key=lambda f: (-rank[f["severity"]], f["file"], f["line"]))

    if args.json:
        print(json.dumps({"findings": findings}, indent=2, ensure_ascii=False))
    else:
        for f in findings:
            print(f'{f["severity"]:8} {f["rule"]:28} {f["file"]}:{f["line"]}  {f["match"]}')
        print(f"\nFindings: {len(findings)}")

    return 1 if any(f["severity"] in {"HIGH", "CRITICAL"} for f in findings) else 0

if __name__ == "__main__":
    raise SystemExit(main())
