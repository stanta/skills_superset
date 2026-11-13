# LLM Evaluation Engineer: engineering playbook

## DSPy mechanism

**Example, Evaluate**. Verify actual imports, signatures and optimizer requirements against the installed DSPy release before writing production code.

## Implementation recipe

### Step 1

Define the target behavior, unit of evaluation and deterministic versus judged metrics.

### Step 2

Curate representative normal, difficult, adversarial and safety-critical cases; remove duplicates and near duplicates.

### Step 3

Split train, validation and sealed final test by related entity, session, user or time to prevent leakage.

### Step 4

Define hard safety constraints, quality metrics, slices, cost and latency; calibrate judges.

### Step 5

Run and archive a baseline with fixed model/version and inference settings.

### Step 6

Report per-slice scores, uncertainty, missing runs, and test-set access rules; provide a reproducible evaluation command.


## Examples and completion criteria

Example request: "Use llm-eval-engineer to improve one bounded AI component, with a frozen baseline, versioned examples and measured acceptance criteria."

- Required input: Frozen task contract and representative examples with provenance
- Required input: Defined failure costs, baseline, model configuration and evaluation budget

- Acceptance: Training examples and optimizer feedback never include held-out test examples.
- Acceptance: Judge outputs are audited, denominators and failed calls included; no cherry-picked slices.

Return **Evaluation contract, datasets, metrics, reproducible run configuration, baseline report.**

## Anti-patterns

- Optimizing on the final test set or treating generated examples as independently verified.
- Giving an optimizer or generated code permission to alter evaluator, policy, production resources or user approvals.
- Reporting only successful attempts while omitting failures, costs and uncertainty.
- Assuming DSPy changes the underlying foundation model weights.

## Fallback

When the library cannot be installed or API support is uncertain, supply the contract, test cases, decision criteria and runnable design rather than pretending the optimizer ran.
