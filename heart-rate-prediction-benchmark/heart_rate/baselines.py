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


def beliefppg_hr(ppg: np.ndarray, acc: np.ndarray | None, fs_ppg: float, fs_acc: float):
    """BeliefPPG on a whole recording (it models the HR sequence, so it takes the continuous
    signal, not pre-cut windows). Returns the package's per-window HR estimates and their
    window timestamps; align to the DaLiA label grid in the caller."""
    try:
        from beliefppg import infer_hr
    except ImportError as e:
        raise ImportError("pip install beliefppg") from e
    # TODO(verify): argument names/order and the returned (hr, time) structure per README.
    return infer_hr(ppg, acc, fs_ppg, fs_acc) if acc is not None else infer_hr(ppg, None, fs_ppg, None)
