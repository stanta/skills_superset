# Project Manager Templates

Use these templates as copy-ready structures. Keep unused optional fields as `unknown` rather than inventing data.

## Project context

```yaml
PROJECT_CONTEXT:
  project:
    name: ""
    state: INTAKE
    decision_owner: ""
    stakeholders: []
  problem:
    affected_user: ""
    situation: ""
    current_behavior_or_state: ""
    pain_and_impact: ""
    evidence: []
    root_cause_hypotheses: []
  outcome:
    product_goal: ""
    baseline:
      metric: ""
      value: unknown
      source: ""
    target:
      value: ""
      review_date: ""
    guardrails: []
    success_decision_rule: ""
    kill_or_pivot_criteria: []
  scope:
    in_scope: []
    out_of_scope: []
    non_goals: []
    constraints:
      deadline: ""
      budget: ""
      architecture: []
      security_privacy: []
      legal_compliance: []
  delivery:
    iteration_length: "1 week"
    current_iteration_goal: ""
    board_url: ""
    repository_urls: []
    documentation_urls: []
    definition_of_ready: []
    definition_of_done: []
    wip_limits: {}
  resources:
    people: []
    weekly_capacity_hours: unknown
    competencies_available: []
    competencies_missing: []
    tools_and_environments: []
    external_dependencies: []
  current_state:
    active_items: []
    blocked_items: []
    recent_evidence: []
    open_decisions: []
    risks: []
    last_updated_at: ""
  authorization:
    may_read: []
    may_write: []
    requires_approval: []
    prohibited: []
```

## Project charter

```yaml
problem: ""
evidence: []
brd_reference: ""
prd_reference: ""
outcome:
  baseline: null
  target: null
  review_date: ""
  source: ""
  guardrails: []
scope:
  in: []
  out: []
  non_goals: []
constraints: []
assumptions: []
decision_criteria:
  continue: []
  pivot: []
  stop: []
```

## Milestone card

```yaml
milestone: ""
observable_state: ""
evidence: ""
dependencies: []
primary_risk: ""
decision_enabled: ""
forecast_range: ""
owner: ""
```

## Work item

```yaml
id: PROJECT-123
title: "Verb + concrete outcome"
outcome: ""
purpose: "How this advances the Iteration Goal"
alignment: "BRD/PRD objective or requirement"
owner: "Name/role"
type: feature | defect | risk-reduction | spike | chore
inputs: []
dependencies: []
acceptance_criteria: []
evidence_required: []
estimate_range: "2-4h"
confidence: low | medium | high
risk_class: ""
risks: []
security_privacy: []
rollback_or_recovery: "if applicable"
status: READY
```

## Spike

```yaml
question: ""
decision_affected: ""
hypotheses: []
method: ""
timebox: ""
budget_cap: ""
expert_needed: ""
evidence: ""
decision_options: [adopt, reject, test_further, escalate]
```

## Daily plan

```markdown
## Start of day
1. Primary outcome for the day:
2. Active work item:
3. Completion criteria and evidence:
4. Most likely blocker and mitigation:
5. Escalation/replan condition:

## End of day
- Completed outcome:
- Evidence:
- Learning:
- Forecast change:
- First work item for next day:
- Unresolved blocker:
```

## Weekly PM decision report

```text
1. Outcome / Iteration Goal status
2. Completed evidence and decisions enabled
3. Flow: WIP, throughput, aging items, cycle-time trend
4. Quality and incidents
5. Blockers and decisions required, with owners and dates
6. Forecast range and changes in assumptions
7. Top risks and responses
8. Next coherent result
```

## Decision packet

```yaml
decision_required: ""
decision_owner: ""
deadline: ""
facts: []
unknowns: []
options:
  - option: ""
    time_range: ""
    resources: []
    risks: []
    exclusions: []
    consequences: []
recommendation: ""
consequences_of_inaction: ""
```

## Board policy

```yaml
workflow:
  - column: BACKLOG
    entry_policy: "Connected to the goal or has risk/learning value"
    exit_policy: "Ordered and selected for refinement"
  - column: READY
    entry_policy: "Meets Definition of Ready"
    exit_policy: "Capacity is available and an owner has started work"
  - column: IN_PROGRESS
    entry_policy: "WIP limit has not been exceeded"
    exit_policy: "A verifiable outcome has been produced"
  - column: REVIEW_VALIDATION
    entry_policy: "Evidence is attached"
    exit_policy: "Meets Definition of Done or is returned with a specific defect"
  - column: DONE
    entry_policy: "Meets Definition of Done"
    exit_policy: "Never silently reopened; a new deviation becomes a separate defect"
wip_policy:
  in_progress: "one primary item per executor unless explicitly approved"
  review_validation: "small explicit limit to avoid hidden review queues"
  blocked: "visible with reason, owner, and next check date; does not justify unlimited new work"
classes_of_service:
  expedite: "requires explicit urgency criterion, owner, and displacement cost"
```

## Project closure record

```yaml
closure_type: done | paused | killed | pivoted
reason: ""
final_evidence: []
decisions: []
reusable_assets: []
remaining_debts_or_obligations: []
follow_up_actions:
  - action: ""
    owner: ""
    due_date: ""
lessons_learned: []
artifact_disposition: []
```
