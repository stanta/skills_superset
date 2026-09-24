# Statistical validation for recursive Wishart compression

## Contents
- Repeated-run and seed protocol
- Matched-compression comparison
- Robust summaries and paired design
- Hyperparameter sensitivity
- Null models and Haken baseline
- Permutation tests
- Scale plateau and change points
- Figure-type attribution
- Metric robustness
- Bootstrap and Monte Carlo error
- Recommended experimental matrix
- Decision language


## 1. Why repeated runs are required

A single recursive Wishart run mixes deterministic structure with several stochastic components:

- candidate-center subsampling;
- graphlet presampling;
- MFPT Monte Carlo;
- sampled betweenness;
- sampled clustering;
- sampled inter-node distances;
- approximate transport computations.

Therefore one run is exploratory evidence.

---

## 2. Seed protocol

For every metric, run a common seed set, e.g.:

```text
1729, 1730, 1731, 1732, 1733
```

Prefer 10+ repeats for publication-level uncertainty if compute budget allows.

Keep all non-seed configuration identical.

Store:
- metric;
- seed;
- git commit;
- config hash;
- input graph hash.

---

## 3. Compare runs at matched compression

Different seeds and metrics can produce different numbers of levels.

Create a common compression grid inside the shared observed range, e.g.:

[
c^*in{0.10,0.20,ldots}.
]

Interpolate each observable against (c), not against level number.

Do not extrapolate beyond observed compression.

---

## 4. Summaries across seeds

At each (c^*), report:
- median;
- Q1/Q3;
- 95% bootstrap CI if enough repeats;
- min/max for diagnostic transparency.

Prefer robust summaries because a rare clustering transition can create large outliers.

---

## 5. Paired design

When comparing metric A and B:
- use the same input graph;
- use the same seed set;
- use the same target compression grid.

Then compute paired differences:

[
delta_i =
D_i^{A}-D_i^{B}.
]

Report:
- median paired difference;
- bootstrap CI;
- optionally Wilcoxon signed-rank if sample size is adequate.

Do not overinterpret p-values with 3-5 seeds.

---

## 6. Multiple observables

Do not cherry-pick one parameter.

Pre-register a primary preservation set, for example:
- stationary-mass TV;
- slow-eigenspace distance;
- slow-eigenvalue error;
- spectral-gap distortion;
- MFPT distortion with hit-rate reliability.

Secondary:
- thresholds;
- congestion;
- clustering;
- path length.

State the set before inspecting the winner.

---

## 7. Wishart hyperparameter sensitivity

At minimum vary:

### k_neighbors
Controls density scale.

### significance
Controls how strongly modes must be separated by density saddles.

### radius
Changes the definition of a candidate local figure.

### candidate_limit
Controls sampling of the graph.

### graphlet_samples
For graphlet metric.

### transport_rank
For lowrank_gw / fgw approximations.

Use one-factor-at-a-time for diagnosis, then a small factorial/grid around the stable region.

A conclusion is stronger if it persists across a reasonable hyperparameter neighborhood.

---

## 8. Null model A: random matched contraction

Construct random disjoint groups with:
- same number of contracted figures per level;
- same empirical group-size distribution.

Then compare dynamic distortion at matched (N_{s+1}).

Question:

> Does Wishart preserve dynamics better than arbitrary contraction of the same strength?

This is the minimum null.

---

## 9. Null model B: degree-matched contraction

Build random groups matched approximately on degree or strength.

This tests whether Wishart's advantage is merely due to degree similarity.

---

## 10. Null model C: relation shuffle

Preserve topology but permute relation labels among edges, ideally within broad degree/weight strata.

Then rerun relation-aware metrics.

Question:

> Are discovered compression figures dependent on meaningful relation structure?

---

## 11. Baseline: Haken coarsening

The semgraphex project already contains a slow-mode/Haken-inspired coarsening branch.

Compare Wishart and Haken at matched compression using the same dynamic observables.

Interpretation:
- Wishart better: local structural modes preserve dynamics efficiently;
- Haken better: explicitly dynamical coordinates matter more;
- similar: possible overlap between structural and slow-mode organization.

---

## 12. Permutation test for baseline superiority

At target compression (c^*), let

[
Delta_i =
D_i^{Wishart}-D_i^{null}.
]

If repeated runs are paired, randomly flip signs of (Delta_i) to form a permutation null for the mean/median difference.

Use effect size and CI as primary evidence, p-value as secondary.

---

## 13. Detecting a scale plateau

Choose primary observables (Q_j) and tolerances (t_j) before inspecting plateaus.

Define level (s) acceptable if:

[
D_s(Q_j)le t_j
]

for every required (j).

A plateau is a contiguous range of compression values where:
- required metrics remain acceptable;
- compression continues to increase;
- seed uncertainty does not cross unacceptable regions excessively.

Report:
- plateau start/end compression;
- number of levels;
- uncertainty across seeds;
- which observable terminates the plateau.

---

## 14. Change-point analysis

Large one-step jumps can indicate structural phase transitions.

For each (Q), inspect:

[
|Delta_s(Q)|.
]

Candidate change point:
- unusually large jump relative to previous steps;
- coincides with large contraction of one/few figure types;
- repeats across seeds.

Do not call a phase transition from one noisy jump alone.

---

## 15. Figure-type attribution

For every transition, regress or correlate distortion increment against:
- number of occurrences by type;
- nodes removed by type;
- median figure size;
- mean leakage;
- relation composition.

Example target:

[
y_s=D_{s+1}(Q)-D_s(Q).
]

This identifies which compression figures are associated with dynamic damage.

With few levels, keep this descriptive rather than fitting complex models.

---

## 16. Metric robustness

A structural conclusion is robust if:
- direction of change is the same across several similarity metrics;
- plateau region overlaps;
- the same relation types internalize early/late;
- the same figure families dominate compression after post-hoc canonicalization.

Disagreement across metrics is itself a result: the notion of “same figure” is representation-dependent.

---

## 17. Bootstrap units

Choose bootstrap unit based on the question:

### Whole-run bootstrap
For variability across seeds.

### Figure-occurrence bootstrap
For distributions of leakage, size, external flow.

### Node/bootstrap within one graph
Usually inappropriate because graph nodes are dependent.

Do not pretend node-level observations are iid.

---

## 18. Monte Carlo error

MFPT, betweenness, clustering, and distance sampling need an estimation-stability check.

Repeat diagnostics on the *same fixed graph* with several diagnostic seeds.

This separates:
- coarsening variability;
- measurement variability.

If diagnostic noise is comparable to between-level change, the observable is not resolved.

---

## 19. Recommended experimental matrix

For initial publication-quality study:

```text
5 similarity metrics
x 5-10 seeds
x 2-3 Wishart parameter settings around baseline
+ random matched null
+ degree-matched null
+ Haken baseline
```

For expensive GW/FGW, use fewer candidate nodes but retain matched graph slices.

---

## 20. Decision language

Use:

- “stable within measured uncertainty”;
- “approximately preserved under the tested compression range”;
- “systematically drifts with compression”;
- “sensitive to similarity metric”;
- “not distinguishable from matched random contraction”.

Avoid:

- “invariant” after one run;
- “universally preserved”;
- “proves semantic self-similarity”;
- “proves multifractality”.
