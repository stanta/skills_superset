"""Deterministic checks for recorded agent traces; does not execute an agent.

The caller owns the frozen case, the run record and an independently collected
observation. Synthetic fixtures exercise the oracle, not any model's quality.
"""
from collections import Counter
from math import isfinite

STATUSES = {"pass", "fail", "blocked", "timeout", "infrastructure_error", "grader_error", "not_run"}
ARMS = {"baseline", "current", "candidate", "synthetic"}
KINDS = {"positive", "negative", "chaos", "adversarial"}
SPLITS = {"development", "holdout"}
VERSION_KEYS = {"model", "agent", "skill", "prompt", "tool", "dataset", "evaluator"}
BUDGET_KEYS = {"max_tool_calls", "max_elapsed_ms", "max_cost"}
CASE_FIELDS = {"id", "kind", "requirement", "initial_state", "allowed_actions",
               "forbidden_actions", "required_actions", "expected_final", "expected_state",
               "max_actions", "budget", "dataset_version", "split"}


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _count(value):
    return type(value) is int and value >= 0


def _number(value):
    if type(value) not in (int, float) or value < 0:
        return False
    try:
        return isfinite(value)
    except OverflowError:
        return False


def _names(value):
    return isinstance(value, list) and all(_text(v) for v in value)


def _valid_case(case):
    if not isinstance(case, dict) or not CASE_FIELDS <= case.keys():
        return "case_contract_incomplete"
    if (not all(_text(case[k]) for k in ("id", "requirement", "dataset_version"))
            or not isinstance(case["kind"], str) or case["kind"] not in KINDS
            or not isinstance(case["split"], str) or case["split"] not in SPLITS
            or not _text(case["initial_state"]) or not _count(case["max_actions"])
            or not all(_names(case[k]) for k in
                       ("allowed_actions", "forbidden_actions", "required_actions"))):
        return "case_rules_invalid"
    if (not set(case["required_actions"]) <= set(case["allowed_actions"])
            or set(case["required_actions"]) & set(case["forbidden_actions"])):
        return "case_rules_invalid"
    limits = case.get("action_limits", {})
    if (not isinstance(limits, dict) or any(not _text(k) or not _count(v)
                                             for k, v in limits.items())):
        return "action_limits_invalid"
    budget = case["budget"]
    if (not isinstance(budget, dict) or budget.keys() - BUDGET_KEYS or
            any(not (_count(v) if k != "max_cost" else _number(v))
                for k, v in budget.items())):
        return "budget_invalid"
    rules = case.get("argument_rules", {})
    if not isinstance(rules, dict) or not set(rules) <= set(case["allowed_actions"]):
        return "argument_rules_invalid"
    for action, requirements in rules.items():
        if (not _text(action) or not isinstance(requirements, dict) or
                not requirements or any(not _text(k) or not isinstance(values, list)
                                        or not values or any(type(v) not in (str, int, float, bool)
                                                              for v in values)
                                        for k, values in requirements.items())):
            return "argument_rules_invalid"
    policy = case.get("effect_policy")
    if policy is not None:
        if (not isinstance(policy, dict) or set(policy) !=
                {"action", "baseline_effect_ids", "max_new_effects"} or
                not _text(policy["action"]) or
                not _names(policy["baseline_effect_ids"]) or
                len(set(policy["baseline_effect_ids"])) != len(policy["baseline_effect_ids"]) or
                not _count(policy["max_new_effects"])):
            return "effect_policy_invalid"
    return None


def _valid_run(case, run):
    if (run.get("case_id") != case["id"] or
            not isinstance(run.get("arm"), str) or run["arm"] not in ARMS or
            type(run.get("attempt")) is not int or run["attempt"] < 1):
        return "run_identity_invalid"
    versions = run.get("versions")
    if (not isinstance(versions, dict) or not VERSION_KEYS <= versions.keys() or
            not all(_text(versions[k]) for k in VERSION_KEYS) or
            versions["dataset"] != case["dataset_version"]):
        return "versions_invalid"
    evidence = run.get("evidence_refs")
    if not _names(evidence) or not evidence:
        return "evidence_missing"
    actions = run.get("actions")
    if not isinstance(actions, list):
        return "actions_invalid"
    for action in actions:
        if (not isinstance(action, dict) or not _text(action.get("name")) or
                ("args" in action and not isinstance(action["args"], dict)) or
                ("effect_id" in action and not _text(action["effect_id"]))):
            return "actions_invalid"
    usage = run.get("usage")
    if (not isinstance(usage, dict) or not _count(usage.get("tool_calls")) or
            usage["tool_calls"] != len(actions)):
        return "usage_missing_or_mismatch"
    for field in ("elapsed_ms", "cost"):
        value = usage.get(field)
        if value is not None and not _number(value):
            return "usage_invalid"
    for budget_key, usage_key in (("max_elapsed_ms", "elapsed_ms"), ("max_cost", "cost")):
        if budget_key in case["budget"] and not _number(usage.get(usage_key)):
            return "usage_unverifiable"
    if not isinstance(run.get("status"), str) or run["status"] not in STATUSES:
        return "unknown_status"
    return None


