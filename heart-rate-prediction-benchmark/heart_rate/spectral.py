"""Classical reference estimator: band-pass, Welch spectrum, peak in the heart-rate band."""
from __future__ import annotations
import numpy as np
from scipy import signal as sps
from common.signal import bandpass


def spectral_hr(ppg_win: np.ndarray, fs: float, band=(0.5, 3.5), hr_range=(30, 210), nfft: int = 4096, chunk: int = 2048) -> np.ndarray:
    """Processed in chunks of `chunk` windows to keep memory flat on large datasets."""
    lo, hi = hr_range[0] / 60.0, hr_range[1] / 60.0
    out = np.empty(len(ppg_win))
    for i in range(0, len(ppg_win), chunk):
        x = bandpass(ppg_win[i:i + chunk], fs, band[0], band[1])
        f, pxx = sps.welch(x, fs=fs, nperseg=x.shape[-1], nfft=nfft, axis=-1)
        m = (f >= lo) & (f <= hi)
        out[i:i + chunk] = f[m][np.argmax(pxx[..., m], axis=-1)] * 60.0
    return out
