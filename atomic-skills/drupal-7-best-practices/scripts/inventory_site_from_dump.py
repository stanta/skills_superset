#!/usr/bin/env python3
"""Inventory a Drupal 7 site from a mysqldump file.

Reads the `system` table to report the core version and the module/theme list,
so a site can be reconstructed from a database dump alone.

Usage:
    python3 inventory_site_from_dump.py path/to/dump.sql
"""
import re
import sys
from collections import defaultdict

# system table row: (filename, name, type, owner, status, bootstrap, schema_version, weight, info)
ROW_RE = re.compile(
    r"\(\s*'((?:[^']|'')*)'\s*,\s*'((?:[^']|'')*)'\s*,\s*'((?:[^']|'')*)'\s*,\s*'((?:[^']|'')*)'\s*,"
    r"\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*,"
)


def unescape(s):
    return s.replace("''", "'").replace("\\'", "'")


def main(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        data = fh.read()

    rows = []
    for m in ROW_RE.finditer(data):
        filename, name, typ, owner, status, bootstrap, schema_version, weight = m.groups()
        rows.append({
            "filename": unescape(filename),
            "name": unescape(name),
            "type": unescape(typ),
            "owner": unescape(owner),
            "status": int(status),
            "bootstrap": int(bootstrap),
            "schema_version": int(schema_version),
            "weight": int(weight),
        })

    if not rows:
        print("No `system` table rows found — is this a Drupal dump?")
        return 1

    system = next((r for r in rows if r["name"] == "system" and r["type"] == "module"), None)
    core_version = None
    if system and 7000 <= system["schema_version"] <= 7999:
        core_version = "7.%d" % (system["schema_version"] % 1000)

    modules = [r for r in rows if r["type"] == "module"]
    themes = [r for r in rows if r["type"] == "theme"]

    def is_contrib(r):
        return r["filename"].startswith("sites/")

    enabled_modules = [r for r in modules if r["status"] == 1]
    enabled_themes = [r for r in themes if r["status"] == 1]
    disabled_modules = [r for r in modules if r["status"] == 0]

    contrib_mods = sorted([r for r in enabled_modules if is_contrib(r)], key=lambda r: r["name"])
    core_mods = sorted([r for r in enabled_modules if not is_contrib(r)], key=lambda r: r["name"])

    print("=" * 60)
    print("DRUPAL 7 SITE INVENTORY")
    print("=" * 60)
    print("Core version:      %s" % (core_version or "unknown (system schema_version=%s)" % (system["schema_version"] if system else "?")))
    print("Total system rows: %d" % len(rows))
    print()
    print("Enabled contrib modules (%d) — MUST be restored to sites/all/modules:" % len(contrib_mods))
    for r in contrib_mods:
        print("  %-35s %s" % (r["name"], r["filename"]))
    print()
    print("Enabled core modules (%d):" % len(core_mods))
    print("  " + ", ".join(r["name"] for r in core_mods))
    print()
    print("Enabled themes (%d) — restore to sites/all/themes:" % len(enabled_themes))
    for r in enabled_themes:
        print("  %-35s %s" % (r["name"], r["filename"]))
    print()
    print("Disabled modules (%d) — safe to omit:" % len(disabled_modules))
    print("  " + ", ".join(sorted(r["name"] for r in disabled_modules)))
    print()
    print("Next steps:")
    print("  1. Restore Drupal core %s" % core_version)
    print("  2. Restore the %d contrib modules above (from git or drupal.org)" % len(contrib_mods))
    print("  3. Create sites/default/settings.php with DB credentials")
    print("  4. Recreate sites/default/files/ and chmod writable")
    print("  5. drush rr && drush cc all && drush updb")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    sys.exit(main(sys.argv[1]))
