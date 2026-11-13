"""Structural checks for the DSPy-inspired suite; no model calls or benchmarks."""
from __future__ import annotations

import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILLS = (
    "task-contract-designer", "llm-eval-engineer", "prompt-optimizer",
    "few-shot-learning", "self-refinement", "long-context-research",
    "rag-optimizer", "tool-use-optimizer", "multi-step-reasoning",
    "model-cost-optimizer", "agent-architecture-evolver", "ai-regression-gate",
)
SECONDARY = {
    "llm-eval-engineer": "meta-testing-quality",
    "ai-regression-gate": "meta-testing-quality",
    "prompt-optimizer": "meta-machine-learning",
    "few-shot-learning": "meta-machine-learning",
    "model-cost-optimizer": "meta-machine-learning",
    "agent-architecture-evolver": "meta-machine-learning",
    "long-context-research": "meta-research-knowledge",
    "rag-optimizer": "meta-research-knowledge",
}
GUIDE = ROOT / "docs/guides/dspy-agent-skills.md"


class DSPySkillStructureTests(unittest.TestCase):
    def test_packages_have_contracts_references_and_optional_adapters(self):
        for skill_id in SKILLS:
            with self.subTest(skill=skill_id):
                package = ROOT / "atomic-skills" / skill_id
                skill = (package / "SKILL.md").read_text(encoding="utf-8")
                self.assertTrue(skill.startswith(f"---\nname: {skill_id}\ndescription:"))
                self.assertIn("license: MIT\n---", skill)
                for heading in (
                    "## When to use", "## Inputs", "## Procedure",
                    "## Deliverable and acceptance", "## Safety",
                ):
                    self.assertIn(heading, skill)
                self.assertLess(len(skill.splitlines()), 180)
                self.assertIn("references/playbook.md", skill)
                self.assertIn("evals/cases.json", skill)
                reference = (package / "references/playbook.md").read_text(encoding="utf-8")
                self.assertIn("https://dspy.ai/", reference)
                self.assertIn("2026-11-13", reference)
                adapter = (package / "agents/openai.yaml").read_text(encoding="utf-8")
                self.assertTrue(adapter.startswith("interface:\n"))
                # These adapters intentionally use only three quoted string fields.
                fields = dict(re.findall(r'^  (\w+): (".*")$', adapter, re.MULTILINE))
                self.assertEqual(set(fields), {"display_name", "short_description", "default_prompt"})
                values = {key: json.loads(value) for key, value in fields.items()}
                self.assertTrue(all(isinstance(value, str) and value.strip() for value in values.values()))
                self.assertIn(f"${skill_id}", values["default_prompt"])
                self.assertFalse((ROOT / "skills" / skill_id).exists())

    def test_behavioral_cases_are_specs_not_claimed_model_results(self):
        seen_ids: set[str] = set()
        for skill_id in SKILLS:
            with self.subTest(skill=skill_id):
                path = ROOT / "atomic-skills" / skill_id / "evals/cases.json"
                data = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(data["schema_version"], 1)
                self.assertEqual(data["skill"], skill_id)
                self.assertEqual(data["status"], "specification-only")
                cases = data["cases"]
                self.assertEqual(len(cases), 3)
                self.assertEqual({case["kind"] for case in cases}, {"positive", "negative", "adversarial"})
                for case in cases:
                    self.assertNotIn(case["id"], seen_ids)
                    seen_ids.add(case["id"])
                    self.assertIs(type(case["should_trigger"]), bool)
                    self.assertEqual(case["should_trigger"], case["kind"] != "negative")
                    self.assertIsInstance(case["prompt"], str)
                    self.assertTrue(case["prompt"].strip())
                    self.assertIsInstance(case["expected"], list)
                    self.assertTrue(case["expected"])
                    self.assertTrue(all(isinstance(item, str) and item.strip() for item in case["expected"]))
        self.assertEqual(len(seen_ids), 36)

    def test_memberships_counts_and_exact_name_registry(self):
        catalogs = {
            path.parent.parent.name: path.read_text(encoding="utf-8")
            for path in (ROOT / "skills").glob("meta-*/references/members.md")
        }
        registry = (ROOT / "skills/meta-specialist-catalog/references/legacy-names.md").read_text(encoding="utf-8")
        for skill_id in SKILLS:
            with self.subTest(skill=skill_id):
                prefix = f"- **{skill_id}** "
                expected = {"meta-agent-systems"}
                if skill_id in SECONDARY:
                    expected.add(SECONDARY[skill_id])
                actual = {
                    name for name, content in catalogs.items()
                    if any(line.startswith(prefix) for line in content.splitlines())
                }
                self.assertEqual(actual, expected)
                lines = [line for line in registry.splitlines() if line.startswith(prefix)]
                self.assertEqual(len(lines), 1)
                self.assertEqual(set(lines[0].split(" — ")[1].split(", ")), expected)
                self.assertTrue(lines[0].endswith(f"`../../../atomic-skills/{skill_id}/SKILL.md`"))
        for name in {"meta-agent-systems", *SECONDARY.values()}:
            with self.subTest(catalog=name):
                content = catalogs[name]
                count = re.search(r"^(\d+) atomic skills\.", content, re.MULTILINE)
                self.assertIsNotNone(count)
                entries = [line for line in content.splitlines() if line.startswith("- **")]
                self.assertEqual(int(count.group(1)), len(entries))

    def test_local_links_and_guide_navigation(self):
        files = [GUIDE]
        for skill_id in SKILLS:
            files.extend((ROOT / "atomic-skills" / skill_id).rglob("*.md"))
        for path in files:
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
                if target.startswith(("https://", "http://", "#")):
                    continue
                with self.subTest(file=str(path.relative_to(ROOT)), target=target):
                    resolved = (path.parent / target.split("#", 1)[0]).resolve()
                    self.assertTrue(resolved.is_relative_to(ROOT))
                    self.assertTrue(resolved.is_file(), f"Missing local link: {target}")
        guide = GUIDE.read_text(encoding="utf-8")
        for skill_id in SKILLS:
            self.assertIn(f"../../atomic-skills/{skill_id}/SKILL.md", guide)
        maintenance = (ROOT / "docs/metaskills.md").read_text(encoding="utf-8")
        self.assertIn("guides/dspy-agent-skills.md", maintenance)


if __name__ == "__main__":
    unittest.main()
