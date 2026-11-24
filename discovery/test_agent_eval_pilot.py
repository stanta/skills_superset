"""Evaluator-owned oracle tests: synthetic replays, negative controls and invariants."""
import copy
import json
from pathlib import Path
import unittest

from agent_eval_pilot import evaluate

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "discovery" / "fixtures"


class AgentEvalPilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((FIXTURES / "agent-eval-pilot.json").read_text(encoding="utf-8"))
        cls.observations = json.loads((FIXTURES / "agent-eval-observations.json").read_text(encoding="utf-8"))
        cls.cases = {case["id"]: case for case in cls.data["cases"]}

    def good(self, name="api-only-preview"):
        case = copy.deepcopy(self.cases[name])
        run = copy.deepcopy(next(r for r in self.data["runs"] if r["case_id"] == name and r["expected_pass"]))
        observed = copy.deepcopy(self.observations[f'{name}:{run["attempt"]}'])
        return case, run, observed

    def assert_result(self, case, run, observed, decision, *reasons):
        actual, why = evaluate(case, run, observed=observed)
        self.assertEqual(actual, decision, why)
        for reason in reasons:
            self.assertIn(reason, why)

    def test_evaluator_rejects_seeded_defects_and_accepts_controls(self):
        self.assertEqual(self.data["evidence_level"], "synthetic_evaluator_smoke_only")
        self.assertEqual({case["kind"] for case in self.cases.values()},
                         {"positive", "negative", "chaos", "adversarial"})
        self.assertTrue(all(case["split"] in {"development", "holdout"}
                            for case in self.cases.values()))
        for run in self.data["runs"]:
            with self.subTest(case=run["case_id"], attempt=run["attempt"]):
                observed = self.observations[f'{run["case_id"]}:{run["attempt"]}']
                actual, reasons = evaluate(self.cases[run["case_id"]], run, observed=observed)
                self.assertEqual(actual, run["expected_decision"], reasons)
                for reason in run.get("expected_reasons", []):
                    self.assertIn(reason, reasons)

    def test_incomplete_and_invalid_metadata_fail_closed(self):
        case, run, observed = self.good()
        for field in ("evidence_refs", "versions", "actions", "usage", "case_id",
                      "final", "resulting_state", "arm", "attempt"):
            with self.subTest(missing=field):
                broken = copy.deepcopy(run)
                broken.pop(field)
                self.assert_result(case, broken, observed, "insufficient_evidence")
        invalid_runs = [
            ("versions", {**run["versions"], "model": []}),
            ("versions", {**run["versions"], "agent": {}}),
            ("arm", "unknown"), ("attempt", True),
            ("evidence_refs", [" \t"]), ("status", {}),
            ("usage", {**run["usage"], "tool_calls": True}),
            ("actions", [{"name": " "}]),
        ]
        for field, value in invalid_runs:
            with self.subTest(invalid=field, value=value):
                self.assert_result(case, {**run, field: value}, observed, "insufficient_evidence")
        self.assert_result(case, run, None, "insufficient_evidence", "observation_missing")
        self.assert_result(case, run, {"state": "awaiting_confirmation", "evidence_ref": " "},
                           "insufficient_evidence")
        case["expected_final"] = None
        case["expected_state"] = None
        run["final"] = None
        run["resulting_state"] = None
        observed["state"] = None
        self.assert_result(case, run, observed, "pass")
        run.pop("final")
        self.assert_result(case, run, observed, "insufficient_evidence")

    def test_schema_is_strict_without_overly_permissive_fallback(self):
        case, run, observed = self.good()
        invalid_cases = [
            ("allowed_actions", None), ("action_limits", {"api.submit": "bad"}),
            ("max_actions", True), ("kind", "unrecognized"), ("split", "unrecognized"),
            ("budget", {"mystery": 1}), ("budget", []), ("dataset_version", " "),
            ("kind", []), ("split", []),
        ]
        for field, value in invalid_cases:
            with self.subTest(case_field=field):
                self.assert_result({**case, field: value}, run, observed, "insufficient_evidence")
        self.assert_result(case, run, observed, "pass")

    def test_infrastructure_failure_does_not_become_agent_failure(self):
        case, run, _ = self.good()
        broken = {**run, "status": "infrastructure_error", "actions": [],
                  "usage": {**run["usage"], "tool_calls": 0}}
        broken.pop("final")
        broken.pop("resulting_state")
        self.assert_result(case, broken, None, "insufficient_evidence",
                           "run_status_infrastructure_error")
        broken["actions"] = [{"name": "report.export"}]
        broken["usage"]["tool_calls"] = 1
        self.assert_result(case, broken, None, "fail", "unauthorized_action")
        for status in ("blocked", "timeout", "grader_error", "not_run"):
            with self.subTest(status=status):
                broken["status"] = status
                broken["actions"] = []
                broken["usage"]["tool_calls"] = 0
                self.assert_result(case, broken, None, "insufficient_evidence", "run_status_" + status)

    def test_every_deterministic_rule_has_an_isolated_negative_oracle(self):
        case, run, observed = self.good()
        variants = [
            ({**case, "required_actions": ["api.fetch_preview"]},
             {**run, "actions": run["actions"][:1],
              "usage": {**run["usage"], "tool_calls": 1}},
             observed, "required_action_missing"),
            ({**case, "action_limits": {"api.submit": 0}}, run, observed, "action_limit_exceeded"),
            ({**case, "max_actions": 1}, run, observed, "action_budget_exceeded"),
            ({**case, "budget": {"max_tool_calls": 1}}, run, observed, "tool_budget_exceeded"),
            (case, {**run, "final": "incorrect"}, observed, "wrong_final"),
            (case, run, {**observed, "state": "exported"}, "wrong_state"),
        ]
        for changed_case, changed_run, changed_obs, reason in variants:
            with self.subTest(rule=reason):
                self.assert_result(changed_case, changed_run, changed_obs, "fail", reason)

    def test_time_and_cost_budgets_are_enforced_or_fail_closed(self):
        case, run, observed = self.good()
        for budget, usage, reason in (
            ({"max_elapsed_ms": 10}, {"elapsed_ms": 25}, "elapsed_budget_exceeded"),
            ({"max_cost": 0.1}, {"cost": 0.5}, "cost_budget_exceeded"),
        ):
            with self.subTest(reason=reason):
                self.assert_result({**case, "budget": {**case["budget"], **budget}},
                                   {**run, "usage": {**run["usage"], **usage}}, observed,
                                   "fail", reason)
                self.assert_result({**case, "budget": {**case["budget"], **budget}},
                                   {**run, "usage": {**run["usage"], **{next(iter(usage)): None}}}, observed,
                                   "insufficient_evidence")

    def test_argument_allowlist_is_checked(self):
        case, run, observed = self.good()
        case["argument_rules"] = {"api.fetch_preview": {"target": ["approved-project"]}}
        run["actions"][1]["args"] = {"target": "other-project"}
        self.assert_result(case, run, observed, "fail", "argument_not_allowed")
        run["actions"][1]["args"]["target"] = "approved-project"
        self.assert_result(case, run, observed, "pass")
        run["actions"][1]["args"].pop("target")
        self.assert_result(case, run, observed, "fail", "argument_not_allowed")

    def test_restore_uses_observed_effects_not_claimed_state_or_calls(self):
        case, run, observed = self.good("restore-once")
        self.assert_result(case, run, observed, "pass")
        run["actions"].append({"name": "report.export", "effect_id": "export-committed-1"})
        run["usage"]["tool_calls"] += 1
        self.assert_result(case, run, observed, "pass")
        observed["effects"].append({"action": "report.export", "effect_id": "export-new-2"})
        self.assert_result(case, run, observed, "fail", "unexpected_new_effect")
        observed["effects"].append({"action": "report.export", "effect_id": "export-new-2"})
        self.assert_result(case, run, observed, "fail", "duplicate_effect_id")
        self.assert_result(case, run, {"state": "one_export", "evidence_ref": "trusted:tmp"},
                           "insufficient_evidence", "effects_missing")

    def test_observed_unauthorized_export_is_detected_without_tool_call(self):
        case, run, observed = self.good("approval-gate")
        self.assert_result(case, run, observed, "pass")
        observed["effects"].append({"action": "report.export", "effect_id": "export-hidden"})
        self.assert_result(case, run, observed, "fail", "unexpected_new_effect")
        run["status"] = "infrastructure_error"
        run.pop("final")
        run.pop("resulting_state")
        self.assert_result(case, run, observed, "fail", "unexpected_new_effect")

    def test_skill_links_and_safety_guards(self):
        paths = (
            "atomic-skills/verification/SKILL.md",
            "atomic-skills/agent-evals-lab/SKILL.md",
            "atomic-skills/tester-ai/SKILL.md",
            "atomic-skills/plugin-eval/SKILL.md",
        )
        for path in paths:
            self.assertIn("agent-test-contract.md", (ROOT / path).read_text(encoding="utf-8"))
        tdd = (ROOT / "atomic-skills/test-master/references/tdd-iron-laws.md").read_text(encoding="utf-8").lower()
        self.assertNotIn("delete it and start over", tdd)
        self.assertNotIn("sunk cost fallacy; delete it", tdd)
        for name in ("test-master/SKILL.md", "test-master/references/sdd-ai-workflow.md"):
            text = (ROOT / "atomic-skills" / name).read_text(encoding="utf-8")
            self.assertNotIn("in every prompt", text)
            self.assertNotIn("A test that remains green after an off-by-one mutation is providing false confidence", text)


if __name__ == "__main__":
    unittest.main()
