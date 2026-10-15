"""Structural checks only; behavioral evaluation requires executing eval cases."""
import datetime
import json
from pathlib import Path
import re
import unittest
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
ID = "apple-app-store-publishing"
SKILL = ROOT / "atomic-skills" / ID
LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


class AppStoreSkillTests(unittest.TestCase):
    def test_frontmatter_and_progressive_disclosure(self):
        body = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(body.startswith("---\nname: " + ID + "\ndescription: >\n"))
        stamp = re.search(r'last_verified: "(\d{4}-\d{2}-\d{2})"', body)
        self.assertIsNotNone(stamp)
        datetime.date.fromisoformat(stamp.group(1))
        self.assertLess(len(body.splitlines()), 300)
        self.assertIn("framework-and-agent-neutral", body)

    def test_internal_links_and_source_anchors(self):
        for source in SKILL.rglob("*.md"):
            body = source.read_text(encoding="utf-8")
            for raw in LINK.findall(body):
                parsed = urlsplit(raw)
                if parsed.scheme:
                    self.assertEqual(parsed.scheme, "https", (source, raw))
                    continue
                target = (source.parent / parsed.path).resolve() if parsed.path else source.resolve()
                target.relative_to(SKILL.resolve())
                self.assertTrue(target.is_file(), (source, raw))
                if parsed.fragment and re.fullmatch(r"s\d+", parsed.fragment):
                    self.assertIn("## " + parsed.fragment.upper() + "\n", target.read_text(encoding="utf-8"))

    def test_primary_source_ledger(self):
        body = (SKILL / "references/sources.md").read_text(encoding="utf-8")
        links = [urlsplit(raw) for raw in LINK.findall(body)]
        external = [item for item in links if item.scheme]
        self.assertGreaterEqual(len(external), 20)
        for item in external:
            self.assertIn(item.hostname, {"developer.apple.com", "docs.flutter.dev", "docs.expo.dev"})
        self.assertIn("effective date", body)
        self.assertIn("Future: April 2027", body)
        self.assertIn("100 bytes", body)
        self.assertIn("100 characters", body)

    def test_evaluation_cases_are_explicit_and_unique(self):
        data = json.loads((SKILL / "evals/cases.json").read_text(encoding="utf-8"))
        self.assertEqual(data["skill"], ID)
        self.assertIn("Structural CI does not constitute", data["protocol"])
        cases = data["cases"]
        self.assertEqual(len(cases), len({case["id"] for case in cases}))
        self.assertGreaterEqual(sum(case["should_trigger"] for case in cases), 8)
        self.assertGreaterEqual(sum(not case["should_trigger"] for case in cases), 3)
        for case in cases:
            self.assertTrue(case["prompt"])
            self.assertTrue(case["required"])
            self.assertTrue(case["forbidden"])

    def test_exactly_two_catalog_owners_and_registry(self):
        prefix = "- **" + ID + "**"
        owners = set()
        for catalog in (ROOT / "skills").glob("meta-*/references/members.md"):
            entries = [line for line in catalog.read_text(encoding="utf-8").splitlines() if line.startswith(prefix)]
            self.assertLessEqual(len(entries), 1)
            if entries:
                owners.add(catalog.parent.parent.name)
                self.assertTrue(entries[0].endswith("`../../../atomic-skills/" + ID + "/SKILL.md`"))
        self.assertEqual(owners, {"meta-mobile-desktop", "meta-devops-cloud"})
        registry = ROOT / "skills/meta-specialist-catalog/references/legacy-names.md"
        entries = [line for line in registry.read_text(encoding="utf-8").splitlines() if line.startswith(prefix)]
        self.assertEqual(len(entries), 1)
        self.assertIn("meta-mobile-desktop", entries[0])
        self.assertIn("meta-devops-cloud", entries[0])

    def test_task_template_has_evidence_and_authority_contract(self):
        body = (SKILL / "templates/release-plan.md").read_text(encoding="utf-8")
        for field in ("depends_on:", "owner:", "acceptance_criteria:", "expected_evidence_artifacts:", "human_gate:", "external_side_effects:", "status: BLOCKED"):
            self.assertIn(field, body)
        self.assertTrue((SKILL / "templates/review-notes.md").is_file())


if __name__ == "__main__":
    unittest.main()
