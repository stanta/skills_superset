---
name: google-colab-python
description: This skill should be used when designing, implementing, reviewing, debugging, or optimizing Python notebooks and experiments for Google Colab, especially workflows involving ephemeral runtimes, Google Drive, Git repositories, reproducible dependencies, CPU/GPU/RAM limits, checkpoints, resumption, or notebook hygiene.
license: MIT
metadata:
  category: data-ml
  role: specialist
  scope: architecture-implementation-review
  triggers: Google Colab, Colaboratory, Python notebook, Colab GPU, Colab Drive, drive.mount, Colab OOM, Colab runtime, Colab reproducibility, checkpoint resume
  related-skills: python-pro, python-dev, ml-pipeline, debugging-wizard, devops-engineer
  source:
    type: synthesized-research
    reviewed: "2026-09-23"
---

# Google Colab Python

Design Python work in Google Colab as a reproducible, restartable experiment that happens to have a notebook UI. Do not design it as a persistent server or as a one-off chain of hidden interactive state.

## Core mental model

Separate four concerns:

1. Persistent plane — Git for code and Google Drive or object storage for durable inputs, checkpoints, and final outputs.
2. Scratch plane — the Colab VM, normally under /content, for fast temporary reads, writes, unpacking, caches, and computation.
3. Control plane — the notebook, containing bootstrap, configuration, orchestration, diagnostics, and concise results.
4. Code plane — importable Python modules, packages, and CLI entry points containing non-trivial logic.

Prefer this flow:

    Git repository -----------> /content/project
    Drive/object storage -----> /content/staging
                                      |
                                      v
                              compute on local VM
                                      |
                          logical checkpoints/results
                                      |
                                      v
                            Drive/object storage

Treat runtime loss as normal. Make expensive work resumable by construction.

## When to use

Use this skill for:

- creating or refactoring Colab notebooks;
- adapting a Python repository to run reliably in Colab;
- moving experiments between local development and Colab;
- using Google Drive for datasets, checkpoints, or outputs;
- diagnosing Colab OOM, slow I/O, package conflicts, hidden notebook state, or lost progress;
- running ML/data/scientific workloads on changing CPU/GPU hardware;
- preparing a notebook for sharing, teaching, or reproducible research.

Do not use Colab-specific patterns when a normal Python package, CI job, batch service, or persistent cloud VM is the actual target runtime.

## Non-negotiable invariants

### MUST

- Detect runtime resources before allocating large data or models.
- Keep durable code in Git and durable outputs outside the ephemeral VM.
- Run heavy random-access I/O on local VM storage, not on mounted Drive.
- Make dependency installation explicit and reproducible.
- Keep notebook cells safe to re-run whenever practical.
- Keep configuration, seeds, paths, and run identifiers explicit.
- Checkpoint at semantic boundaries and support resume from the latest valid checkpoint.
- Save a run manifest containing enough information to reproduce or audit the run.
- Test the notebook from a clean runtime with Restart/Run All before declaring it reproducible.
- Keep secrets outside notebook source and normal cell output.

### MUST NOT

- Assume a specific GPU model, RAM amount, disk size, or session duration.
- Treat /content as persistent storage.
- Perform training or graph/data processing directly against thousands of small files on mounted Drive.
- Put substantial reusable logic only inside notebook cells.
- Rely on out-of-order cell execution or variables created by an undocumented exploratory path.
- Blindly upgrade the whole preinstalled Python stack.
- Hard-code API keys, tokens, credentials, personal Drive paths, or user-specific absolute paths.
- Use keepalive, anti-idle, or other mechanisms intended to bypass Colab resource policies.
- Print huge tensors, DataFrames, logs, or secrets into saved notebook output.
- Call GPU cache-clearing functions as a substitute for fixing live references or oversized batches.

## Workflow

### Phase 1 — classify the workload

Classify before writing cells:

| Class | Default strategy |
| --- | --- |
| Small demo/tutorial | Minimal bootstrap, small local data, deterministic example |
| Reproducible experiment | Pin dependencies, pin Git commit, manifest, checkpoints |
| Large Drive-backed dataset | Archive/shard, stage to /content, compute locally, sync results |
| GPU training/inference | Detect GPU, adaptive batch size, AMP when validated, frequent checkpoints |
| Long multi-stage analysis | Separate stages, persist intermediate artifacts, resume per stage |

