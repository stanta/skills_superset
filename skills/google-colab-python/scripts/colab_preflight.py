#!/usr/bin/env python3
"""Inspect a Google Colab runtime before starting an expensive job."""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


GIB = 1024 ** 3


def _run(command: list[str], timeout: int = 5) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "returncode": completed.returncode,
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
        }
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"error": f"{type(exc).__name__}: {exc}"}


def _memory_info() -> dict[str, float | None]:
    values: dict[str, int] = {}
    meminfo = Path("/proc/meminfo")
    if meminfo.exists():
        for line in meminfo.read_text(encoding="utf-8").splitlines():
            if ":" not in line:
                continue
            key, raw = line.split(":", 1)
            parts = raw.strip().split()
            if not parts:
                continue
            try:
                values[key] = int(parts[0]) * 1024
            except ValueError:
                continue
    total = values.get("MemTotal")
    available = values.get("MemAvailable")
    return {
        "total_gib": round(total / GIB, 2) if total is not None else None,
        "available_gib": round(available / GIB, 2) if available is not None else None,
    }


def _disk_info(path: Path) -> dict[str, float]:
    usage = shutil.disk_usage(path)
    return {
        "total_gib": round(usage.total / GIB, 2),
        "used_gib": round(usage.used / GIB, 2),
        "free_gib": round(usage.free / GIB, 2),
    }


def _gpu_info() -> dict[str, Any]:
    executable = shutil.which("nvidia-smi")
    if not executable:
        return {"available": False}
    query = _run(
        [
            executable,
            "--query-gpu=name,memory.total,memory.free,driver_version",
            "--format=csv,noheader,nounits",
        ]
    )
    if query.get("returncode") != 0:
        return {"available": False, "diagnostic": query}

    devices = []
    for line in query.get("stdout", "").splitlines():
        parts = [part.strip() for part in line.split(",")]
        if len(parts) != 4:
            continue
        name, total_mb, free_mb, driver = parts
        try:
            total_value = int(total_mb)
            free_value = int(free_mb)
        except ValueError:
            continue
        devices.append(
            {
                "name": name,
                "memory_total_mb": total_value,
                "memory_free_mb": free_value,
                "driver_version": driver,
            }
        )
    return {"available": bool(devices), "devices": devices}


def _package_versions(packages: list[str]) -> dict[str, str | None]:
    if not packages:
        return {}

    from importlib.metadata import PackageNotFoundError, version

    result: dict[str, str | None] = {}
    for package in packages:
        try:
            result[package] = version(package)
        except PackageNotFoundError:
            result[package] = None
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workdir", default="/content")
    parser.add_argument("--min-free-disk-gb", type=float, default=5.0)
    parser.add_argument("--min-available-ram-gb", type=float, default=2.0)
    parser.add_argument("--require-gpu", action="store_true")
    parser.add_argument(
        "--packages",
        nargs="*",
        default=[],
        help="Package names whose installed versions should be reported.",
    )
    args = parser.parse_args()

    workdir = Path(args.workdir)
    if not workdir.exists():
        workdir = Path("/")

    memory = _memory_info()
    disk = _disk_info(workdir)
    gpu = _gpu_info()

    info: dict[str, Any] = {
        "python": {
            "version": platform.python_version(),
            "executable": sys.executable,
            "implementation": platform.python_implementation(),
        },
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "runtime": {
            "workdir": str(workdir),
            "cwd": os.getcwd(),
            "cpu_count": os.cpu_count(),
            "is_colab": "COLAB_RELEASE_TAG" in os.environ
            or Path("/content").exists(),
            "drive_mounted": Path("/content/drive").exists(),
        },
        "memory": memory,
        "disk": disk,
        "gpu": gpu,
        "packages": _package_versions(args.packages),
        "warnings": [],
        "errors": [],
    }

    if disk["free_gib"] < args.min_free_disk_gb:
        info["errors"].append(
            f"Free disk {disk['free_gib']} GiB is below required "
            f"{args.min_free_disk_gb} GiB."
        )

    available_ram = memory.get("available_gib")
    if available_ram is not None and available_ram < args.min_available_ram_gb:
        info["errors"].append(
            f"Available RAM {available_ram} GiB is below required "
            f"{args.min_available_ram_gb} GiB."
        )

    if args.require_gpu and not gpu.get("available"):
        info["errors"].append("GPU was required but no NVIDIA GPU was detected.")

    if not info["runtime"]["drive_mounted"]:
        info["warnings"].append(
            "Google Drive is not mounted. This is fine unless the workflow "
            "expects Drive-backed persistence."
        )

    print(json.dumps(info, indent=2, sort_keys=True))
    return 1 if info["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
