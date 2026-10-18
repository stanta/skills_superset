"""Maintainer-only structural tests; no network, builds or store publication."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "atomic-skills" / "google-play-publishing"
OWNERS = ("meta-mobile-desktop", "meta-devops-cloud")


class GooglePlayPublishingStructureTests(unittest.TestCase):
    def test_skill_frontmatter_and_scope(self):
        body = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(body.startswith("---\nname: google-play-publishing\ndescription: >\n"))
        self.assertIn('last_verified: "2026-10-15"', body)
        self.assertLess(len(body.splitlines()), 220)
        for term in ("native Android", "Flutter", "React Native/Expo", "Unity", "unknown", "authority"):
            self.assertIn(term, body)

    def test_local_markdown_links_resolve(self):
        files = list(SKILL.rglob("*.md")) + [ROOT / "docs/guides/google-play-publishing.md"]
        for source in files:
            body = source.read_text(encoding="utf-8")
            for target in re.findall(r"\]\(([^)]+)\)", body):
                if target.startswith(("https://", "http://", "#")):
                    continue
                resolved = (source.parent / target.split("#", 1)[0]).resolve()
                with self.subTest(source=source.relative_to(ROOT), target=target):
                    self.assertTrue(resolved.is_relative_to(ROOT.resolve()))
                    self.assertTrue(resolved.is_file(), str(resolved))

    def test_source_ledger_covers_claim_ids(self):
        ledger = (SKILL / "references/sources.md").read_text(encoding="utf-8")
        ids = set(re.findall(r"^## (S\d{2})\b", ledger, re.M))
        self.assertEqual(ids, {f"S{i:02}" for i in range(1, 35)})
        for source in list(SKILL.rglob("*.md")) + [ROOT / "docs/guides/google-play-publishing.md"]:
            referenced = set(re.findall(r"\bS\d{2}\b", source.read_text(encoding="utf-8")))
            self.assertFalse(referenced - ids, str(source))
        self.assertNotIn("/thread/", ledger)

    def test_template_is_unfilled_not_a_pass(self):
        template = json.loads((SKILL / "assets/release-readiness.template.json").read_text(encoding="utf-8"))
        self.assertEqual(template["mode"], "research")
        self.assertEqual(template["status"], "not_ready")
        self.assertIsNone(template["application"]["package_id"])
        self.assertIsNone(template["artifact"]["sha256"])
        self.assertTrue(all(value is None for value in template["approvals"].values()))
        checks = template["checks"]
        self.assertEqual(len(checks), len({check["id"] for check in checks}))
        self.assertGreaterEqual(len(checks), 10)
        self.assertTrue(all(check["status"] == "unknown" and not check["evidence"] for check in checks))
        self.assertTrue(all(item["applicability"] == "unknown" for item in template["conditional_modules"]))

    def test_behavioral_cases_are_not_claimed_as_runs(self):
        suite = json.loads((SKILL / "tests/evals.json").read_text(encoding="utf-8"))
        self.assertEqual(suite["evaluation_status"], "cases_authored_behavioral_runs_not_performed")
        cases = suite["cases"]
        self.assertEqual(len(cases), 18)
        self.assertEqual(len(cases), len({case["id"] for case in cases}))
        self.assertEqual(sum(not case["should_trigger"] for case in cases), 3)
        self.assertTrue(all(case["prompt"] and case["must"] for case in cases))

    def test_two_owner_catalogs_and_counts(self):
        actual_owners = set()
        for catalog in (ROOT / "skills").glob("meta-*/references/members.md"):
            body = catalog.read_text(encoding="utf-8")
            matches = [line for line in body.splitlines() if line.startswith("- **google-play-publishing**")]
            if not matches:
                continue
            actual_owners.add(catalog.parent.parent.name)
            self.assertEqual(len(matches), 1)
            self.assertTrue(matches[0].endswith("`../../../atomic-skills/google-play-publishing/SKILL.md`"))
            count = re.search(r"(?m)^(\d+) atomic skills\.", body)
            self.assertIsNotNone(count)
            self.assertEqual(int(count.group(1)), sum(line.startswith("- **") for line in body.splitlines()))
        self.assertEqual(actual_owners, set(OWNERS))

    def test_registry_and_navigation(self):
        registry = ROOT / "skills/meta-specialist-catalog/references/legacy-names.md"
        lines = [line for line in registry.read_text(encoding="utf-8").splitlines() if line.startswith("- **google-play-publishing**")]
        self.assertEqual(len(lines), 1)
        self.assertTrue(all(owner in lines[0] for owner in OWNERS))
        for owner in OWNERS:
            body = (ROOT / "skills" / owner / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("Google Play", body.split("---", 2)[1])
            self.assertIn("../../atomic-skills/google-play-publishing/SKILL.md", body)
        for path in (ROOT / "README.md", ROOT / "docs/metaskills.md"):
            self.assertIn("google-play-publishing", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