Prefer a CPU runtime when no accelerator is used. Avoid consuming scarce GPU/TPU resources for CPU-only work.

### Phase 2 — preflight the runtime

Run scripts/colab_preflight.py or an equivalent cell before downloading data or loading a large model.

Inspect at least:

- Python version and executable;
- free local disk;
- available RAM;
- CPU count;
- accelerator availability and model;
- GPU memory when applicable;
- mounted Drive state;
- versions of critical packages.

Fail early if minimum requirements are not met. Never encode today's Colab hardware as a permanent assumption.

### Phase 3 — bootstrap dependencies reproducibly

Prefer the current Colab runtime plus explicit project dependency versions. Pin a past Colab runtime only when the runtime image itself is part of the compatibility contract, such as a workshop or a dependency that cannot be changed independently.

Install dependencies before importing them.

In notebooks, prefer IPython package magics such as %pip because they target the current kernel. For repository-backed projects, prefer a constraints or lock workflow maintained in Git.

For exploratory development:

    %pip install -r requirements.txt
    %pip install -e .

For a reproducible experiment:

    git checkout <exact-commit-sha>
    %pip install -r requirements/locked.txt
    %pip install --no-deps -e .

Use hash-checked requirements for higher-assurance experiments when the project workflow supports them.

Avoid broad commands such as pip install -U <large-stack> unless the compatibility impact is understood. If an installation replaces an already-imported core library, restart the runtime before continuing.

### Phase 4 — define storage roles explicitly

Create three path roots:

- repo_root — checked-out source tree;
- scratch_root — fast local workspace, normally under /content;
- persistent_root — Drive or another durable store.

Use pathlib.Path and derive all other paths from these roots.

For large Drive-backed input:

1. Mount Drive only when needed.
2. Copy a coarse-grained archive or shard from Drive to /content.
3. Verify size or checksum when integrity matters.
4. Unpack or preprocess locally.
5. Run the heavy workload locally.
6. Copy only checkpoints and final artifacts back to persistent storage.

Avoid many small Drive reads/writes. Keep Drive directories reasonably sharded; Colab documentation warns that directories with roughly 10,000 direct children can become unreliable.

### Phase 5 — keep the notebook thin

Use the notebook for:

- human-readable context;
- configuration;
- environment checks;
- package installation;
- authentication and mounts;
- data staging;
- invoking functions or CLI commands;
- compact diagnostics, plots, and summaries.

Move reusable or complex logic into src/, a package, or scripts/.

Make each cell perform one meaningful step. Prefer functions over mutable global state. Make cells idempotent when possible.

Treat Restart runtime -> Run all as a release test, not an optional cleanup step.

### Phase 6 — configure experiments explicitly

Place user-editable parameters in one early configuration cell or a config file.

Record:

- run_id;
- random seed;
- input paths and input fingerprints;
- algorithm/model parameters;
- dependency or environment identifier;
- Git commit SHA and dirty state;
- requested device and detected device;
- checkpoint cadence;
- output path.

For stochastic work, seed every relevant library used by the experiment. Distinguish "seeded" from "fully deterministic": some accelerator kernels remain nondeterministic unless framework-specific deterministic modes are enabled.

### Phase 7 — manage memory and parallelism deliberately

Prefer algorithmic fixes before manual cache clearing:

- process streams/chunks rather than full datasets;
- use generators, iterators, memory maps, sparse matrices, and compact dtypes when appropriate;
- avoid unnecessary DataFrame/array copies;
- delete large references when a stage is complete;
- checkpoint and release stage-local objects;
- monitor peak rather than only current memory.

For PyTorch:

- inspect allocated and reserved CUDA memory when diagnosing OOM;
- reduce batch size, sequence length, resolution, or activation footprint first;
- use automatic mixed precision only when the model and numerical requirements permit it;
- use torch.cuda.empty_cache() only after unused tensors are actually dereferenced; it does not increase memory available to PyTorch for live tensors.

For CPU-heavy numerical code, avoid nested thread oversubscription. Set BLAS/OpenMP thread limits before importing NumPy/SciPy when necessary. Avoid combining n_jobs=-1 with heavily threaded BLAS without measurement.

