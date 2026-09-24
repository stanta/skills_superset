# Google Colab Python: Detailed Best Practices

This reference expands the operating rules in SKILL.md. Prefer the main skill for day-to-day execution and load this file when designing a non-trivial Colab workflow or reviewing reliability problems.

## 1. Treat Colab as ephemeral compute

A managed Colab runtime is a temporary VM with dynamically allocated resources. Hardware availability, memory, accelerator type, and runtime lifetime can vary. Do not make correctness depend on a specific T4/A100/L4, an exact RAM size, or a session surviving until the end.

Design consequences:

- discover resources at runtime;
- place durable code in Git;
- place durable experiment state in Drive/object storage;
- place high-frequency scratch I/O on the VM;
- make long work resumable;
- make setup reconstructable from notebook cells and repository files.

The correct failure model is "the VM may disappear between checkpoints", not "the VM will probably stay alive".

## 2. Use a three-tier storage policy

### Local VM: hot tier

Use /content or another local path for:

- extracted datasets;
- temporary preprocessing output;
- model caches;
- SQLite/temp databases;
- sparse matrix workspaces;
- compilation/build output;
- high-frequency checkpoints before sync;
- files repeatedly scanned or randomly accessed.

Local storage is fast but ephemeral.

### Drive/object storage: durable tier

Use Google Drive or another persistent store for:

- original datasets;
- compact archives/shards;
- immutable checkpoints;
- final outputs;
- run manifests;
- artifacts that must survive runtime replacement.

Drive is convenient but mounted-Drive I/O has higher latency and quota/folder-size failure modes. Avoid treating it as a POSIX SSD.

### Git: code/provenance tier

Use Git for:

- source code;
- configs;
- requirements/constraints;
- notebook source;
- small test fixtures;
- experiment definitions.

Do not use Git for large generated artifacts unless the repository intentionally supports them.

## 3. Stage data instead of computing on Drive

The highest-value Colab performance pattern is:

    persistent archive/shard -> local VM -> compute -> durable checkpoint/result

Prefer one large tar/zip or a moderate number of shards over tens of thousands of tiny files.

Example strategy:

1. Mount Drive.
2. Copy dataset.tar.zst or shard-003.parquet to /content/data.
3. Verify expected file size/checksum when important.
4. Unpack/read locally.
5. Write temporary results locally.
6. Copy a checkpoint bundle to Drive after a logical unit of work.

Colab documentation warns that Drive mounting or folder access can become unreliable when a folder has roughly 10,000 direct items. Shard directories and avoid huge flat layouts.

## 4. Make setup explicit and restart-safe

A shared notebook does not share the VM, packages, or custom files that happened to exist in the author's runtime. Therefore include setup steps needed to reconstruct the environment.

Prefer this order:

1. configuration;
2. package installation;
3. runtime restart when required;
4. imports;
5. authentication;
6. mounts;
7. repository checkout/install;
8. data staging;
9. execution.

Avoid importing a library and then replacing it with a different version later in the same kernel.

### Package installation

Prefer %pip in notebooks because IPython executes it for the current kernel.

For a project repository, maintain dependency policy in repository files rather than scattering package versions across many cells.

Recommended patterns:

Exploration:

    %pip install -r requirements.txt
    %pip install -e .

Reproducible run:

    git checkout <commit>
    %pip install -r requirements/locked.txt
    %pip install --no-deps -e .

High-assurance run:

- pin every resolved dependency;
- optionally require hashes;
- capture pip freeze;
- capture the Colab runtime/Python version;
- capture Git SHA and dirty state.

Google recommends using the latest Colab runtime by default and installing the specific library versions a notebook needs. Pin an older runtime image only when a core dependency or teaching/workshop contract requires it.

## 5. Keep notebook state observable

Interactive notebooks make hidden state easy to create. Typical failure pattern:

- cell 20 depends on a variable produced by an old version of cell 7;
- cell 7 is edited but not rerun;
- outputs still look plausible;
- a collaborator runs top-to-bottom and gets a different result.

Prevent this by:

- making each cell one meaningful step;
- avoiding duplicated/tweaked copies of the same logic;
- putting parameters near the top;
- using functions and modules instead of free-floating mutable globals;
- saving intermediate artifacts only when they are intentionally part of the workflow;
- regularly using Restart runtime -> Run all.

For reusable logic, prefer a Python package or module. A notebook should narrate and orchestrate the computation, not be the only implementation.

## 6. Make cells idempotent where practical

