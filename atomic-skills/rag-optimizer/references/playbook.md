# RAG experiment matrix

## Separate the failure sources

If the document is absent, repair authorized ingestion/coverage before tuning generation. If the document exists but is not retrieved, inspect query, filters, index and ranking. If correct passages are present but the answer is wrong, inspect context packing and answer generation. An oracle-context test can help separate these causes, but must be labeled diagnostic rather than production performance.

Record question IDs, expected evidence IDs, retrieved IDs/ranks, corpus/index version, answer claims and cited passage IDs. Use a frozen evidence set for comparisons. Retrieval precision can fall while answer quality rises; evaluate both against the actual product objective.

## Optional DSPy composition

Represent query formulation and grounded answer generation as separate signatures/modules, with the actual retriever supplied by the application. DSPy does not by itself supply the corpus, access-control policy or universal retriever. GEPA/MIPROv2 may optimize model-facing instructions against the selected metric; evaluating a module does not automatically optimize index parameters.

A proposed experiment should state hypothesis, one changed variable, fixed dependencies, budget, validation criterion and rollback configuration. Include no-answer questions, contradictory document revisions, invalid source IDs and tenant-boundary probes. Check citation entailment, not just the presence of a URL.

## Primary sources

Checked 2026-11-13. Original experiment procedure informed by DSPy's modular composition and optimization interfaces:

- https://dspy.ai/current/tutorials/rag/
- https://dspy.ai/current/diving-deeper/gepa-in-depth/

Recheck available APIs before coding; no retriever service or private corpus access is implied by this skill.
