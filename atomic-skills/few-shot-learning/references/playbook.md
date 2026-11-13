# Few-Shot Learning: engineering playbook

## DSPy mechanism

**LabeledFewShot, BootstrapFewShot**. Verify actual imports, signatures and optimizer requirements against the installed DSPy release before writing production code.

## Implementation recipe

### Step 1

Choose a no-example baseline and evaluation metric.

### Step 2

Curate diverse labeled demonstrations, remove duplicates and prohibited personal information.

### Step 3

Try a small labeled few-shot candidate before bootstrapping outputs with a teacher.

### Step 4

Reject bootstrapped examples failing schema, metric or provenance checks.

### Step 5

Measure different shot counts and class/error slices on validation.

### Step 6

Freeze selection, run held-out evaluation and document the full demonstration lineage.


## Examples and completion criteria

Example request: "Use few-shot-learning to improve one bounded AI component, with a frozen baseline, versioned examples and measured acceptance criteria."

- Required input: Task Signature and curated examples with verified expected outputs
- Required input: Model and token budget, data-use permissions and validation split

- Acceptance: Demonstrations are traceable, representative and limited to approved data.
- Acceptance: Any bootstrapped label is verified; test examples are never candidates.

Return **Validated few-shot set, shot-selection rule and comparison to zero-shot baseline.**

## Anti-patterns

- Optimizing on the final test set or treating generated examples as independently verified.
- Giving an optimizer or generated code permission to alter evaluator, policy, production resources or user approvals.
- Reporting only successful attempts while omitting failures, costs and uncertainty.
- Assuming DSPy changes the underlying foundation model weights.

## Fallback

When the library cannot be installed or API support is uncertain, supply the contract, test cases, decision criteria and runnable design rather than pretending the optimizer ran.
