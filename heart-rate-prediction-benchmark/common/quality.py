"""Signal-quality gate. Decisions are made before any model sees a window, and the
fraction of accepted windows (coverage) is always reported next to accuracy."""
from __future__ import annotations
import numpy as np


def acc_rms_g(acc_win: np.ndarray) -> np.ndarray:
    """RMS of accelerometer magnitude with the static (gravity) component removed.
    acc_win: (n_windows, 3, n_samples) in g."""
    mag = np.linalg.norm(acc_win, axis=1)
    mag = mag - mag.mean(axis=-1, keepdims=True)
    return np.sqrt((mag ** 2).mean(axis=-1))


def flat_fraction(ppg_win: np.ndarray, tol: float = 1e-6) -> np.ndarray:
    """Fraction of samples whose first difference is ~0 (flatline or clipping)."""
    d = np.abs(np.diff(ppg_win, axis=-1))
    return (d < tol * (np.abs(ppg_win).max(axis=-1, keepdims=True) + 1e-12)).mean(axis=-1)


def amplitude(ppg_win: np.ndarray) -> np.ndarray:
    return ppg_win.max(axis=-1) - ppg_win.min(axis=-1)


def gate(ppg_win: np.ndarray, acc_win: np.ndarray | None, cfg: dict) -> tuple[np.ndarray, dict]:
    """Return (accepted boolean mask, per-window features). All thresholds come from cfg."""
    feats = {"flat_fraction": flat_fraction(ppg_win)}
    amp = amplitude(ppg_win)
    med = np.median(amp) if len(amp) else 1.0
    feats["amp_ratio"] = amp / (med + 1e-12)
    ok = (feats["flat_fraction"] <= cfg["flat_fraction_max"]) \
        & (feats["amp_ratio"] <= cfg["amp_ratio_max"]) & (feats["amp_ratio"] >= cfg["amp_ratio_min"])
    if acc_win is not None:
        feats["acc_rms_g"] = acc_rms_g(acc_win)
        ok &= feats["acc_rms_g"] <= cfg["acc_rms_max_g"]
    return ok, feats
