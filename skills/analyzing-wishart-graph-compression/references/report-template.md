# Report template: Wishart graph-compression analysis

## Contents
- Experiment identity and integrity
- Compression trajectory
- Scalar parameter changes
- Strong preservation diagnostics
- Threshold and diffusion analysis
- Traffic and relation-aware analysis
- Wishart modes
- Cross-metric and seed comparison
- Null baselines
- Scale plateau
- Semantic inspection
- Falsification and sources
- Final conclusion format


## Executive summary

State:
- input graph;
- metrics compared;
- seed count;
- compression range;
- strongest preserved quantities;
- first quantities to break;
- whether a scale plateau is supported;
- whether Wishart beats matched baselines.

Do not state conclusions before integrity/comparability checks.

---

## 1. Experiment identity

Table:

| field | value |
|---|---|
| git commit | |
| config hash | |
| input graph hash | |
| ConceptNet slice | |
| aggregation | |
| metric | |
| seed(s) | |
| candidate radius | |
| k_neighbors | |
| significance | |
| candidate_limit | |

---

## 2. Integrity and comparability

Report:
- COMPLETED present;
- hierarchy level count;
- mapping consistency;
- baseline hashes equal across metrics;
- configuration differences;
- missing/corrupt artifacts.

Verdict:
- comparable;
- comparable with caveats;
- not directly comparable.

---

## 3. Compression trajectory

Table:

| metric | seed | level | N | nnz | compression fraction | compression ratio | figure occurrences | Wishart clusters | noise fraction |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|

Discuss:
- reduction speed;
- no-reduction stops;
- whether few figure types dominate compression.

---

## 4. Scalar parameter changes

For each:
- mean degree;
- second moment degree;
- spreading proxy;
- percolation proxy;
- spectral gap;
- MFPT + hit rate;
- synchronizability;
- max betweenness;
- congestion threshold;
- clustering;
- mean/median/p95 distance.

Table:

| Q | Q0 | final | max baseline distortion | largest step jump | qualitative trend |
|---|---:|---:|---:|---:|---|

Explain mechanisms, not just values.

---

## 5. Strong preservation diagnostics

### Stationary mass

Report per-transition:
- L1;
- TV.

### Slow eigenvalues

Report:
- relative L2 error;
- max absolute error.

### Slow eigenspace

Report:
- principal angles;
- projection distance.

Identify the first compression point where each becomes materially distorted.

---

## 6. Threshold mechanism analysis

Show together:
- (langle kangle);
- (langle k^2angle);
- (kappa=langle k^2angle/langle kangle);
- spreading proxy;
- percolation proxy.

Explain threshold movement through degree heterogeneity.

---

## 7. Diffusion analysis

Show:
- stationary mass error;
- spectral gap;
- MFPT;
- hit rate;
- slow eigenspace.

Ask whether all tell a consistent story.

If MFPT disagrees while hit rate changes strongly, treat MFPT as censored/noisy.

---

## 8. Traffic analysis

Show:
- max betweenness;
- congestion threshold;
- path distances.

Identify artificial macro-hubs introduced by compression.

For suspicious supernodes, inspect:
- concept_concat;
- figure_type;
- external flow.

---

## 9. Relation-aware semantic flow

For every relation:
- total weight;
- self-loop/internalized weight;
- off-diagonal weight;
- internalization fraction.

Heatmap:
- rows = relations;
- columns = levels/compression.

Interpret which relations become internal earliest.

Do semantic interpretation only after topology-only analysis is complete.

---

## 10. Wishart modes

Table per figure_type:

| type | occurrences | median nodes | nodes removed | median kth radius | median leakage | dominant relations |
|---|---:|---:|---:|---:|---:|---|

Discuss:
- dense recurring types;
- rare types;
- high-compression/high-distortion types;
- high-compression/low-distortion types.

---

## 11. Cross-metric comparison

Always use matched compression.

Table:

| target compression | metric | stationary TV | eigenspace dist | spectral-gap dist | MFPT dist | threshold dist |
|---:|---|---:|---:|---:|---:|---:|

Add Pareto plots.

Do not produce one global winner unless the user's objective specifies weights.

---

## 12. Seed robustness

For each primary observable:
- median curve;
- IQR;
- 95% CI if enough repeats.

Report:
- stable signs/trends;
- unstable transitions;
- seed-sensitive figure types.

---

## 13. Null/baseline comparison

Compare Wishart to:
- random matched contraction;
- degree-matched;
- Haken if available.

Table:

| compression | method | primary distortion | delta vs random |
|---:|---|---:|---:|

A positive research result requires more than “Wishart compresses”: it should preserve chosen observables better than plausible controls.

---

## 14. Scale plateau

Report:
- operational tolerances;
- plateau start/end;
- limiting observable;
- reproducibility across seeds;
- method dependence.

If none exists, say so explicitly.

---

## 15. Semantic inspection of merged concepts

Use `concept_concat` only after structural analysis.

For selected figure types:
- inspect 20-100 representative occurrences;
- detect semantic coherence/heterogeneity;
- summarize common ConceptNet relation patterns;
- separate topology-driven grouping from lexical similarity.

Do not use post-hoc semantic coherence to rewrite the original clustering criterion.

---

## 16. Falsification section

Explicitly answer:

- Does stationary mass fail unexpectedly?
- Does slow eigenspace collapse early?
- Is Wishart no better than random matched contraction?
- Are results metric-specific?
- Are results seed-specific?
- Are apparent gains driven by MFPT censoring?
- Do relation layers collapse into self-loops too quickly?
- Is there no plateau?

---

## 17. Sources and short quotes

Include at least:
- Wishart 1969;
- Gfeller & De Los Rios 2007;
- Barrat et al. 2008;
- the paper corresponding to the chosen similarity metric.

Use short direct quotes only, then interpret in your own words.

---

## 18. Final conclusion format

End with four separate statements:

### Compression
How much structural reduction was achieved?

### Preservation
Which observables remain stable over what compression range?

### Mechanism
Which figure types / relation flows explain the main changes?

### Robustness
Do conclusions survive seeds, metrics and null baselines?

Never merge these into one vague “method works/doesn't work” verdict.
