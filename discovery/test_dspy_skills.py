"""Static checks for DSPy-derived Agent Skills and their two-meta navigation."""
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "atomic-skills"
MANIFEST = ROOT / "discovery" / "dspy-skills.json"

class DSPySkillsTest(unittest.TestCase):
    def test_all_twelve_are_complete_and_discoverable(self):
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        defs = data["skills"]
        self.assertEqual(len(defs), 12)
        self.assertEqual(len({d["id"] for d in defs}), 12)
        registry = (ROOT / "skills/meta-specialist-catalog/references/legacy-names.md").read_text(encoding="utf-8")
        for d in defs:
            sid = d["id"]
            folder = SKILLS / sid
            skill = (folder / "SKILL.md").read_text(encoding="utf-8")
            self.assertTrue(skill.startswith("---\nname: " + sid + "\ndescription:"))
            self.assertIn("## Acceptance checks", skill)
            self.assertIn("## Boundaries and failure handling", skill)
            for rel in ["references/playbook.md", "references/sources.md", "evals/cases.json", "agents/openai.yaml"]:
                self.assertTrue((folder / rel).is_file(), f"{sid}/{rel}")
            cases = json.loads((folder / "evals/cases.json").read_text(encoding="utf-8"))
            self.assertEqual(len(cases["cases"]), 4)
            self.assertFalse(cases["executed"])
            self.assertEqual(len(d["owners"]), 2)
            self.assertEqual(registry.count("- **" + sid + "**"), 1)
            for meta in d["owners"]:
                members = (ROOT / "skills" / meta / "references/members.md").read_text(encoding="utf-8")
                self.assertEqual(members.count("- **" + sid + "**"), 1)
                self.assertIn("../../../atomic-skills/" + sid + "/SKILL.md", members)

if __name__ == "__main__":
    unittest.main()
