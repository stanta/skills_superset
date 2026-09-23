# Colab Python Templates

Use these snippets as starting points. Adapt them to the repository rather than pasting all of them blindly.

## 1. Parameters and paths

    from pathlib import Path
    from dataclasses import dataclass

    @dataclass(frozen=True)
    class RunConfig:
        run_id: str
        seed: int = 42
        drive_project: str = "MyDrive/MyProject"
        min_free_disk_gb: float = 10.0

    CFG = RunConfig(run_id="exp-001")

    CONTENT = Path("/content")
    REPO = CONTENT / "project"
    SCRATCH = CONTENT / "scratch"
    DRIVE_MOUNT = CONTENT / "drive"
    PERSISTENT = DRIVE_MOUNT / CFG.drive_project

    SCRATCH.mkdir(parents=True, exist_ok=True)

Avoid embedding a personal email address or user-specific absolute Drive path deeper than the single configurable project root.

## 2. Runtime inspection

    import os
    import platform
    import shutil
    import subprocess
    import sys

    print("Python:", sys.version)
    print("Executable:", sys.executable)
    print("Platform:", platform.platform())
    print("CPUs:", os.cpu_count())

    disk = shutil.disk_usage("/content")
    print("Disk free GiB:", round(disk.free / 1024**3, 2))

    if shutil.which("nvidia-smi"):
        subprocess.run(["nvidia-smi"], check=False)
    else:
        print("No NVIDIA GPU detected")

For automated checks, prefer scripts/colab_preflight.py.

## 3. Dependency installation

Put installs before imports.

    %pip install -r requirements.txt
    %pip install -e .

For an exact repository state, checkout an immutable commit before editable installation.

    import subprocess

    subprocess.run(
        ["git", "-C", "/content/project", "checkout", "<commit-sha>"],
        check=True,
    )

Do not run a broad package upgrade cell only because Colab packages are "old". Upgrade only dependencies required by the project.

## 4. Drive mount

    from google.colab import drive

    if not Path("/content/drive/MyDrive").exists():
        drive.mount("/content/drive")

Treat mounting Drive as granting notebook code access to Drive. Mount only when required.

## 5. Secrets

    from google.colab import userdata

    API_KEY = userdata.get("MY_API_KEY")

Do not print API_KEY. Prefer passing it directly to a client constructor.

If an SDK only accepts an environment variable:

    import os
    os.environ["MY_API_KEY"] = userdata.get("MY_API_KEY")

Avoid persisting the environment or dumping os.environ to output.

## 6. Stage an archive from Drive to local scratch

    from pathlib import Path
    import shutil
    import tarfile

    src = PERSISTENT / "datasets" / "dataset.tar.gz"
    local_archive = SCRATCH / src.name
    local_data = SCRATCH / "dataset"

    if not local_archive.exists():
        shutil.copy2(src, local_archive)

    if not local_data.exists():
        local_data.mkdir(parents=True, exist_ok=True)
        with tarfile.open(local_archive, "r:gz") as tf:
            tf.extractall(local_data)

For untrusted archives, add safe-path extraction checks instead of blindly extractall.

## 7. Checksum validation

    import hashlib

    def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as f:
            while chunk := f.read(chunk_size):
                digest.update(chunk)
        return digest.hexdigest()

    actual = sha256_file(local_archive)
    assert actual == EXPECTED_SHA256, (actual, EXPECTED_SHA256)

Use checksums for immutable datasets, model files, or checkpoints when correctness depends on exact content.

## 8. Seed common libraries

    import os
    import random

    def seed_python_numpy(seed: int) -> None:
        os.environ["PYTHONHASHSEED"] = str(seed)
        random.seed(seed)

        try:
            import numpy as np
        except ImportError:
            pass
        else:
            np.random.seed(seed)

    seed_python_numpy(CFG.seed)

