# Model Cost Optimizer: engineering playbook

## DSPy mechanism

**LM, Evaluate, Optimizers**. Verify actual imports, signatures and optimizer requirements against the installed DSPy release before writing production code.

## Implementation recipe

### Step 1

Fix the evaluation metric, hard constraints and representative workload distribution.

### Step 2

Measure per-model accuracy slices, tokens, cache effects, retries and p95 latency.

### Step 3

Account for inference, judge calls, compilation, failed optimizations and ongoing monitoring.

### Step 4

Test static model choices before introducing conditional routing.

### Step 5

Evaluate routing and fallback on held-out samples including error and outage cases.

### Step 6

Choose a Pareto-appropriate configuration that meets hard floors; monitor cost drift.


## Examples and completion criteria

Example request: "Use model-cost-optimizer to improve one bounded AI component, with a frozen baseline, versioned examples and measured acceptance criteria."

- Required input: Representative datasets, model/version inventory and price assumptions
- Required input: Hard correctness, safety, p95 latency and budget thresholds

- Acceptance: No quality or safety floor is traded away to improve an average cost.
- Acceptance: Reported savings include all overhead, not just successful final-call tokens.

Return **Cost-quality-latency matrix, selected routing policy, assumptions and re-evaluation triggers.**

## Anti-patterns

- Optimizing on the final test set or treating generated examples as independently verified.
- Giving an optimizer or generated code permission to alter evaluator, policy, production resources or user approvals.
- Reporting only successful attempts while omitting failures, costs and uncertainty.
- Assuming DSPy changes the underlying foundation model weights.

## Fallback

When the library cannot be installed or API support is uncertain, supply the contract, test cases, decision criteria and runnable design rather than pretending the optimizer ran.
