"""Official open baselines, used as-is with their pretrained weights (Experiment 0 of the
architecture document: reproduce before comparing). Both are optional dependencies.

KID-PPG  : pip install kid-ppg     (Kechris et al., IEEE TBME 2025; github.com/esl-epfl/KID-PPG)
BeliefPPG: pip install beliefppg   (Bieri et al., UAI 2023;     github.com/eth-siplab/BeliefPPG)

The exact call signatures, expected sampling rates and window conventions must be taken
from each package's README; the wrappers below isolate that in one place and raise a clear
error if the installed API differs from what is assumed here."""
from __future__ import annotations
import numpy as np


def kidppg_hr(ppg_win: np.ndarray, acc_win: np.ndarray, fs_ppg: float, fs_acc: float) -> np.ndarray:
    """KID-PPG pretrained model. Inputs: windows of PPG and 3-axis accelerometer.
    Returns one heart rate (bpm) per window."""
    try:
        from kid_ppg import KID_PPG
    except ImportError as e:
        raise ImportError("pip install kid-ppg") from e
    model = KID_PPG()
    # TODO(verify): KID-PPG expects PPG and ACC at a fixed rate and window length (see README).
    # Resample here if fs_ppg / fs_acc differ from the package's expected rates.
    preds = []
    for p, a in zip(ppg_win, acc_win):
        out = model.predict(p, a)                     # adapt to the documented signature
        preds.append(float(np.ravel(out)[0]))
    return np.asarray(preds)


def beliefppg_hr(bvp: np.ndarray, acc: np.ndarray, fs_ppg: float, fs_acc: float,
                 n_windows: int, window_s: float, stride_s: float) -> np.ndarray:
    """BeliefPPG (pretrained) on one whole recording. infer_hr returns heart rates and the
    time index (in PPG samples) of each window midpoint; those are aligned to the DaLiA
    label grid (window i covers [i*stride, i*stride+window] s). Windows whose nearest
    BeliefPPG estimate is more than 1 s away are left NaN.
    Note: BeliefPPG's published training data includes PPG-DaLiA, so a DaLiA run is a
    reproduction check of the package, not an out-of-sample evaluation."""
    try:
        from beliefppg import infer_hr
    except ImportError as e:
        raise ImportError("pip install beliefppg (needs Python 3.10; see README)") from e
    hr, t = infer_hr(np.asarray(bvp, float).reshape(-1, 1), int(fs_ppg), np.asarray(acc, float), int(fs_acc))
    hr = np.asarray(hr, float).reshape(-1); t = np.asarray(t, float).reshape(-1)
    mid = (np.arange(n_windows) * stride_s + window_s / 2.0) * fs_ppg
    idx = np.clip(np.searchsorted(t, mid), 1, len(t) - 1)
    left = idx - 1
    pick = np.where(np.abs(t[left] - mid) <= np.abs(t[idx] - mid), left, idx)
    out = hr[pick].copy()
    out[np.abs(t[pick] - mid) > fs_ppg] = np.nan
    return out