Move multiprocessing worker functions into importable modules instead of defining fragile process targets deep inside notebook state.

### Phase 8 — checkpoint for interruption

Assume the runtime can disappear.

A useful checkpoint should identify:

- run_id and step/epoch;
- config and seed;
- input fingerprints;
- Git commit;
- model/optimizer/scheduler state when relevant;
- progress cursor or processed shard list;
- metric state needed to continue correctly;
- checkpoint format version.

Write checkpoints locally first. Sync immutable/versioned checkpoint artifacts to persistent storage at semantic boundaries. Write a COMPLETED marker only after final outputs and metadata have been fully synchronized.

On failure, persist a small FAILED.json when possible with phase, exception type, message, and last valid checkpoint.

On resume, validate checkpoint version, config compatibility, and input identity before continuing.

### Phase 9 — handle secrets safely

Prefer Colab Secrets and google.colab.userdata for API keys and similar credentials.

Never:

- paste a secret into notebook source;
- store it in Git;
- print it;
- include it in exception dumps, manifests, or saved outputs;
- copy long-lived credentials into Drive unless the security model explicitly requires it.

Remember that notebook code, comments, and normal outputs are shared when the notebook is shared. Omit saved outputs when they may contain sensitive material.

### Phase 10 — validate and export

Before completion:

1. Run a small smoke test.
2. Check expected artifact counts and schemas.
3. Confirm the latest checkpoint can be loaded.
4. Restart runtime and Run All on a representative path.
5. Capture environment and Git metadata.
6. Sync final artifacts to persistent storage.
7. Write COMPLETED last.
8. Keep notebook outputs concise.
9. Report exact persistent output locations.

## Default notebook structure

Prefer this order:

1. Title, purpose, expected cost/resources.
2. User parameters.
3. Runtime preflight.
4. Dependency bootstrap.
5. Imports.
6. Secrets/authentication.
7. Drive/object-storage mount.
8. Git checkout and project installation when applicable.
9. Path/config construction.
10. Data staging.
11. Smoke test.
12. Main execution.
13. Checkpoint/resume diagnostics.
14. Validation and metrics.
15. Final synchronization.
16. Reproduction manifest and artifact summary.

Do not interleave dependency installation, imports, and main execution without a clear reason.

## Colab review checklist

When reviewing an existing notebook, check these in order:

| Area | Pass condition |
| --- | --- |
| Clean execution | Runs top-to-bottom from a fresh runtime |
| Dependencies | Explicit, version-aware, installed before import |
| Storage | Heavy I/O local; Drive used mainly for persistence |
| Portability | No unexplained user-specific paths |
| State | No hidden out-of-order prerequisites |
| Resources | Hardware detected, not assumed |
| Memory | Bounded/chunked; no obvious full-copy blowups |
| Secrets | No credentials in source or output |
| Recovery | Checkpoints and resume path for expensive work |
| Provenance | Git/config/environment captured |
| Outputs | Bounded and intentionally persisted |
| Policy | No anti-idle or policy-circumvention behavior |

## Reference guide

Load supporting material only when needed:

| Reference | Load when |
| --- | --- |
| references/best-practices.md | Detailed rationale, anti-patterns, storage, packaging, resources, reproducibility |
| references/templates.md | Copy-ready Colab cells and patterns |
| references/research-sources.md | Evidence, source links, and research notes |
| scripts/colab_preflight.py | Runtime resource and dependency preflight |

## Deliverables when using this skill

For notebook creation or refactoring, produce:

1. A thin, ordered notebook flow.
2. Explicit environment and dependency bootstrap.
3. Scratch/persistent storage separation.
4. Runtime/resource preflight.
5. Resume-safe checkpoint strategy when work is expensive.
6. Reproducibility manifest.
7. A clean-run verification plan.
8. A concise list of Colab-specific risks that remain.

For repository adaptation, also produce:

1. A Colab-specific requirements/constraints entry point when needed.
2. Importable Python logic outside the notebook.
3. One CLI or function entry point for the main workload.
4. A Drive staging/sync boundary.
5. A small end-to-end smoke path suitable for Colab.
