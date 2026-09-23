# Metrics and formulas for Wishart graph-compression analysis

## Contents
- Compression coordinates
- Scalar change metrics
- Stationary mass
- Slow eigenvalues and eigenspace
- Spectral gap and MFPT
- Degree moments and threshold proxies
- Synchronizability, betweenness and congestion
- Clustering and path lengths
- Relation-flow conservation and internalization
- External flow and exit distributions
- Wishart mode diagnostics
- Composite distortion
- Matched-compression comparison


## 1. Compression coordinates

For level (s):

[
c_s = 1 - rac{N_s}{N_0}
]

is cumulative compression fraction.

[
R_s = rac{N_0}{N_s}
]

is compression ratio.

Use (c_s) as the primary x-axis for cross-method comparison.

---

## 2. Scalar change metrics

For scalar observable (Q):

### Adjacent-step change

[
Delta_s(Q)=
rac{Q_{s+1}-Q_s}{|Q_s|+epsilon}
]

Use to locate abrupt transitions.

### Baseline distortion

[
D_s(Q)=
rac{|Q_s-Q_0|}{|Q_0|+epsilon}
]

Use to evaluate preservation from the original graph.

### Signed baseline drift

[
B_s(Q)=
rac{Q_s-Q_0}{|Q_0|+epsilon}
]

Use when direction matters.

### Log elasticity

[
E_s(Q)=
rac{Delta log Q}{Delta log N}
]

Use only for positive, sufficiently stable quantities.

---

## 3. Stationary mass

Let (P_sin{0,1}^{N_s	imes N_{s+1}}) be the fine-to-coarse membership matrix.

Expected coarse mass:

[
widehat{pi}_{s+1}=P_s^Tpi_s.
]

Errors:

[
E_pi^{L1}
=
|widehat{pi}_{s+1}-pi_{s+1}|_1,
]

[
E_pi^{TV}
=
rac12E_pi^{L1}.
]

For undirected nonnegative sum-aggregation, this is also an implementation consistency test.

---

## 4. Slow eigenvalues

After removing the Perron/trivial mode and matching the first (r) available nontrivial values:

[
E_lambda^{rel}
=
rac{
|lambda_s^{(1:r)}-lambda_{s+1}^{(1:r)}|_2
}{
|lambda_s^{(1:r)}|_2+epsilon
}.
]

Also report max absolute error:

[
E_lambda^{max}
=
max_i|lambda_{s,i}-lambda_{s+1,i}|.
]

Do not compare unequal spectrum lengths without explicitly recording truncation.

---

## 5. Slow eigenspace

Let (U_sinmathbb R^{N_s	imes r}).

Lift the coarse basis:

[
widetilde U_{s+1}=P_s U_{s+1}.
]

Orthonormalize both bases in the chosen inner product.

Compute singular values:

[
sigma_i =
sigma_i(U_s^Twidetilde U_{s+1}).
]

Principal angles:

[
	heta_i=arccos(mathrm{clip}(sigma_i,-1,1)).
]

Useful summary:

[
d_{proj}=
rac{
|U_sU_s^T-widetilde U_{s+1}widetilde U_{s+1}^T|_F
}{
sqrt{2r}
}.
]

This is invariant to sign flips and rotations inside the subspace.

---

## 6. Spectral gap

Current semmap-wishart implementation uses leading eigenvalues of normalized adjacency (S=D^{-1/2}AD^{-1/2}):

[
g_s = lambda_1(S_s)-lambda_2(S_s).
]

For a connected undirected graph, (lambda_1approx1), so this resembles (1-lambda_2).

Do not confuse it with Laplacian algebraic connectivity.

---

## 7. MFPT

Artifacts contain:
- `mfpt_mean`;
- `mfpt_hit_rate`.

The mean is computed only over successful hits before `mfpt_max_steps`.

Therefore pair:

[
M_s=(MFPT_s,h_s)
]

must be interpreted jointly.

A simple reliability flag:

[
R_s^{MFPT}=1-h_s.
]

Large changes in hit rate invalidate naive MFPT comparisons.

If raw trajectory times are available later, prefer survival-analysis / restricted-mean estimates.

---

## 8. Degree statistics

Topological degree:

[
k_i = |{j:A_{ij}
e0}|.
]

Mean:

[
langle kangle=
rac1Nsum_i k_i.
]

Second moment:

[
langle k^2angle=
rac1Nsum_i k_i^2.
]

Heterogeneity ratio:

[
kappa=
rac{langle k^2angle}{langle kangle}.
]

Track (kappa) because many network-process thresholds depend on degree heterogeneity.

---

## 9. Spreading-threshold proxy

Current implementation:

[
T_{spread}=
rac{langle kangle}{langle k^2angle}.
]

Interpret as a heterogeneous-mean-field style proxy.

Barrat et al. note for SIS that a threshold of this form arises under specific assumptions; it is not a universal ConceptNet threshold.

