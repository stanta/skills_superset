"""CI-only acceptance tests for portable Anthropic skill adaptations."""
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "docs/imports/anthropic-portable-skills.json"


class PortableSkillImportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_all_31_source_packages_accounted_for(self):
        self.assertEqual(self.manifest["source_packages"], 31)
        self.assertEqual(self.manifest["imported_portable_skills"], 26)
        self.assertEqual(len(self.manifest["excluded_existing_or_examples"]), 5)
        self.assertEqual(len(self.manifest["imported"]), 26)
        self.assertEqual(
            len({s["target"] for s in self.manifest["imported"]}), 26
        )

    def test_skills_are_portable_and_licensed(self):
        for skill in self.manifest["imported"]:
            with self.subTest(skill=skill["target"]):
                folder = ROOT / skill["target"]
                content = (folder / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn("## Runtime-neutral contract", content)
                self.assertIn("## Procedure", content)
                self.assertIn("## Completion check", content)
                self.assertIn("## Provenance and adaptation", content)
                self.assertIn("license: Apache-2.0", content)
                self.assertTrue((folder / "LICENSE").is_file())
                self.assertIn("Apache License", (folder / "LICENSE").read_text())
                name = folder.name
                self.assertTrue(content.startswith("---\nname: " + name + "\n"))
                self.assertGreaterEqual(
                    len(re.findall(r"^\d+\. ", content, flags=re.MULTILINE)), 5
                )
                for forbidden in [
                    "CLAUDE_PLUGIN_ROOT",
                    "~/.claude/",
                    "Workflow(claude-security:",
                    "Bash(git ",
                    "/plugin install ",
                ]:
                    self.assertNotIn(forbidden, content)

    def test_meta_catalogs_and_exact_lookup(self):
        registry = (
            ROOT / "skills/meta-specialist-catalog/references/legacy-names.md"
        ).read_text(encoding="utf-8")
        for skill in self.manifest["imported"]:
            name = Path(skill["target"]).name
            relative = "../../../atomic-skills/" + name + "/SKILL.md"
            with self.subTest(skill=name):
                self.assertIn("- **" + name + "** — ", registry)
                self.assertIn(relative, registry)
                for meta in skill["metas"]:
                    catalog = (
                        ROOT / "skills" / meta / "references/members.md"
                    ).read_text(encoding="utf-8")
                    self.assertIn("- **" + name + "** — ", catalog)
                    self.assertIn(relative, catalog)
                    front = (ROOT / "skills" / meta / "SKILL.md").read_text(
                        encoding="utf-8"
                    ).split("---", 2)[1]
                    self.assertIn("Additional scope:", front)

    def test_manifest_has_pinned_and_auditable_provenance(self):
        self.assertEqual(
            self.manifest["pinned_commit"],
            "fa59bc9037741ecfa131aa27938272605710d7b2",
        )
        self.assertEqual(
            {x["license"] for x in self.manifest["imported"]},
            {"Apache-2.0"},
        )
        self.assertTrue(all(x["source"] and x["target"] for x in
                            self.manifest["imported"]))


if __name__ == "__main__":
    unittest.main()
