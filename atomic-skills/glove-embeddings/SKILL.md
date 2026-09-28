---
name: glove-embeddings
description: >-
  Use for selecting, loading, training, auditing, comparing, and evaluating GloVe
  word embeddings, including corpus co-occurrence engineering, reproducible
  Python/Colab workflows, SVD baselines, and text-attributed semantic graphs
  such as ConceptNet/SemMap. Trigger for GloVe, global vectors, weighted
  log-co-occurrence factorization, pretrained GloVe vectors, or GloVe-to-graph alignment.
metadata:
  category: machine-learning
  last_verified: "2026-09-28"
---

# GloVe embeddings: evidence-based workflow

## Mission and boundaries

Produce a reproducible, task-evaluated GloVe embedding pipeline. Distinguish **word-form distributional similarity** from a unique concept identity, ontological relation, contextual sense, or causal inference. Never equate word embeddings with a semantic ontology. Read [references/glove-methods.md](references/glove-methods.md) when selecting objectives, datasets, formats, baselines or evaluation protocols.

## Route the request

1. **Inspect** task (nearest-neighbor retrieval, lexical similarity, domain adaptation, graph feature initialization, analogy, cluster discovery), target language/domain, vocabulary, available corpus, memory, compute, and desired reproducibility.
2. **Choose** pretrained vectors when coverage and corpus provenance fit the task. Otherwise train on a licensed representative corpus, with a pretrained-versus-in-domain comparison if practical. Explicitly check whether a downloaded model supports the target language and domain; English vectors are not automatically Russian vectors.
3. **Record** vector distribution/version, tokenizer/normalization, vocabulary mapping, dimension, OOV policy, corpus provenance and license, embedding transformation, seed, and evaluation split in an experiment manifest.
4. **Validate** shape, dtype, all-finite values, duplicate tokens, exact token-to-row alignment, norm distribution and vocabulary coverage before use. Keep a raw copy and record whether vectors are normalized.
5. **Evaluate** against task-specific baselines and holdouts; publish negative results and limitations alongside successful metrics.

## Mathematical contract

For word \(i\), context \(j\) and positive co-occurrence count \(X_{ij}\), optimize

\[
J = \sum_{(i,j):X_{ij}>0} f(X_{ij})
\big(w_i^\top \tilde w_j+b_i+\tilde b_j-\log X_{ij}\big)^2,
\quad
f(x)=\begin{cases}(x/x_{\max})^\alpha&x<x_{\max},\\1&x\ge x_{\max}.\end{cases}
\]

Keep separate word and context embeddings during training and document whether export uses \(w_i\), \(\tilde w_i\), or \(w_i+\tilde w_i\). The usual final vector is their sum for a shared word/context vocabulary; never silently assume this for a third-party export.

**Do not claim GloVe literally computes SVD.** It fits a *weighted, biased log-co-occurrence regression* on observed entries; truncated SVD of a suitably transformed matrix is a useful but non-equivalent baseline. Missing \(X_{ij}=0\) values must not be sent through \(\log\); they are excluded from the standard objective, not automatically treated as zero log counts.

## Load pretrained vectors

Prefer the official Stanford distribution and verify the archive provenance, extraction size and license for the actual chosen dataset. In gensim 4+, headerless GloVe text can be loaded directly:

```python
from gensim.models import KeyedVectors

kv = KeyedVectors.load_word2vec_format(
    "glove.6B.100d.txt", binary=False, no_header=True
)
assert kv.vector_size == 100
assert "the" in kv
```

Use \(no\_header=True\) only for the headerless GloVe text format. Precheck available RAM (vocabulary × dimension × dtype plus Python/index overhead); use a justified `limit` for a pilot and clearly label coverage truncation. Cache large loaded vectors as gensim native files only after validating their version/provenance. Do not use deprecated `glove2word2vec` as the default path.

## Train on a new corpus

1. Fix corpus snapshot, language, license, sentence boundaries, normalization (including Unicode), tokenization/lemmatization decision and train/validation/test split **before** fitting vocabulary or building co-occurrences. Beware that lemmatization can merge different senses and that n-grams change the unit being embedded.
2. Count vocabulary with a documented `min_count`, unknown-word policy and maximum size. For every token, collect context counts within a documented window, distance weighting and symmetry/direction policy; preserve sparse counts rather than a full \(|V|\times|V|\) dense matrix.
3. Run the official Stanford `vocab_count → cooccur → shuffle → glove` pipeline for a reliable baseline. Inspect flags with the *checked-out source version*; select dimension, window, \(\alpha\), \(x_{max}\), epochs, threads and optimizer/learning rate from a pilot rather than presenting sample values as universal optima.
4. Save and verify corpus/vocabulary hashes, build/commit, command, seed, hyperparameters, checkpoints and model export. Evaluate at multiple epochs to detect overtraining. GPU is **not** provided by the standard Stanford C training executable; do not claim Colab GPU utilization without a verified GPU implementation and device-level measurements.
5. On interrupted runs, resume only from a checkpoint that truly includes the needed optimizer state and matching vocabulary/co-occurrence data; otherwise label the restart as retraining or warm-start, not exact continuation.

## Metrics and checks

- **Intrinsic**: vocabulary coverage and OOV by frequency/domain; lexical similarity Spearman on an appropriate *held-out*, language-matched set; nearest-neighbor manual audit (polysemy, antonyms, morphology); analogy accuracy with explicit OOV and no-answer accounting. Analogy results alone do not establish downstream utility.
- **Extrinsic**: retrieval Recall@k/MRR/nDCG or task-specific downstream metrics; use the same splits, candidate pool, tokenization, dimensionality budget and preprocessing across baselines. Report confidence intervals or repeated-seed variability where feasible.
- **Robustness**: rare-word frequency buckets, domain shift, corpora from another time period, subword/OOV cases, perturbation of window and \(x_{max}\), and lexical leakage. Record memory, wall time and throughput.
- **Bias and privacy**: audit representational stereotypes and sensitive training content before publishing nearest neighbors; do not expose private corpus tokens through example outputs.

## SemMap / ConceptNet integration

Use GloVe as **one feature view** for lexical labels, not as the canonical coordinate of a concept. Attach vectors to graph nodes using an explicit, loss-audited mapping: concept ID → language + normalized label / aliases → token sequence → pooled or phrase vector, with OOV mask and uncertainty flag. Compare mean/weighted pooling with a phrase-specific or contextual baseline when word order or polysemy matters. Preserve edge type/direction and graph structure separately.

For typed-WL, motif statistics, Wishart, FGW or graphon/graphex experiments, test GloVe-only, graph-only and fused features under identical graph splits and seeds; normalize and calibrate feature-vs-structure scales before selecting FGW \(\alpha\). Avoid constructing dense all-pairs word similarities or treating vector cosine as edge probability. A sparse kNN graph is an experimental derived graph, **not** the original ontology. Check hubness and neighbor stability; log the graph construction threshold and sampling procedure.

## Deliverables

Return: (1) short decision with assumptions and suitability; (2) executable commands/code matched to environment; (3) manifest and versioned artifacts; (4) evaluation table including baselines, coverage and uncertainty; (5) explicit known limitations and next experiment. Separate published method claims from project hypotheses. Never invent measured quality, speedups, GPU use or trained-model outputs.

## Sources

Read source-specific detail and links in [references/glove-methods.md](references/glove-methods.md). Prioritize Pennington, Socher & Manning (2014), the Stanford GloVe project and source code, and maintained library documentation.