"""PPG-DaLiA loader (Reiss et al., 2019). Expects data/PPG_FieldStudy/S<k>/S<k>.pkl as
distributed by the authors (pickle, latin1). Wrist BVP at 64 Hz, wrist ACC at 32 Hz,
ECG-derived heart-rate labels for 8-s windows with 2-s stride, activity labels at 4 Hz."""
from __future__ import annotations
import os, pickle
import numpy as np
from common.signal import make_windows


def load_subject(data_dir: str, subject: str, cfg: dict) -> dict:
    npz = os.path.join(data_dir, subject, f"{subject}.npz")
    if os.path.exists(npz):                                            # compact form from prepare_dalia
        z = np.load(npz)
        bvp, acc, y, act = z["bvp"].astype(float), z["acc"].astype(float), z["label"].astype(float), z["activity"].astype(float)
    else:                                                              # original pickle
        with open(os.path.join(data_dir, subject, f"{subject}.pkl"), "rb") as f:
            d = pickle.load(f, encoding="latin1")
        bvp = np.asarray(d["signal"]["wrist"]["BVP"], dtype=float).reshape(-1)
        acc = np.asarray(d["signal"]["wrist"]["ACC"], dtype=float)    # (n, 3) in g
        y = np.asarray(d["label"], dtype=float).reshape(-1)           # one HR per window
        act = np.asarray(d["activity"], dtype=float).reshape(-1)
    n = len(y)
    ppg_win = make_windows(bvp, cfg["fs_ppg"], cfg["window_s"], cfg["stride_s"], n)
    acc_win = np.stack([make_windows(acc[:, k], cfg["fs_acc"], cfg["window_s"], cfg["stride_s"], n) for k in range(3)], axis=1)
    n = min(len(ppg_win), len(acc_win), n)
    # activity per window: mode of the 4 Hz activity labels inside the window
    fa, w, s = cfg["fs_activity"], cfg["window_s"], cfg["stride_s"]
    act_win = np.array([np.bincount(act[int(i * s * fa): int(i * s * fa + w * fa)].astype(int)).argmax()
                        if len(act[int(i * s * fa): int(i * s * fa + w * fa)]) else 0 for i in range(n)])
    return {"subject": subject, "ppg": ppg_win[:n], "acc": acc_win[:n], "y": y[:n], "activity": act_win}


def load_all(data_dir: str, subjects: list[str], cfg: dict) -> dict:
    parts = [load_subject(data_dir, s, cfg) for s in subjects]
    return {
        "ppg": np.concatenate([p["ppg"] for p in parts]),
        "acc": np.concatenate([p["acc"] for p in parts]),
        "y": np.concatenate([p["y"] for p in parts]),
        "activity": np.concatenate([p["activity"] for p in parts]),
        "subject": np.concatenate([[p["subject"]] * len(p["y"]) for p in parts]),
    }
