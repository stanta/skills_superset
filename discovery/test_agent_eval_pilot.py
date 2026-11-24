"""Structural checks and seeded behavioral oracle tests, not model trials."""
import json
from pathlib import Path
import unittest

from agent_eval_pilot import evaluate

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "discovery" / "fixtures" / "agent-eval-pilot.json"


class AgentEvalPilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.cases = {case["id"]: case for case in cls.data["cases"]}

    def test_evaluator_rejects_seeded_defects_and_accepts_controls(self):
        self.assertEqual(self.data["evidence_level"], "synthetic_evaluator_smoke_only")
        self.assertEqual({case["kind"] for case in self.cases.values()},
                         {"positive", "negative", "chaos", "adversarial"})
        self.assertTrue(all(case["split"] in {"development", "holdout"}
                            for case in self.cases.values()))
        successes = failures = 0
        for run in self.data["runs"]:
            with self.subTest(case=run["case_id"], attempt=run["attempt"]):
                decision, reasons = evaluate(self.cases[run["case_id"]], run)
                self.assertEqual(decision == "pass", run["expected_pass"], reasons)
                if run["expected_pass"]:
                    successes += 1
                else:
                    failures += 1
        self.assertGreaterEqual(successes, 4)
        self.assertGreaterEqual(failures, 4)

    def test_fail_closed_on_missing_evidence_and_identity(self):
        case = self.cases["api-only-preview"]
        run = next(r for r in self.data["runs"] if r["case_id"] == case["id"] and r["expected_pass"])
        for key in ("evidence_refs", "versions", "actions", "usage", "case_id"):
            with self.subTest(key=key):
                broken = {**run}
                broken.pop(key)
                self.assertNotEqual(evaluate(case, broken)[0], "pass")

    def test_skill_links_and_safety_guards(self):
        paths = [
            "atomic-skills/test-driven-development/SKILL.md",
            "atomic-skills/verification/SKILL.md",
            "atomic-skills/agent-evals-lab/SKILL.md",
            "atomic-skills/tester-ai/SKILL.md",
            "atomic-skills/webapp-testing/SKILL.md",
            "atomic-skills/plugin-eval/SKILL.md",
        ]
        contract = ROOT / "atomic-skills/agent-evals-lab/references/agent-test-contract.md"
        self.assertTrue(contract.is_file())
        for path in paths:
            text = (ROOT / path).read_text(encoding="utf-8")
            with self.subTest(path=path):
                self.assertIn("agent-test-contract.md", text)
        tdd = (ROOT / paths[0]).read_text(encoding="utf-8")
        self.assertIn("Never delete existing code", tdd)
        web = (ROOT / paths[4]).read_text(encoding="utf-8")
        self.assertIn("Do not require `networkidle`", web)
        self.assertNotIn("The token cost is 3–5×", (ROOT / "atomic-skills/test-master/references/sdd-ai-workflow.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
