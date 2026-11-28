"""Every run writes its config, git hash, timestamp and package versions next to its results."""
from __future__ import annotations
import json, os, platform, subprocess, sys, time


def git_hash() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return "unknown"


def write_log(path: str, cfg: dict, extra: dict | None = None) -> dict:
    import numpy, scipy, sklearn
    log = {
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "git_hash": git_hash(), "python": sys.version.split()[0], "platform": platform.platform(),
        "numpy": numpy.__version__, "scipy": scipy.__version__, "sklearn": sklearn.__version__,
        "config": cfg, **(extra or {}),
    }
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w") as f:
        json.dump(log, f, indent=2, default=str)
    return log
