# Evaluation and experimental protocol

## 1. Primary questions

Evaluate grammar-based compression along separate axes:

1. **Fidelity:** exact reconstruction or quantified loss.
2. **Compression:** actual bits/bytes, not only fewer nodes.
3. **Construction cost:** wall time, CPU/GPU time, peak RAM, disk I/O.
4. **Queryability:** latency and throughput for the intended compressed queries.
5. **Structural discovery:** stability and reuse of learned symbols.
6. **Scalability:** behavior as \(|V|, |E|\), label vocabulary, motif size and rank grow.

Do not collapse these into one score unless weights are fixed before seeing results.

## 2. Lossless verification

For exact mode:

1. fully decode the grammar;
2. verify node/edge/relation counts;
3. verify labels, direction, multiplicity, self-loops and weights covered by the contract;
4. canonicalize both original and decoded graph or use a robust exact-equivalence test;
5. verify original-to-expanded membership/bindings if exposed by the API.

\`decode(encode(G))\` must equal \(G\) under the declared graph semantics.

A graph can have different node IDs after derivation and still be isomorphic; do not use raw adjacency-file bytes as the only equivalence test.

## 3. Compression metrics

Report at least:

\[
R_{\mathrm{bits}}=
\frac{L_{\mathrm{compressed}}}
{L_{\mathrm{baseline}}}
\]

and its inverse if desired.

Break down:

~~~text
start graph
grammar rules
nonterminal references
port bindings
residual/correction stream
label dictionaries
query indexes
container/metadata overhead
~~~

Also report bits per original edge (bpe) or bytes per edge when meaningful.

Never call \(1-N_{\mathrm{coarse}}/N_{\mathrm{original}}\) the storage compression ratio.

## 4. Baselines

Select baselines by goal and graph type.

### Universal storage baselines

- raw or canonical edge list + a general compressor such as zstd/gzip;
- CSR/CSC plus integer compression where appropriate.

### Graph-specific compact representations

For web/RDF/hypergraph workloads, include a maintained succinct/domain compressor if available.

### Structural/MDL baselines

- VoG-like MDL summary;
- supernode + corrections methods;
- exact motif dictionary without approximate family clustering.

### Grammar baselines

- gRePair/SL-HR;
- ITR when label/triple/neighborhood queries matter.

A new Wishart/embedding-assisted grammar should beat a simpler exact dictionary at equal fidelity before attributing value to the approximate discovery layer.

## 5. Synthetic test suite

### A. Repeated exact motifs

Generate a graph from known motifs with controlled frequency, overlap and interface rank.

Tests:
- symbol recovery;
- gain estimate vs true encoded size;
- exact round-trip;
- overlap selection quality.

### B. Hierarchical grammar

Generate:

\[
A\to(B,C,C),\quad
B\to(D,E),\quad
C\to(D,D,F).
\]

Expand to a large graph. Hide the grammar and test whether the compressor recovers reusable rules and a similar derivation hierarchy.

Do not require identical nonterminal names/order: compare canonical rule structures and achieved code length.

### C. Approximate families

Perturb a prototype with controlled edge/relation edits.

Vary edit probability and measure when:

\[
L(\text{family}+\text{residuals})
<
L(\text{separate exact rules}).
\]

This gives a principled cutoff for approximate clustering.

### D. High-rank stress

Hold internal repetition constant while increasing external ports. Verify that code length eventually penalizes otherwise frequent motifs.

### E. Overlap adversary

Construct many high-frequency overlapping occurrences where greedy selection is suboptimal. Measure the gap between simple greedy and a stronger local-improvement or exact solution on small instances.

### F. Labels and directions

Use isomorphic topology with different relation labels/directions. An exact semantic-graph compressor must keep them distinct unless they are explicitly residualized.

## 6. Order and seed sensitivity

gRePair-style greedy occurrence counting can depend on node order. Approximate motif sampling and density clustering add randomness.

Use multiple:

- deterministic orderings (ID, degree, BFS/DFS, canonical);
- random order seeds;
- candidate sampling seeds.

Report median, range/IQR and best/worst compression only with the ordering policy clearly identified. Never report only the lucky seed.

## 7. Dictionary quality

For each symbol:

~~~text
occurrence count
selected non-overlapping count
raw frequency
rank / port count
expanded nodes/edges
rule cost
reference cost
residual cost
net gain
first-seen level
reuse depth
~~~

Global metrics:

- dictionary size;
- percentage of rules with positive net gain;
- coverage of original edges;
- mean/median reuse depth;
- novelty rate by recursion level;
- fraction of compressed bits spent on residuals/interfaces.

A useful hierarchy should generally show reuse, not merely continuous creation of one-off rules.

## 8. MDL validity

Use one coherent code to compare candidate models. The two-part score must include every component needed for reconstruction.

For approximate matching, edit/distortion costs should correspond to an actual code or probabilistic model; arbitrary similarity thresholds are discovery hyperparameters, not MDL evidence.

The MDL pattern-mining literature specifically warns that SUBDUE-style approximate matching is not automatically a proper reconstruction-error code.

## 9. Query benchmark

Choose a fixed query set before tuning.

Examples:

- \`neighbors(v)\`;
- \`(subject, predicate, ?object)\` triple queries;
- reachability;
- regular path queries.

Report:

~~~text
compressed size with query indexes
p50 / p95 / p99 latency
throughput
cold/warm cache
decompression avoided? yes/no
~~~

Compare both compressed and uncompressed reference implementations.

## 10. Semantic / knowledge graph experiment

For ConceptNet/SemMap-style graphs:

- terminals: relation type + direction;
- optional terminal/node typing: language, POS, concept class;
- symbol identity: internal typed topology + ranked interface;
- occurrence metadata: original concept IDs;
- residuals: relation/interface exceptions.

Recommended ablation:

~~~text
exact canonical grammar
typed-WL proposal + exact verification
Wishart proposal + exact verification
Wishart approximate family + residuals
~~~

Keep the same coding backend and graph split.

Primary endpoint: total bits at exact reconstruction.

Secondary endpoints:
- query latency;
- dictionary reuse/stability;
- relation-specific interface statistics;
- preservation of chosen dynamics if a lossy mode is intentionally tested.

## 11. Discovery claims need controls

A recurring grammar is not automatically a "natural semantic grammar."

For a discovery claim, test:

- repeated graph samples/subsets;
- multiple seeds/orderings;
- degree/relation-preserving null graphs;
- label-shuffle controls;
- stability of canonical symbols across runs;
- gain over matched random contractions/dictionaries.

Use language such as "reusable compression symbols under this representation" before stronger semantic interpretation.

## 12. Stopping rules

Stop recursive replacement when one of these holds:

- no candidate has positive estimated gain;
- actual encoded size no longer decreases;
- only one-use rules remain after pruning;
- rank/interface costs dominate;
- fidelity/query constraints fail;
- resource limit reached.

For research, log all rejected top candidates and why they failed; rejection statistics reveal whether the bottleneck is frequency, interface rank, overlap, or residual cost.
