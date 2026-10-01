# SemMap implementation findings for recursive lossless graph dictionaries

These findings come from implementing and testing the decoder-first grammar_exact_v2 / recursive Wishart pipeline in SemanticMap/semgraphex.

## 1. Verify reversibility before contraction

A coarse matrix such as

\[
A_{s+1}=P^\top A_sP
\]

is an analysis view, not a lossless encoding of \(A_s\). Emit the exact
transition representation before contraction and round-trip it immediately.

For multi-level compression, require the stronger chain:

\[
G_L \rightarrow G_{L-1}\rightarrow\cdots\rightarrow G_0.
\]

Do not publish a completion marker until the consolidated final-to-level-0
decode succeeds.

## 2. Separate internal shape from interface identity

Boundary-sensitive exact types are useful for matching, but storing a full
prototype per boundary pattern duplicates internal topology.

Use at least three identities:

- shape_id: exact internal typed/directed topology;
- interface_variant_id: canonical external port pattern;
- type_id: full exact matching identity.

One internal shape may have many interface variants.

## 3. Port bindings are part of the exact code

When a figure is replaced by one macro node, a coarse external edge does not
identify which internal node it originally touched.

Store occurrence-specific bindings containing occurrence, local port, external
endpoint, relation, direction, and exact weight.

A cross-figure edge must have exactly one physical owner in the payload even
though it contributes to both figures' interface profiles.

## 4. Final graph plus reverse transition deltas can avoid repeated residual graphs

Under sum aggregation, an edge between two untouched singleton nodes has a
one-to-one preimage at the previous level. A consolidated hierarchy can store:

- the final coarse graph once;
- internal/port payload only for edges touching contracted figures at each
  transition.

During reverse decoding, untouched singleton-to-singleton edges are inherited;
all edges touching a figure are replaced by exact transition payload.

This optimization is not automatically valid for normalized or mean-density
aggregation. Either derive and verify an inverse or store the necessary
residual data.

## 5. Semantic embeddings are proposal/ranking signals, not exact symbol identity

A structurally reusable motif must not disappear merely because its endpoints
belong to different GloVe/Wishart families or are OOV/noise.

Prefer:

\[
\text{exact structure}\rightarrow\text{symbol},
\qquad
\text{embedding/density family}\rightarrow\text{ranking/metadata}.
\]

Keep a hard semantic filter only as an explicit ablation/baseline.

## 6. Selection cost and measured storage are different quantities

A codec-aligned logical score should include rule definition, placement,
internal payload, ports, and residuals.

It is appropriate for choosing occurrences, but it still is not the measured
compressed container size. Report both separately.

Port-heavy motifs can have lower compression value than equally frequent
low-rank motifs, so external-interface cost must be present before selection.

## 7. Binary occurrence placement is a high-value early optimization

Occurrence placement is a high-frequency stream. Replace repeated JSON node
arrays with integer IDs and signed delta/varint coding before optimizing rare
metadata. Preserve arbitrary prototype-to-fine permutations; deltas can be
negative.

Exact floating-point weights can be stored as IEEE-754 bit patterns when
bitwise losslessness is required.

## 8. Incremental census must be conservative

After contracting a local region, do not assume every previous match remains
valid.

For radius-r ego candidates with external boundary signatures, a safe initial
invalidation rule is to rescan centers within at least r+1 of every contracted
node on undirected support. Carry forward only exact matches outside that
region.

Also:

- rescan all previous no-match centers, because newly discovered types can now
  match them;
- perform periodic complete censuses;
- after RESUME, force a complete census unless the incremental cache itself is
  versioned and checkpointed;
- test incremental counts against a full census on controlled graphs.

## 9. Graphon/graphex mass must follow original graph mass

At coarse level s, different macro nodes represent different numbers of
level-0 nodes. Do not assign equal mass to coarse nodes merely because they are
one row each.

Use

\[
\mu_s(u)=|\pi_s^{-1}(u)|/|V_0|.
\]

For grammar-symbol blocks, aggregate this original-node mass by symbol.
Relation-specific block intensities should state their exposure denominator
explicitly.

A finite grammar-induced block model is not by itself proof of convergence to
an exchangeable graphon/graphex limit. If only a W-like empirical block kernel
is estimated, explicitly say that S and I are not yet estimated.

## 10. Adjacency redundancy is a verified property, not an assumption

If an archive stores typed relation layers, the aggregate adjacency may be
derivable as their deterministic sum. Check this per run and report shape,
nonzero counts, total weights and maximum absolute residual.

Only omit adjacency.npz as redundant when the declared reconstruction scope and
diagnostic justify it.

## 11. Testing hierarchy

Minimum behavioral coverage should include:

- isomorphic internal shapes with different interfaces;
- relation direction and labels;
- parallel edges;
- self-loops;
- cross-figure edges stored once;
- arbitrary edge order / non-contiguous IDs;
- exact binary64 weights;
- recursive child symbols;
- full transition round-trip;
- consolidated final-to-level-0 round-trip;
- incremental-vs-full census equality;
- port-heavy motifs receiving higher code cost;
- original-mass graph block projection.

A codec test that succeeds only because the whole graph is stored as residual
does not demonstrate grammar compression; track internal/port/residual shares
and actual archive bytes.


## 12. Pipeline CPU-bound scan stages under one worker budget

In recursive graph dictionaries, a full census may contain two different CPU
bottlenecks:

- sparse ego/subgraph extraction, often dominated by SciPy CSR slicing and BFS;
- exact isomorphism/VF2 matching, which is GIL-heavy Python work.

Do not assign `cpu_workers` independently to both stages. That creates nested
oversubscription and can multiply process/thread counts and memory use.

Use one explicit budget:

[
W = W_{mathrm{extract}} + W_{mathrm{match}}.
]

A practical initial split for mixed CSR/VF2 work is roughly one third to
extraction and the remainder to spawned matching processes, with at least one
worker in each stage when (W>1). Keep BLAS/OpenMP thread counts separately
bounded, typically to one thread per worker in Colab.

Pipeline the stages with bounded queues:

[
	ext{extract batch}_{i+1}
parallel
	ext{match batch}_{i}.
]

Important invariants:

- spawn matching processes before starting extraction threads if CUDA has been
  initialized in the parent;
- workers receive only read-only dictionary snapshots;
- persistent dictionary mutation remains in the parent;
- consume results in original center order if candidate IDs/frequencies must
  remain deterministic;
- bound extraction prefetch and matching futures instead of eagerly scheduling
  the whole 100k graph;
- record the effective split and queue limits in run artifacts;
- test serial and parallel census outputs for exact equality.

A notebook should expose one `CPU_WORKERS` budget, not separate unbounded
`n_jobs` knobs. On interruption, RESUME must keep the same code/config/input
lineage; changing worker count may be permitted only if the deterministic
contract has been explicitly tested.
