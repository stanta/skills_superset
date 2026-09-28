# GloVe methods, implementation notes and references

## Primary evidence (consult in this order)

1. Pennington, J., Socher, R., Manning, C. D. (2014). *GloVe: Global Vectors for Word Representation*, EMNLP, pp. 1532–1543. https://aclanthology.org/D14-1162/ — original model, objective, co-occurrence-ratio motivation and evaluation. DOI: 10.3115/v1/D14-1162.
2. Stanford NLP project: https://nlp.stanford.edu/projects/glove/ — pretrained release inventory, model overview and official download links. Match actual dataset license and release metadata before reuse.
3. Stanford implementation: https://github.com/stanfordnlp/GloVe — executable, demo, training documentation and flags. Consult `src/glove.c`, `src/README.md` and `Training_README.md` at the actual revision. The example `-alpha 0.75 -x-max 100` comes from the code's help text; it is **not** a universally optimal configuration. Some 2024 published vector recipes use different values.
4. Gensim KeyedVectors API: https://radimrehurek.com/gensim/models/keyedvectors.html — check the installed major version and `load_word2vec_format(binary=False, no_header=True)`. Gensim 4 supports this headerless-loading path; don't require legacy conversion.
5. SemMap-specific claims about geometry, Wishart, graphons, FGW or graph symbols are project hypotheses/implementation choices, not findings of the original GloVe paper.

## Correct interpretation of the objective

Given global co-occurrence counts `X_ij > 0`, target and context vectors and biases fit `log X_ij` under a frequency-dependent weighting. The weighting suppresses very rare noisy counts and caps common counts. Co-occurrence ratios motivate the model; they are not the literal training target of each summand. A target-context vector sum may improve symmetry in a shared vocabulary but must be reported as an export policy.

### Contrast with SVD

- `SVD(A)` computes a low-rank least-squares approximation to a **specified** matrix under the standard unweighted Frobenius norm (for truncated SVD).
- `GloVe` learns two low-rank factors **plus biases**, with **nonuniform weights**, only on observed positive pairs, generally by iterative optimization.
- Therefore `GloVe = weighted SVD(log X)` is only a loose analogy; even weighted low-rank matrix fitting need not have a closed-form SVD solution.
- A fair comparison fixes corpus, vocabulary, tokenization, dimension, handling of missing counts and downstream evaluation while documenting the exact SVD input (e.g., shifted PPMI versus observed log-counts).

## Corpus/window decision log

Capture language, locale, case policy, Unicode form, tokenization library/version, sentence boundaries, document deduplication, min frequency, window width, context direction and distance weight, memory/overflow settings and whether held-out material influenced vocabulary. Window size adjusts which distributional relations are visible; don't present short-window syntactic / long-window topical tendencies as guarantees.

Use `float32` for exported embeddings when the numerical tolerance and downstream API allow it, but preserve enough count precision during sparse accumulation and verify integer overflow/large counts. Never coerce positive counts to zero through low-precision storage. Large vector files can be memory-expensive beyond their compressed download size.

## Evaluation protocol

Prepare an auditable table with:
`model_id | corpus | language | dim | preprocessing | OOV% | benchmark | score | CI/seeds | runtime | RAM | notes`.
Report denominators for analogy tasks and pair coverage for lexical similarity. Fit any centering, PCA, whitening, or alignment **only** on the training portion. Hold out connected graph nodes/edges/corpus documents according to the actual research question; prevent leaking labels through aliases or duplicate surface forms.

For semantic graph integration, first choose whether vectors represent surface forms, lemmas, phrases or canonical concept IDs. Graph-structured relations such as `IsA` and `Causes` are not derivable solely from nearest lexical neighbors. Validate fusion empirically and preserve provenance per feature.

## Suggested reproducible experiment matrix

Compare: (a) pretrained GloVe matched to language/domain; (b) in-domain GloVe; (c) truncated SVD on a documented co-occurrence transform; (d) graph-structural features alone; (e) fused GloVe+graph. Vary dimension and context window at fixed budget. Include a simple corpus-frequency / TF-IDF or lexical retrieval baseline where relevant. For FGW jointly report feature cost scale, structure cost scale, `alpha` and transport solver.

## Source verification checklist

- Confirm citation DOI/title/authors against ACL Anthology.
- Check Stanford repository commit and help output before publishing CLI flags.
- Check the model card/release page for each vector's corpus, tokenization, casing, language, dimension, licensing and download.
- Check installed gensim API rather than copying an obsolete `glove2word2vec` tutorial.
- Mark all SemMap graphon/multifractal interpretations as hypotheses until measured with an explicit protocol.