A re-run-safe cell should not corrupt state or duplicate outputs.

Prefer:

    output_dir.mkdir(parents=True, exist_ok=True)

over assumptions that directories do not exist.

Prefer writing to deterministic run-specific paths over appending to one global file.

When a destructive operation is required:

- make the target explicit;
- assert path boundaries;
- print a concise plan;
- avoid recursive deletion of user Drive roots.

For setup steps, detect existing clone/mount/cache state instead of blindly recreating it.

## 7. Separate configuration from code

Use a single config object/file for parameters that change between runs.

Good candidates:

- dataset URI/path;
- run_id;
- random seed;
- number of epochs/iterations;
- batch size;
- checkpoint cadence;
- model/algorithm options;
- output root;
- feature flags.

Avoid editing magic constants across many cells.

For research workloads, serialize the final resolved config into the run directory before execution.

## 8. Reproducibility is more than a seed

Record:

- exact code revision;
- dependency versions;
- runtime/Python version;
- input fingerprints;
- config;
- seed(s);
- hardware/accelerator;
- important environment variables;
- output artifact hashes when practical.

Seed every random generator used by the workload, such as Python random, NumPy, PyTorch, JAX, or TensorFlow.

For GPU frameworks, distinguish two levels:

- seeded: random sources initialized repeatably;
- deterministic: framework configured to reject/avoid nondeterministic kernels where possible.

Full bitwise reproducibility can cost performance and may not be possible across different hardware/software stacks. State the level required.

## 9. Build interruption tolerance into the algorithm

Checkpoint by semantic progress, not only wall clock.

Examples:

- each processed dataset shard;
- each recursive graph coarsening level;
- each training epoch or fixed number of steps;
- each search partition;
- each completed simulation batch.

A good checkpoint contains enough state to continue without silently repeating or skipping work.

Prefer immutable checkpoint names:

    checkpoint_000120/
    checkpoint_000240/
    checkpoint_000360/

Keep a small latest-checkpoint pointer/manifest if helpful, but validate the pointed artifact before use.

Write COMPLETED only after final artifact sync succeeds.

Optionally write FAILED.json containing:

- timestamp;
- phase;
- exception class;
- short message;
- last valid checkpoint;
- Git SHA;
- run_id.

Do not store secrets or full sensitive stack locals.

## 10. Use local-then-sync for checkpoints

Avoid serializing a large model directly to Drive while training. A network interruption can leave a partial artifact.

Safer sequence:

1. write checkpoint to local scratch;
2. fsync/close it;
3. validate that it can be reopened;
4. copy to an immutable persistent path;
5. write/update a small checkpoint index last.

For multi-file checkpoints, bundle or version the directory rather than updating files in place.

## 11. Plan memory before optimizing code style

Colab OOM failures are often architectural:

- loading a 20 GB CSV twice;
- converting sparse data to dense;
- materializing all pairwise distances;
- keeping every model output in a list;
- accidentally copying a DataFrame several times;
- using a batch size chosen for a different GPU.

Preferred responses:

- stream or chunk input;
- pre-shard large datasets;
- use Parquet/Arrow for columnar access;
- use sparse matrices for sparse graphs/features;
- choose compact dtypes;
- iterate over generators;
- preallocate when size is known;
- aggregate online;
- spill deliberate intermediates to local disk;
- release stage-local references.

Measure peak memory. A program that finishes a stage at low memory may still have peaked above the runtime limit.

## 12. PyTorch GPU guidance

Always detect device and GPU memory. Never assume CUDA is present because a notebook is configured for GPU; allocation can change.

Use automatic mixed precision when:

- the workload is dominated by compatible tensor operations;
- numerical validation shows acceptable behavior;
- the selected accelerator benefits from lower precision.

For OOM:

1. identify live allocations;
2. reduce batch/sequence/resolution;
3. enable gradient accumulation or checkpointing if appropriate;
4. use mixed precision when valid;
5. delete no-longer-needed tensors;
6. then use empty_cache only if fragmentation/cached blocks are relevant.

PyTorch documents that empty_cache releases unused cached blocks for other applications but does not increase memory available to PyTorch for live tensors.

## 13. Avoid CPU oversubscription

A Colab VM may have only a small number of CPUs. Libraries such as OpenBLAS, MKL, NumExpr, joblib, multiprocessing, and framework data loaders can each create worker pools.

Bad pattern:

- BLAS uses all cores;
- joblib starts one worker per core;
- every worker starts BLAS threads.

The result can be slower than single-level parallelism and can increase memory.

