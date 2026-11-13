# RAG Optimizer: engineering playbook

## DSPy mechanism

**Module composition, Evaluate, GEPA**. Verify actual imports, signatures and optimizer requirements against the installed DSPy release before writing production code.

## Implementation recipe

### Step 1

Baseline end-to-end RAG quality, retrieval recall, faithfulness and latency separately.

### Step 2

Audit corpus provenance, chunking, index version and access-control filters.

### Step 3

Optimize retrieval parameters and query transformation without weakening authorization filters.

### Step 4

Optimize answer instructions or demonstrations only after establishing adequate retrieval.

### Step 5

Test unsupported queries, stale passages, contradictory sources and prompt injections.

### Step 6

Verify citation-to-claim alignment and compare held-out slices plus total cost.


## Examples and completion criteria

Example request: "Use rag-optimizer to improve one bounded AI component, with a frozen baseline, versioned examples and measured acceptance criteria."

- Required input: Versioned corpus/index, labeled queries and ground-truth source spans
- Required input: Retriever settings, answer policy and accepted freshness/quality thresholds

- Acceptance: Unauthorized documents are never surfaced regardless of retrieval score.
- Acceptance: Improved answer score is not allowed to mask falling retrieval recall or faithfulness.

Return **Versioned retriever/generator configs, grounded answer report and regression comparison.**

## Anti-patterns

- Optimizing on the final test set or treating generated examples as independently verified.
- Giving an optimizer or generated code permission to alter evaluator, policy, production resources or user approvals.
- Reporting only successful attempts while omitting failures, costs and uncertainty.
- Assuming DSPy changes the underlying foundation model weights.

## Fallback

When the library cannot be installed or API support is uncertain, supply the contract, test cases, decision criteria and runnable design rather than pretending the optimizer ran.
