"""Shared signal processing. Every function is pure and deterministic."""
from __future__ import annotations
import numpy as np
from scipy import signal as sps


def bandpass(x: np.ndarray, fs: float, lo: float, hi: float, order: int = 4) -> np.ndarray:
    """Zero-phase Butterworth band-pass along the last axis."""
    sos = sps.butter(order, [lo, hi], btype="bandpass", fs=fs, output="sos")
    return sps.sosfiltfilt(sos, x, axis=-1)


def resample(x: np.ndarray, fs_in: float, fs_out: float) -> np.ndarray:
    """Polyphase resampling along the last axis (exact for rational ratios)."""
    if fs_in == fs_out:
        return np.asarray(x, dtype=float)
    from fractions import Fraction
    fr = Fraction(fs_out / fs_in).limit_denominator(1000)
    return sps.resample_poly(np.asarray(x, dtype=float), fr.numerator, fr.denominator, axis=-1)


def zscore(x: np.ndarray, eps: float = 1e-8) -> np.ndarray:
    """Per-window standardisation along the last axis."""
    m = x.mean(axis=-1, keepdims=True)
    s = x.std(axis=-1, keepdims=True)
    return (x - m) / (s + eps)


def window_starts(n_samples: int, fs: float, window_s: float, stride_s: float) -> np.ndarray:
    """Start indices of fixed windows covering a signal of n_samples."""
    w, s = int(round(window_s * fs)), int(round(stride_s * fs))
    if n_samples < w:
        return np.zeros(0, dtype=int)
    return np.arange(0, n_samples - w + 1, s, dtype=int)


def make_windows(x: np.ndarray, fs: float, window_s: float, stride_s: float, n_windows: int | None = None) -> np.ndarray:
    """Slice a 1-D signal into (n_windows, window_len). If n_windows is given, truncate or
    verify the count so that windows align with an external label sequence."""
    w = int(round(window_s * fs))
    starts = window_starts(len(x), fs, window_s, stride_s)
    if n_windows is not None:
        starts = starts[:n_windows]
    return np.stack([x[s:s + w] for s in starts]) if len(starts) else np.zeros((0, w))
