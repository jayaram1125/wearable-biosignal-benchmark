"""Classical reference estimator: band-pass, Welch spectrum, peak in the heart-rate band."""
from __future__ import annotations
import numpy as np
from scipy import signal as sps
from common.signal import bandpass


def spectral_hr(ppg_win: np.ndarray, fs: float, band=(0.5, 3.5), hr_range=(30, 210), nfft: int = 4096) -> np.ndarray:
    x = bandpass(ppg_win, fs, band[0], band[1])
    f, pxx = sps.welch(x, fs=fs, nperseg=x.shape[-1], nfft=nfft, axis=-1)
    lo, hi = hr_range[0] / 60.0, hr_range[1] / 60.0
    m = (f >= lo) & (f <= hi)
    peak = f[m][np.argmax(pxx[..., m], axis=-1)]
    return peak * 60.0
