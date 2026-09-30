# Engineering playbook

## 1. Define the graph contract first

Record whether the input supports:

- directed edges;
- edge/relation labels;
- node labels/types;
- multiedges;
- self-loops;
- hyperedges;
- weights;
- attributes excluded from or included in exact reconstruction.

Two graphs are "the same symbol" only relative to this contract.

For knowledge graphs, relation direction and label usually belong to the terminal structure. Treating \`IsA\` and \`UsedFor\`, or incoming and outgoing edges, as interchangeable silently changes semantics.

## 2. Core shape and interface

Represent a candidate occurrence as:

~~~text
Occurrence
  internal_graph
  ordered_external_ports
  port_relation_profile
  consumed_edges
  member_nodes
~~~

A reusable symbol can be:

~~~text
GraphSymbol
  symbol_id
  canonical_core
  rank
  ordered_port_schema
  child_symbols
  definition_cost_bits
~~~

If many occurrences share an internal topology but differ in their outer attachment pattern, consider:

~~~text
shape_id + interface_variant_id + bindings
~~~

rather than creating one fully distinct symbol per occurrence.

## 3. Candidate discovery options

### Exact local digrams

Fast and RePair-like. Best when repetitions are literal and local.

### Frequent/canonical motifs

Enumerate bounded subgraphs, hash/canonicalize them, then count occurrences. More expressive, more expensive.

### MDL-guided expansion

Start small and extend promising motifs. Useful when frequency alone finds trivial edges/stars.

### Approximate proposal space

Use descriptors such as typed WL, graphlets, relation histograms, spectral features, embeddings, GW/FGW, or density clustering (including Wishart) to propose families.

**Proposal is not identity.** For lossless grammar rules, validate exact core/interface equivalence or encode residuals.

## 4. Canonicalization pipeline

Use a cheap-to-expensive cascade:

1. invariants: node/edge counts, degree/type histograms, rank;
2. rooted/typed WL or canonical hash;
3. exact canonical labeling / graph-isomorphism verification when required;
4. canonical port ordering.

WL is an excellent partition/filter but is not a complete graph-isomorphism test for arbitrary graphs.

For very small motifs, exact canonical labeling is often cheap enough after bucketing.

## 5. External ports

A node is external when an occurrence has an edge/hyperedge connection to structure outside the consumed fragment.

The port schema should encode, as needed:

- port order;
- node type;
- allowed incoming/outgoing relation labels;
- whether multiple ports may bind the same original node;
- weight/multiplicity semantics.

Rank explosion is a compression hazard. Track:

\[
\mathrm{rank}(T)=|\mathrm{ports}(T)|.
\]

Use a maximum-rank constraint only as an explicit compression/query trade-off, not as an arbitrary magic constant.

## 6. Overlap selection

If occurrences consume the same edge or an internal node that would be removed, they conflict.

For pair-digram RePair, maximum non-overlap may map to a matching problem. For general motifs it resembles weighted set packing and is usually intractable at scale.

Practical strategies:

- deterministic greedy by gain;
- gain per consumed edge/node;
- local improvement / swap;
- partition graph into independent regions;
- approximate MWIS on the conflict graph for high-value candidates.

Always log the selection heuristic because it changes the resulting grammar.

## 7. Coding-aware gain

Raw frequency is insufficient.

For a candidate type \(T\) with selected occurrences \(O\), estimate:

\[
\mathrm{Gain}(T,O)=
L_{\mathrm{raw}}(O)
-
\big[
L_{\mathrm{rule}}(T)
+L_{\mathrm{references}}(O)
+L_{\mathrm{port\ bindings}}(O)
+L_{\mathrm{residuals}}(O)
\big].
\]

Count the start graph, grammar dictionary, symbol IDs, ranks, port bindings, residual edits, relation labels, and any indexes required by the claimed query workload.

A rule that appears only once should normally be inlined unless it provides query/semantic value that is explicitly part of the objective.

## 8. Replacement and hierarchy

Maintain an acyclic rule DAG:

~~~text
S
 ├─ T17
 │   ├─ T4
 │   └─ terminals
 └─ T9
~~~

Every new nonterminal may refer only to terminals and previously defined nonterminals, or otherwise preserve an explicit topological order.

Store original membership separately if users need to map compressed symbols back to original concepts without full expansion.

## 9. Incremental occurrence maintenance

Avoid rescanning the entire graph after every replacement.

When replacing occurrence \(o\):

1. identify edges incident to its attachment ports;
2. invalidate motif occurrences touching consumed/changed edges;
3. introduce the nonterminal edge/node representation;
4. enumerate only newly possible motifs in the affected neighborhood;
5. update counts/priority queues.

This local-update pattern is essential for RePair-like scalability.

## 10. Approximate family + residual design

For an approximate family:

~~~text
FamilySymbol
  prototype / canonical medoid
  allowed edit alphabet
  interface schema
Occurrence
  family_id
  port bindings
  residual edit script
~~~

Possible residual operations:

- add/remove internal edge;
- relation-label substitution;
- direction change;
- node-type exception;
- extra/missing port;
- external-edge correction.

Use a prefix-decodable or otherwise self-delimiting residual code. The family is beneficial only if prototype references plus residuals beat exact alternatives.

## 11. Symbol coding

After grammar discovery, encode symbol references by:

- Huffman code for simple static frequency coding;
- arithmetic/range coding for closer-to-entropy coding;
- conditional coding \(P(T_j\mid T_i)\) for grammar-context streams if justified.

Keep **grammar definition cost** separate from **symbol-stream entropy**. A shorter Huffman stream cannot rescue an overgrown dictionary.

## 12. Direct queries on the grammar

Before adding query indexes, classify the workload:

- neighbor enumeration;
- triple lookup;
- reachability;
- regular path query;
- motif/pattern search;
- original-node membership;
- random access.

Some SL-HR methods support reachability/traversal without full decompression; ITR targets neighborhood/triple access. Query-specific indexes add storage cost and must be included in the compression benchmark.

## 13. Reproducibility manifest

Store:

~~~text
input graph hash
code commit
graph semantics contract
candidate method + parameters
canonicalization method/version
node/order seed
overlap heuristic
max rank
pruning policy
coding model
query indexes
lossless/lossy mode
residual alphabet
~~~

For approximate/discovery pipelines also store random seeds and candidate sampling policy.

## 14. Wishart-assisted dictionary discovery

A safe integration is:

\[
G
\to
\text{local subgraphs}
\to
\phi(H)
\to
\text{Wishart modes}
\to
\text{candidate families}
\to
\text{canonical/residual symbols}
\to
\text{MDL selection}
\to
\text{recursive replacement}.
\]

Recommended data model:

~~~text
wishart_mode_id      # local proposal only
shape_id             # persistent exact/reconstructible core
variant_id           # interface/residual variant
symbol_id            # grammar nonterminal
occurrence_id
~~~

Run a full-graph census after discovery; do not estimate Huffman probabilities only from the Wishart candidate sample.

## 15. Common implementation failures

| Failure | Consequence | Fix |
|---|---|---|
| cluster ID used as persistent symbol | level-local IDs masquerade as grammar | canonical persistent \`symbol_id\` |
| ignores external interface | decode/query corruption | explicit ranked ports |
| counts all overlaps as usable | impossible replacement set | conflict-aware selection |
| optimizes node reduction only | may increase bits | total-code MDL |
| approximate family without residual | silent lossy compression | residual or label as lossy |
| WL hash treated as proof of isomorphism | false symbol merging | exact verification after bucketing |
| rule dictionary not charged | fake compression | include grammar/index cost |
| only one node ordering/seed | unstable RePair result hidden | repeat orderings/seeds |


## 16. Decoder-first recursive hierarchy

For recursive coarsening, do not rely on the quotient graph alone. A practical exact design is:

\[
\text{final coarse graph}+\sum_s \text{reverse transition delta}_s.
\]

When aggregation is a simple sum, unchanged singleton-to-singleton edges can be inherited from the next coarser level. Store exact internal/port payload for every edge touching a contracted figure. Require an end-to-end reverse decode before publishing completion.

Do not reuse this inheritance rule for mean-density or normalized aggregation without deriving and testing the inverse.

## 17. Conservative incremental census

If ego identity includes external boundary statistics, contraction can change a candidate even when the contracted node lies just outside the ego. For radius-r egos, invalidate at least the undirected radius-(r+1) neighborhood of changed nodes.

Carry forward only already-exact matches outside the invalid region. Rescan all previous no-match centers because newly learned dictionary types can match them. Periodically force a full census and test incremental counts against it.

## 18. Graphon/graphex projection from a compressed hierarchy

Mass at coarse levels must represent level-0 mass, not one unit per macro node:

\[
\mu_s(u)=|\pi_s^{-1}(u)|/|V_0|.
\]

Keep the lossless grammar and the statistical graph model as separate projections of the same hierarchy. A finite relation-specific block intensity is a W-like empirical model, not automatically a complete graphex; state explicitly when S or I are not estimated.

See [SemMap implementation findings](semmap-implementation-findings.md) for tested details.


## 16. Interface schema is not edge multiplicity

 If exact external edge records are already stored as occurrence-level port bindings, do not repeat one identical PortSpec per external record in the reusable interface identity.

Prefer:

~~~text
InterfaceVariant
  unique allowed/local typed-directed ports

Occurrence
  one PortBinding per exact external edge record
~~~

Thus two occurrences can share one interface variant even when one has one `RelatedTo` edge through a port and another has several. Multiplicity, endpoints, weights and record identity live in the bindings.

Making multiplicity part of the interface type fragments the dictionary, inflates variant metadata and lowers apparent symbol reuse without adding reconstruction information.

Retain multiplicity in the variant only if the grammar semantics explicitly requires a fixed arity/count constraint that is not otherwise encoded.

## 17. Compression baselines must be representation-competitive

Do not claim grammar compression from a comparison against verbose JSON or a raw text edge list alone.

At minimum report a compact exact non-grammar baseline using the same semantic contract:

- integer/varint node and relation IDs;
- exact record order or an explicit order code;
- exact binary64 weight bits when bitwise floating-point fidelity is required;
- the same membership/label payloads when the candidate archive stores them;
- the same required adjacency fallback or other decoder-required metadata.

For a hierarchy archive, compare like with like. If the grammar archive stores level-0 memberships, the baseline bundle must also store those memberships. Keep older/legacy ratios for continuity, but label the compact binary ratio as the primary storage comparator for new claims.

Report both legacy and compact-binary ratios. Only the compact exact baseline is suitable for a strong statement that the grammar itself beats a reasonable exact representation.
