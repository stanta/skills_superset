import json
from pathlib import Path
import tempfile
import unittest
from skills_discovery import build, frontmatter, read_index, search, evaluate


class TestDiscovery(unittest.TestCase):
    def test_frontmatter(self):
        self.assertEqual(frontmatter("---\nname: example\ndescription: >\n  useful\n  tool\n---\nBODY"),
                         {"name": "example", "description": "useful tool"})

    def test_index_search_eval(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for slug, desc in [("react-debug", "React TypeScript runtime crash"),
                               ("gitlab-ci", "GitLab CI deployment pipeline")]:
                folder = root / "skills" / slug
                folder.mkdir(parents=True)
                (folder / "SKILL.md").write_text(
                    "---\nname: " + slug + "\ndescription: " + desc + "\n---\n",
                    encoding="utf-8")
            (root / "discovery").mkdir()
            (root / "discovery" / "overrides.json").write_text(
                json.dumps({"react-debug": {"aliases": ["react typescript error"]}}),
                encoding="utf-8")
            path = root / "skills-index.jsonl"
            self.assertEqual(build(root, path)[:2], (2, 0))
            self.assertEqual(build(root, path, check=True), (2, 2, True))
            rows = read_index(path)
            self.assertEqual(search("react typescript error", rows, 1)[0]["name"], "react-debug")
            self.assertEqual(search("GitLab CI deployment", rows, 1)[0]["name"], "gitlab-ci")
            dataset = root / "eval.jsonl"
            dataset.write_text('{"query":"react typescript error","expected":["react-debug"]}\n')
            self.assertEqual(evaluate(rows, dataset)["recall_at_1"], 1)
            (root / "skills" / "react-debug" / "SKILL.md").write_text(
                "---\nname: react-debug\ndescription: React component\n---\n")
            self.assertFalse(build(root, path, check=True)[2])
            self.assertEqual(build(root, path)[:2], (2, 1))

    def test_no_skill_and_negative(self):
        rows = [dict(name="deploy", path="skills/deploy/SKILL.md",
                     description="deploy pipeline", negative_intents=["do not deploy"])]
        self.assertEqual(search("", rows), [])
        self.assertEqual(search("do not deploy", rows), [])


if __name__ == "__main__":
    unittest.main()
