"""Local structural checks. These do not evaluate story quality or attention gains."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


class SkillStructureTests(unittest.TestCase):
    def test_frontmatter_and_identity(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\nname: magical-storyteller\ndescription:"))
        self.assertIn('display_name: "Волшебный сказочник"', text)
        self.assertEqual(len(text.split("---", 2)), 3)

    def test_31_functions(self):
        functions = load("assets/functions.json")["functions"]
        self.assertEqual([f["number"] for f in functions], list(range(1, 32)))
        self.assertEqual([f["id"] for f in functions], [f"F{i:02d}" for i in range(1, 32)])
        self.assertEqual(functions[7]["variants"], ["harm", "lack"])
        self.assertFalse(load("assets/functions.json")["initial_situation_is_function"])

    def test_function_reference_matches(self):
        text = (ROOT / "references/functions.md").read_text(encoding="utf-8")
        self.assertEqual(len(re.findall(r"^## F\d{2}\. ", text, flags=re.M)), 31)
        for f in load("assets/functions.json")["functions"]:
            self.assertIn(f"## {f['id']}. {f['name']}", text)
            for field in ("meaning", "writing_use", "original_example", "common_mistake"):
                self.assertIn(f[field], text)

    def test_local_markdown_links(self):
        checked = 0
        for source in ROOT.rglob("*.md"):
            for raw in re.findall(r"\[[^\]]*\]\(([^)]+)\)", source.read_text(encoding="utf-8")):
                if raw.startswith(("https://", "http://", "#")):
                    continue
                target = (source.parent / raw.split("#", 1)[0]).resolve()
                self.assertTrue(target.is_relative_to(ROOT.resolve()), (source, raw))
                self.assertTrue(target.is_file(), (source, raw))
                checked += 1
        self.assertGreaterEqual(checked, 13)

    def test_scene_identifiers_and_causality(self):
        plan = load("assets/example-plan.json")
        scenes = plan["scenes"]
        ids = [s["id"] for s in scenes]
        self.assertEqual(len(ids), len(set(ids)))
        move_ids = {m["id"] for m in plan["moves"]}
        order = {s["id"]: s["story_order"] for s in scenes}
        valid = {f"F{i:02d}" for i in range(1, 32)}
        for field in ("story_order", "presentation_order"):
            self.assertEqual(sorted(s[field] for s in scenes), list(range(1, len(scenes) + 1)))
        for scene in scenes:
            self.assertIn(scene["move_id"], move_ids)
            self.assertTrue(set(scene["function_ids"]) <= valid)
            for parent in scene["caused_by"]:
                self.assertIn(parent, ids)
                self.assertLess(order[parent], scene["story_order"])
        for loop in plan["open_loops"]:
            self.assertIn(loop["introduced_in"], ids)
            if loop["resolved_in"] is None:
                self.assertTrue(loop["intentional_open"])
            else:
                self.assertIn(loop["resolved_in"], ids)

    def test_schema_function_enum(self):
        schema = load("assets/story-plan.schema.json")
        values = schema["properties"]["scenes"]["items"]["properties"]["function_ids"]["items"]["enum"]
        self.assertEqual(values, [f"F{i:02d}" for i in range(1, 32)])
        plan = load("assets/example-plan.json")
        self.assertTrue(set(schema["required"]) <= set(plan))
        self.assertTrue(set(plan) <= set(schema["properties"]))

    def test_behavioral_specs_honest(self):
        cases = load("evals/cases.json")
        self.assertEqual(cases["status"], "specified_not_behaviorally_run")
        self.assertEqual(len(cases["cases"]), 15)
        self.assertEqual(len({c["id"] for c in cases["cases"]}), 15)
        for case in cases["cases"]:
            self.assertTrue(case["prompt"])
            self.assertTrue(case["expected"])

    def test_portability_and_optional_dependency(self):
        body = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("необязательное дополнение", body)
        self.assertIn("Отсутствие этого дополнения не блокирует работу", body)
        self.assertFalse((ROOT / "scripts").exists())
        self.assertIn("Создание текста не разрешает его публикацию", body)
        agent = (ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
        self.assertIn("$magical-storyteller", agent)

    def test_expected_resources(self):
        for name in ("morphology", "functions", "roles-and-character", "attention", "examples", "quality", "sources"):
            self.assertTrue((ROOT / f"references/{name}.md").is_file())
        self.assertTrue((ROOT / "assets/story-plan-template.md").is_file())


if __name__ == "__main__":
    unittest.main()
