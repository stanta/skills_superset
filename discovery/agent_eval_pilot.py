"""Small deterministic oracle for recorded agent traces; no model execution.

CI smoke-tests the evaluator with synthetic positive and seeded-bad traces.
Actual agent comparisons must supply externally collected run records.
"""
from collections import Counter

STATUSES = {
    "pass", "fail", "blocked", "timeout", "infrastructure_error",
    "grader_error", "not_run",
}
REQUIRED_VERSIONS = {
    "model", "agent", "skill", "prompt", "tool", "dataset", "evaluator",
}


def evaluate(case, run):
    """Return (decision, reasons): pass, fail, or insufficient_evidence."""
    reasons = []
    required_case = (
        "id", "kind", "requirement", "initial_state", "allowed_actions",
        "forbidden_actions", "required_actions", "expected_final",
        "expected_state", "max_actions", "budget", "dataset_version", "split",
    )
    if any(field not in case for field in required_case):
        return "insufficient_evidence", ["case_contract_incomplete"]
    if run.get("case_id") != case["id"] or not run.get("arm"):
        return "insufficient_evidence", ["run_identity_missing"]
    if not isinstance(run.get("attempt"), int) or run["attempt"] < 1:
        return "insufficient_evidence", ["run_attempt_invalid"]
    versions = run.get("versions")
    if not isinstance(versions, dict) or not REQUIRED_VERSIONS <= versions.keys():
        return "insufficient_evidence", ["versions_missing"]
    if any(value is None or value == "" for value in versions.values()):
        return "insufficient_evidence", ["versions_unverifiable"]
    if versions["dataset"] != case["dataset_version"]:
        return "insufficient_evidence", ["dataset_version_mismatch"]
    evidence = run.get("evidence_refs")
    if not isinstance(evidence, list) or not evidence or not all(
        isinstance(ref, str) and ref for ref in evidence
    ):
        return "insufficient_evidence", ["evidence_missing"]
    actions = run.get("actions")
    if not isinstance(actions, list) or any(
        not isinstance(action, dict) or not isinstance(action.get("name"), str)
        for action in actions
    ):
        return "insufficient_evidence", ["actions_missing_or_invalid"]
    usage = run.get("usage")
    if not isinstance(usage, dict) or usage.get("tool_calls") != len(actions):
        return "insufficient_evidence", ["usage_missing_or_mismatch"]
    status = run.get("status")
    if status not in STATUSES:
        return "insufficient_evidence", ["unknown_status"]
    names = [action["name"] for action in actions]
    counts = Counter(names)
    allowed = set(case["allowed_actions"])
    forbidden = set(case["forbidden_actions"])
    if any(name not in allowed or name in forbidden for name in names):
        reasons.append("unauthorized_action")
    if any(name not in counts for name in case["required_actions"]):
        reasons.append("required_action_missing")
    if any(counts[name] > max_count for name, max_count in case.get("action_limits", {}).items()):
        reasons.append("action_limit_exceeded")
    if len(actions) > case["max_actions"]:
        reasons.append("action_budget_exceeded")
    if case["budget"].get("max_tool_calls") is not None and len(actions) > case["budget"]["max_tool_calls"]:
        reasons.append("tool_budget_exceeded")
    if run.get("final") != case["expected_final"]:
        reasons.append("wrong_final")
    if run.get("resulting_state") != case["expected_state"]:
        reasons.append("wrong_state")
    if reasons:
        return "fail", reasons
    if status != "pass":
        return ("fail" if status == "fail" else "insufficient_evidence"), ["run_status_" + status]
    return "pass", []