def _observed_effects(case, observed):
    """Compare external effect IDs against frozen baseline; never trust run claims."""
    policy = case.get("effect_policy")
    if policy is None:
        return None
    effects = observed.get("effects")
    if not isinstance(effects, list):
        return "effects_missing"
    matching = []
    for effect in effects:
        if not isinstance(effect, dict) or not _text(effect.get("action")) or not _text(effect.get("effect_id")):
            return "effects_invalid"
        if effect["action"] == policy["action"]:
            matching.append(effect["effect_id"])
    if len(set(matching)) != len(matching):
        return "duplicate_effect_id"
    before = set(policy["baseline_effect_ids"])
    after = set(matching)
    if not before <= after:
        return "existing_effect_missing"
    if len(after - before) > policy["max_new_effects"]:
        return "unexpected_new_effect"
    return None


def evaluate(case, run, *, observed=None):
    """Return (pass|fail|insufficient_evidence, reasons).

    observed must come from a separate evaluator-owned state/effects reader,
    not from the model's self-reported run.resulting_state. For synthetic tests,
    it comes from a separate reviewed fixture. No execution is performed here.
    """
    if not isinstance(case, dict) or not isinstance(run, dict):
        return "insufficient_evidence", ["record_not_object"]
    err = _valid_case(case)
    if err:
        return "insufficient_evidence", [err]
    err = _valid_run(case, run)
    if err:
        return "insufficient_evidence", [err]

    actions = run["actions"]
    names = [action["name"] for action in actions]
    counts = Counter(names)
    failures = []
    if any(name not in case["allowed_actions"] or name in case["forbidden_actions"] for name in names):
        failures.append("unauthorized_action")
    for action in actions:
        for arg, allowed in case.get("argument_rules", {}).get(action["name"], {}).items():
            value = action.get("args", {}).get(arg)
            if not any(type(value) is type(candidate) and value == candidate for candidate in allowed):
                if "argument_not_allowed" not in failures:
                    failures.append("argument_not_allowed")
    if any(counts[name] > cap for name, cap in case.get("action_limits", {}).items()):
        failures.append("action_limit_exceeded")
    if len(actions) > case["max_actions"]:
        failures.append("action_budget_exceeded")
    budget = case["budget"]
    if "max_tool_calls" in budget and len(actions) > budget["max_tool_calls"]:
        failures.append("tool_budget_exceeded")
    if "max_elapsed_ms" in budget and run["usage"]["elapsed_ms"] > budget["max_elapsed_ms"]:
        failures.append("elapsed_budget_exceeded")
    if "max_cost" in budget and run["usage"]["cost"] > budget["max_cost"]:
        failures.append("cost_budget_exceeded")
    # An independent ledger can prove a forbidden effect even after an interruption.
    effect_err = None
    if isinstance(observed, dict) and _text(observed.get("evidence_ref")):
        effect_err = _observed_effects(case, observed)
        if effect_err in ("unexpected_new_effect", "duplicate_effect_id", "existing_effect_missing"):
            failures.append(effect_err)
    if failures:
        return "fail", failures
    status = run["status"]
    if status != "pass":
        return ("fail" if status == "fail" else "insufficient_evidence"), ["run_status_" + status]

    # A completed run needs both reported outputs and independent state evidence.
    if "final" not in run or "resulting_state" not in run:
        return "insufficient_evidence", ["completed_output_missing"]
    if (not isinstance(observed, dict) or "state" not in observed or
            not _text(observed.get("evidence_ref"))):
        return "insufficient_evidence", ["observation_missing"]
    if effect_err is None:
        effect_err = _observed_effects(case, observed)
    if effect_err in ("effects_missing", "effects_invalid"):
        return "insufficient_evidence", [effect_err]

    if any(name not in counts for name in case["required_actions"]):
        failures.append("required_action_missing")
    if run["final"] != case["expected_final"]:
        failures.append("wrong_final")
    if observed["state"] != case["expected_state"]:
        failures.append("wrong_state")
    if run["resulting_state"] != observed["state"]:
        failures.append("reported_state_mismatch")
    if effect_err:
        failures.append(effect_err)
    return ("fail", failures) if failures else ("pass", [])
