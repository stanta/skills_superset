"""Regression checks for the historical inventory's layout-aware CI gate."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import unittest


ROOT = Path(__file__).resolve().parent.parent


class SecurityBaselineTests(unittest.TestCase):
    def validator_source(self):
        workflow = (ROOT / ".github/workflows/skill-security-audit.yml").read_text()
        section = workflow.split("      - name: Validate security capability manifests\n", 1)[1]
        body = section.split("          python3 - <<'PY'\n", 1)[1].split("\n          PY", 1)[0]
        return textwrap.dedent(body)

    def make_fixture(self, root):
        skill = root / "atomic-skills/demo"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("safe\n")
        manifest = {"version": 1, "risk_tier": "S1", "capabilities": {}}
        (skill / "security-manifest.json").write_text(json.dumps(manifest))
        security = root / "security"
        security.mkdir()
        (security / "skills-security-inventory.json").write_text(json.dumps({
            "skill_root": "atomic-skills", "skills": [{"skill": "demo"}]
        }))
        return skill

    def run_validator(self, root):
        return subprocess.run([sys.executable, "-c", self.validator_source()],
                              cwd=root, capture_output=True, text=True)

    def test_unbaselined_packages_are_reported_not_invented(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.make_fixture(root)
            other = root / "skills/meta-demo"
            other.mkdir(parents=True)
            (other / "SKILL.md").write_text("safe\n")
            result = self.run_validator(root)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Coverage gap: 1", result.stdout)
            self.assertIn("1 packages without manifests", result.stdout)

    def test_inventory_package_cannot_omit_manifest(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            skill = self.make_fixture(root)
            (skill / "security-manifest.json").unlink()
            result = self.run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing security-manifest.json", result.stderr)

    def test_existing_manifests_outside_inventory_are_validated(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.make_fixture(root)
            other = root / "atomic-skills/extra"
            other.mkdir()
            (other / "SKILL.md").write_text("safe\n")
            (other / "security-manifest.json").write_text("{broken")
            result = self.run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("invalid JSON", result.stderr)

    def test_all_historical_inventory_entries_have_exact_manifests(self):
        inventory = json.loads((ROOT / "security/skills-security-inventory.json").read_text())
        self.assertEqual(inventory["skill_root"], "atomic-skills")
        self.assertEqual(len(inventory["skills"]), 160)
        for entry in inventory["skills"]:
            skill = ROOT / "atomic-skills" / entry["skill"]
            self.assertTrue((skill / "SKILL.md").is_file(), str(skill))
            data = json.loads((skill / "security-manifest.json").read_text())
            self.assertEqual(data["risk_tier"], entry["risk_tier"])
        result = self.run_validator(ROOT)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