---

## 10. Percolation-threshold proxy

Current implementation:

[
T_{perc}=
rac{langle kangle}
{langle k^2angle-langle kangle}.
]

This is tied to locally tree-like uncorrelated configuration-model reasoning.

Treat it as a structural robustness proxy.

---

## 11. Synchronizability proxy

Current implementation computes unnormalized Laplacian:

[
L=D-A
]

and

[
S_{sync}=
rac{lambda_{max}(L)}{lambda_2(L)}.
]

Smaller ratio is usually interpreted as easier synchronization in standard master-stability settings.

Preconditions:
- connected graph;
- undirected/symmetric coupling;
- compatible oscillator/coupling model if making a physical claim.

If (lambda_2) is near zero, report disconnected/nearly disconnected status instead of using a huge ratio as ordinary data.

---

## 12. Betweenness and congestion

Let (b_i) be unnormalized shortest-path betweenness.

[
b^*=max_i b_i.
]

Current congestion proxy:

[
R_c=
rac{N-1}{b^*}.
]

Report (N), (b^*), (R_c) together.

If betweenness is sampled, repeat with multiple seeds.

---

## 13. Clustering

Current artifact `macro_clustering` is a sample mean of unweighted local clustering.

It does not preserve:
- relation types;
- ConceptNet weights;
- exact all-node average when sampling is active.

Treat as descriptive topology.

---

## 14. Path-length summaries

Current artifacts:
- mean;
- median;
- p95 sampled reachable shortest-path lengths.

Recommended additions when recomputing:
- diameter or effective diameter;
- global efficiency;
- disconnected-pair fraction.

Global efficiency:

[
E_G=
rac1{N(N-1)}
sum_{i
e j}rac1{d(i,j)}
]

with (1/infty=0).

---

## 15. Relation-flow conservation

For relation layer (A^{(r)}_s):

[
W_r(s)=sum_{ij}A^{(r)}_{s,ij}.
]

For sum aggregation:

[
E_r^{mass}=
rac{|W_r(s+1)-W_r(s)|}
{|W_r(s)|+epsilon}.
]

This should be near numerical zero unless data/aggregation semantics changed.

---

## 16. Relation internalization

Self-loop mass:

[
L_r(s)=operatorname{tr}A^{(r)}_s.
]

Off-diagonal mass:

[
O_r(s)=W_r(s)-L_r(s).
]

Internalization fraction:

[
I_r(s)=rac{L_r(s)}{W_r(s)+epsilon}.
]

Interpretation:
- rising (I_r): relation (r) is increasingly absorbed inside supernodes;
- stable low (I_r): relation stays predominantly inter-block.

---

## 17. External flow and leakage

For block (C):

[
F_{out}(C)=
sum_{iin C,j
otin C}w_{ij}.
]

Let (F_{internal}(C)) be internal edge weight under the chosen convention.

Leakage:

[
ell(C)=
rac{F_{out}(C)}
{F_{out}(C)+F_{internal}(C)+epsilon}.
]

Analyze leakage by figure_type.

---

## 18. Exit-distribution comparison

If fine block exit distribution (p_C) and coarse transition distribution (q_C) are both available, compare with:

### Total variation

[
TV(p,q)=rac12sum_j|p_j-q_j|.
]

### Jensen-Shannon distance

[
d_{JS}(p,q)=sqrt{JS(p,q)}.
]

Use relation-conditioned variants if relation-specific transitions are available.

---

## 19. Wishart mode diagnostics

From `wishart.json` and `candidate_labels.npz`:

Noise fraction:

[
f_{noise}=
rac{#{i:label_i<0}}{N_{candidates}}.
]

Accepted-occurrence fraction:

[
f_{acc}=
rac{N_{accepted}}{N_{candidates}}.
]

Compression contribution of figure type (t):

[
C_t=
sum_{oin t}(|V(o)|-1).
]

Normalize:

[
p_t=rac{C_t}{sum_u C_u}.
]

A highly concentrated (p_t) means most compression comes from few figure families.

---

## 20. Composite distortion

Only after reporting individual metrics.

For tolerances (t_j) and weights (w_j):

[
D_{dyn}=
rac{sum_jw_jD_j/t_j}{sum_jw_j}.
]

Worst-case:

[
D_{max}=max_jD_j/t_j.
]

Also report the unaggregated vector ((D_1,ldots,D_m)).

---

## 21. Matched-compression comparison

For method (m), observe points:

[
(c_{m,s},D_{m,s}).
]

To compare methods at target compression (c^*):
- prefer an observed point close to (c^*);
- otherwise interpolate only between adjacent observed compression levels;
- never extrapolate beyond the method's achieved range without explicit caveat.

A method Pareto-dominates another at a point if it achieves:
- at least as much compression;
- no larger distortion;
- and strictly improves one of the two.
