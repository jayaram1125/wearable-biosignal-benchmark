"""Convert PPG-DaLiA subject pickles (~1.5 GB each, mostly unused 700 Hz chest channels)
into compact .npz files holding only wrist BVP (64 Hz), wrist ACC (32 Hz), the ECG-derived
heart-rate labels and the 4 Hz activity labels. Extracts one subject at a time from data.zip
and deletes the pickle afterwards, so the full dataset needs ~150 MB, not ~23 GB.
    python -m heart_rate.prepare_dalia --zip datasets/data.zip --out datasets/PPG_FieldStudy
"""
from __future__ import annotations
import argparse, os, pickle, subprocess
import numpy as np


def convert(pkl_path: str, npz_path: str) -> None:
    with open(pkl_path, "rb") as f:
        d = pickle.load(f, encoding="latin1")
    np.savez_compressed(
        npz_path,
        bvp=np.asarray(d["signal"]["wrist"]["BVP"], dtype=np.float32).reshape(-1),
        acc=np.asarray(d["signal"]["wrist"]["ACC"], dtype=np.float32),
        label=np.asarray(d["label"], dtype=np.float32).reshape(-1),
        activity=np.asarray(d["activity"], dtype=np.int8).reshape(-1),
    )


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", default="datasets/data.zip")
    ap.add_argument("--out", default="datasets/PPG_FieldStudy")
    ap.add_argument("--subjects", default=",".join(f"S{i}" for i in range(1, 16)))
    a = ap.parse_args(argv)
    os.makedirs(a.out, exist_ok=True)
    for s in a.subjects.split(","):
        npz = os.path.join(a.out, s, f"{s}.npz"); pkl = os.path.join(a.out, s, f"{s}.pkl")
        if os.path.exists(npz):
            print(s, "already converted"); continue
        if not os.path.exists(pkl):
            subprocess.run(["unzip", "-q", "-o", a.zip, f"PPG_FieldStudy/{s}/{s}.pkl", "-d", os.path.dirname(a.out)], check=True)
        convert(pkl, npz); os.remove(pkl)
        print(s, "->", npz, f"{os.path.getsize(npz) / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
