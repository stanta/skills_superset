"""Structural checks only; these do not measure viewer retention or agent quality."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "atomic-skills" / "catch-attention"
GROUPS = [
    ("01-hooks.md", 1, 10),
    ("02-curiosity.md", 11, 22),
    ("03-empathy.md", 23, 32),
    ("04-conflict.md", 33, 44),
    ("05-thinking.md", 45, 54),
    ("06-emotion.md", 55, 64),
    ("07-editing.md", 65, 70),
]


class CatchAttentionStructureTests(unittest.TestCase):
    def test_portable_skill_and_references(self):
        body = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(body.startswith("---\nname: catch-attention\ndescription:"))
        for mode in ("create", "rewrite", "audit", "hooks", "explain", "analyze-retention"):
            self.assertIn(mode, body)
        for name, _, _ in GROUPS:
            self.assertIn("references/" + name, body)
        self.assertLess(len(body.splitlines()), 500)
        self.assertTrue((SKILL / "agents/openai.yaml").is_file())
        self.assertFalse((ROOT / "skills/catch-attention/SKILL.md").exists())

    def test_all_seventy_complete_cards(self):
        total = []
        for name, start, end in GROUPS:
            body = (SKILL / "references" / name).read_text(encoding="utf-8")
            matches = list(re.finditer(r"^## ATT-(\d{2}) — .+$", body, re.M))
            ids = [int(match.group(1)) for match in matches]
            self.assertEqual(ids, list(range(start, end + 1)), name)
            total.extend(ids)
            for index, match in enumerate(matches):
                stop = matches[index + 1].start() if index + 1 < len(matches) else len(body)
                card = body[match.end():stop]
                for field in ("Суть", "Как применить", "Реальный пример", "Оригинальная мини-сцена", "Ошибка"):
                    self.assertIn("**" + field + ".**", card, (name, match.group(1), field))
                self.assertRegex(card, r"\[S\d{2}\]\(sources\.md#s\d{2}\)")
        self.assertEqual(total, list(range(1, 71)))

    def test_relative_markdown_links_and_source_anchors(self):
        for path in SKILL.rglob("*.md"):
            body = path.read_text(encoding="utf-8")
            for target in re.findall(r"\[[^\]\n]*\]\(([^)\s]+)\)", body):
                if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                    continue
                relative, _, fragment = target.partition("#")
                destination = (path.parent / relative).resolve() if relative else path.resolve()
                self.assertTrue(destination.is_file(), (path, target))
                if fragment.startswith("s") and re.fullmatch(r"s\d{2}", fragment):
                    text = destination.read_text(encoding="utf-8")
                    self.assertIn('id="' + fragment + '"', text, (path, target))
        sources = (SKILL / "references/sources.md").read_text(encoding="utf-8")
        anchors = re.findall(r'<a id="(s\d{2})"></a>', sources)
        self.assertEqual(anchors, [f"s{i:02d}" for i in range(1, 36)])

    def test_evaluation_cases_are_specs_not_results(self):
        spec = json.loads((SKILL / "evals/cases.json").read_text(encoding="utf-8"))
        self.assertEqual(spec["skill"], "catch-attention")
        self.assertEqual(spec["status"], "not_run")
        self.assertEqual(spec["measured_retention_effect"], "unknown")
        self.assertEqual(spec["behavioral_runs"], [])
        cases = spec["cases"]
        self.assertEqual(len(cases), 12)
        self.assertEqual(len({case["id"] for case in cases}), 12)
        self.assertEqual({case["category"] for case in cases}, {"positive", "negative", "adversarial"})
        for case in cases:
            for key in ("id", "category", "mode", "input", "expected", "forbidden"):
                self.assertTrue(case[key], (case["id"], key))
            self.assertIsInstance(case["expected"], list)
            self.assertIsInstance(case["forbidden"], list)

    def test_navigation(self):
        catalog = ROOT / "skills/meta-media-production/references/members.md"
        registry = ROOT / "skills/meta-specialist-catalog/references/legacy-names.md"
        child = "../../../atomic-skills/catch-attention/SKILL.md"
        for path in (catalog, registry):
            lines = [line for line in path.read_text(encoding="utf-8").splitlines()
                     if line.startswith("- **catch-attention**")]
            self.assertEqual(len(lines), 1, str(path))
            self.assertTrue(lines[0].endswith("`" + child + "`"))
            self.assertEqual((path.parent / child).resolve(), (SKILL / "SKILL.md").resolve())
        self.assertIn("— meta-media-production —", lines[0])


if __name__ == "__main__":
    unittest.main()
