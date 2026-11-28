"""Synthetic PPG-DaLiA-shaped subjects for tests and CI smoke runs. Not real data.
Each subject: 64 Hz PPG = sinusoid at a slowly varying heart rate + noise; 32 Hz ACC with
occasional motion bursts; labels = true HR per 8-s window at 2-s stride; activity at 4 Hz."""
import os, pickle, sys
import numpy as np


def make_subject(seed: int, minutes: float = 4.0):
    rng = np.random.default_rng(seed)
    fs, fa, fact = 64, 32, 4
    n = int(minutes * 60 * fs)
    t = np.arange(n) / fs
    hr = 70 + 25 * np.sin(2 * np.pi * t / 120.0) + rng.normal(0, 1, n).cumsum() * 0.01
    phase = np.cumsum(hr / 60.0 / fs) * 2 * np.pi
    ppg = np.sin(phase) + 0.3 * np.sin(2 * phase) + 0.05 * rng.normal(size=n)
    acc = np.tile([0.0, 0.0, 1.0], (int(minutes * 60 * fa), 1)) + 0.02 * rng.normal(size=(int(minutes * 60 * fa), 3))
    act = np.ones(int(minutes * 60 * fact))
    # one motion burst in the middle third: corrupt PPG, raise ACC, label activity 7 (walking)
    a0, a1 = int(n * 0.4), int(n * 0.6)
    ppg[a0:a1] += 2.0 * np.sin(2 * np.pi * 2.2 * t[a0:a1]) + 0.5 * rng.normal(size=a1 - a0)
    acc[int(a0 / 2):int(a1 / 2)] += 2.5 * rng.normal(size=(int(a1 / 2) - int(a0 / 2), 3))
    act[int(a0 / 16):int(a1 / 16)] = 7
    starts = np.arange(0, n - 8 * fs + 1, 2 * fs)
    label = np.array([hr[s:s + 8 * fs].mean() for s in starts])
    return {"signal": {"wrist": {"BVP": ppg.reshape(-1, 1), "ACC": acc}}, "label": label, "activity": act, "subject": f"S{seed}"}


def write(data_dir: str, n_subjects: int = 3, minutes: float = 4.0):
    for k in range(1, n_subjects + 1):
        d = os.path.join(data_dir, f"S{k}"); os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, f"S{k}.pkl"), "wb") as f:
            pickle.dump(make_subject(k, minutes), f)


if __name__ == "__main__":
    write(sys.argv[1] if len(sys.argv) > 1 else "data/PPG_FieldStudy", 3)