For PyTorch:

    import torch

    torch.manual_seed(CFG.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(CFG.seed)

If strict determinism is required, explicitly enable framework deterministic settings and document the performance/compatibility impact.

## 9. Device detection

    import torch

    if torch.cuda.is_available():
        device = torch.device("cuda")
        props = torch.cuda.get_device_properties(0)
        print("GPU:", props.name)
        print("VRAM GiB:", round(props.total_memory / 1024**3, 2))
    else:
        device = torch.device("cpu")
        print("GPU unavailable; using CPU")

Do not branch on a hard-coded GPU model unless the algorithm genuinely requires that device feature.

## 10. PyTorch AMP

    use_amp = device.type == "cuda"
    scaler = torch.amp.GradScaler("cuda", enabled=use_amp)

    for batch in loader:
        optimizer.zero_grad(set_to_none=True)
        with torch.autocast(
            device_type=device.type,
            dtype=torch.float16,
            enabled=use_amp,
        ):
            loss = compute_loss(batch)

        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()

Validate numerical behavior before making AMP the default.

## 11. Memory-aware chunking

    import pandas as pd

    total = 0
    for chunk in pd.read_csv(input_path, chunksize=250_000):
        total += process_chunk(chunk)

Prefer Parquet when repeated typed/columnar access is important and the upstream format allows it.

## 12. Versioned checkpoint directory

    import json
    import shutil
    from datetime import datetime, timezone

    def utc_now() -> str:
        return datetime.now(timezone.utc).isoformat()

    def save_checkpoint(
        step: int,
        state_path: Path,
        persistent_run_dir: Path,
        metadata: dict,
    ) -> Path:
        local_dir = SCRATCH / "checkpoints" / f"checkpoint_{step:08d}"
        local_dir.mkdir(parents=True, exist_ok=False)

        shutil.copy2(state_path, local_dir / state_path.name)
        (local_dir / "checkpoint.json").write_text(
            json.dumps(
                {
                    "format_version": 1,
                    "step": step,
                    "created_at": utc_now(),
                    **metadata,
                },
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )

        remote_dir = persistent_run_dir / "checkpoints" / local_dir.name
        if remote_dir.exists():
            raise FileExistsError(remote_dir)
        shutil.copytree(local_dir, remote_dir)
        return remote_dir

Prefer immutable checkpoints. Avoid updating a large checkpoint in place.

## 13. COMPLETED sentinel

    import json

    completed = {
        "status": "completed",
        "run_id": CFG.run_id,
        "completed_at": utc_now(),
    }

    (persistent_run_dir / "COMPLETED").write_text(
        json.dumps(completed, indent=2),
        encoding="utf-8",
    )

Write this only after all required result files have been synchronized and validated.

## 14. Failure marker

    import traceback

    try:
        run_experiment()
    except Exception as exc:
        failure = {
            "status": "failed",
            "run_id": CFG.run_id,
            "exception_type": type(exc).__name__,
            "message": str(exc),
            "traceback_tail": traceback.format_exc().splitlines()[-20:],
        }
        (persistent_run_dir / "FAILED.json").write_text(
            json.dumps(failure, indent=2),
            encoding="utf-8",
        )
        raise

Do not serialize arbitrary locals into failure diagnostics because they may contain secrets or huge objects.

## 15. Git provenance

    import subprocess

    def git_text(*args: str) -> str:
        return subprocess.check_output(
            ["git", "-C", str(REPO), *args],
            text=True,
        ).strip()

    git_sha = git_text("rev-parse", "HEAD")
    git_dirty = bool(git_text("status", "--porcelain"))

Record both. A dirty working tree means the commit SHA alone is not a complete reproduction identifier.

## 16. Run manifest

    import json
    import platform
    import sys

    manifest = {
        "format_version": 1,
        "run_id": CFG.run_id,
        "python": sys.version,
        "platform": platform.platform(),
        "git_sha": git_sha,
        "git_dirty": git_dirty,
        "config": CFG.__dict__,
    }

    (persistent_run_dir / "run_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True),
        encoding="utf-8",
    )

For rigorous experiments, also save a pip freeze file and input hashes.

## 17. Package snapshot

    import subprocess
    import sys

    with (persistent_run_dir / "pip_freeze.txt").open("w", encoding="utf-8") as f:
        subprocess.run(
            [sys.executable, "-m", "pip", "freeze"],
            check=True,
            stdout=f,
            text=True,
        )

Use this as evidence, not necessarily as the project's hand-maintained dependency specification.

## 18. Limit CPU thread oversubscription

Set before importing NumPy/SciPy for the clearest effect.

    import os

    os.environ.setdefault("OMP_NUM_THREADS", "2")
    os.environ.setdefault("MKL_NUM_THREADS", "2")
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")

Choose values from measurement and available CPU count, not from this example.

## 19. Bounded logging

    import logging

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    log = logging.getLogger("experiment")

    for step, batch in enumerate(loader):
        loss = train_step(batch)
        if step % 100 == 0:
            log.info("step=%d loss=%.5f", step, loss)

Write detailed telemetry to an artifact file rather than rendering every event in notebook output.

## 20. Clean-run release test

Before sharing:

1. Save important local results to persistent storage.
2. Restart runtime.
3. Execute all cells in order.
4. Confirm smoke mode completes.
5. Confirm a checkpoint can be reloaded.
6. Confirm no secret appears in source or output.
7. Confirm final artifacts are outside /content.