Mitigations:

- inspect os.cpu_count();
- set OMP_NUM_THREADS/MKL_NUM_THREADS/OPENBLAS_NUM_THREADS before importing numerical libraries when necessary;
- benchmark one parallel layer at a time;
- avoid n_jobs=-1 by default for memory-heavy tasks;
- keep notebook process orchestration simple;
- define multiprocessing workers in importable modules.

## 14. Control output volume

Notebook output becomes part of the notebook unless omitted/cleared. Huge output:

- bloats Drive and Git;
- slows rendering;
- can expose sensitive information;
- makes collaboration painful.

Prefer:

- logging every N steps;
- compact metric tables;
- bounded head/tail samples;
- saving full logs as files;
- plots summarized from persisted metrics.

Never print full environment variables or secret objects.

## 15. Use secrets, not literals

For API keys and tokens, prefer Colab Secrets and google.colab.userdata.

Load at execution time and pass values directly to clients or transient environment variables.

Avoid:

- hard-coded tokens;
- tokens in Git remote URLs;
- secrets in notebook parameters;
- echoing shell commands that contain credentials;
- saving secret-bearing outputs.

Remember that sharing a notebook shares source, comments, and saved outputs.

## 16. Prefer repo-backed code over notebook-only projects

For anything beyond a demo:

- put library code under src/ or a package;
- expose a function or CLI entry point;
- keep configs in files;
- write tests in the repository;
- make Colab invoke the same code used locally/CI.

Benefits:

- real diffs and code review;
- linting/type checking;
- tests outside a long-running notebook;
- easier local reproduction;
- smaller notebook;
- less hidden state.

A Colab notebook then becomes an executable runbook.

## 17. Use a smoke path

Every expensive workflow should have a small mode that completes quickly.

Examples:

- first 1,000 rows;
- first graph shard;
- two training batches;
- one coarsening level;
- tiny synthetic dataset.

Run this after dependency setup and before committing GPU-hours to the full job.

The smoke path should validate:

- imports;
- filesystem permissions;
- expected schemas;
- accelerator code path;
- checkpoint write/read;
- final sync.

## 18. Capture a run manifest

Create a JSON/YAML manifest near final artifacts with at least:

- started_at / completed_at;
- run_id;
- status;
- Git SHA;
- Git dirty flag;
- Python version;
- critical package versions or pip freeze path;
- detected hardware;
- config;
- input identifiers/hashes;
- checkpoint lineage;
- final artifact list.

Keep the manifest small and machine-readable.

## 19. Common anti-patterns

| Anti-pattern | Why it fails | Preferred replacement |
| --- | --- | --- |
| Read every training sample directly from Drive | latency/quota/file-count pressure | copy archive/shards to /content |
| Save every tiny intermediate to Drive | slow, unreliable, cluttered | local aggregation + periodic bundle/checkpoint |
| One 1,000-line notebook cell | impossible to test/reuse | module + thin invocation cell |
| pip install latest halfway through notebook | kernel/package inconsistency | install first; pin; restart if needed |
| Assume T4/A100 and fixed memory | hardware varies | detect capabilities |
| Batch size copied from another runtime | OOM/underutilization | derive/test adaptive batch size |
| Keep all outputs in RAM | peak memory explosion | online aggregation/chunking |
| Call empty_cache after every batch | synchronization/overhead, does not fix live tensors | manage references and workload size |
| Put API key in a cell | leaks when shared | Colab Secrets |
| Rely on manual cell order | hidden state | top-to-bottom workflow + clean-run test |
| No checkpoint until end | runtime loss destroys progress | semantic periodic checkpoints |
| Store 50,000 files in one Drive folder | mount/I/O failures | sharded directories/archives |
| Keepalive/anti-idle JavaScript | policy circumvention | design for interruption/resume |

## 20. Review severity guide

Classify review findings:

### Critical

- secrets committed or printed;
- destructive Drive operations with unsafe path handling;
- expensive run cannot resume and loss would be substantial;
- correctness depends on hidden cell state;
- output is only in ephemeral storage after completion.

### High

- heavy compute directly over Drive;
- unpinned dependencies for a published/research experiment;
- hard-coded accelerator assumptions;
- deterministic claim without evidence;
- checkpoint incompatible with resume logic.

### Medium

- overly large cells;
- excessive notebook output;
- avoidable duplicate data copies;
- missing smoke mode;
- unclear path/config handling.

### Low

- cosmetic cell organization;
- minor logging polish;
- optional resource diagnostics.
