"""End-to-end smoke test on synthetic DaLiA-shaped data: loader -> gate -> spectral -> tables."""
import os, subprocess, sys
import numpy as np, pandas as pd, yaml
from tests.make_synthetic_dalia import write
from heart_rate.dalia import load_all
from heart_rate.spectral import spectral_hr
from common.quality import gate
from common.metrics import mae


def test_spectral_recovers_synthetic_hr(tmp_path):
    cfg = yaml.safe_load(open("configs/hr_dalia.yaml"))
    write(str(tmp_path), n_subjects=2, minutes=3)
    D = load_all(str(tmp_path), ["S1", "S2"], cfg)
    assert D["ppg"].shape[1] == cfg["window_s"] * cfg["fs_ppg"] and D["acc"].shape[1:] == (3, cfg["window_s"] * cfg["fs_acc"])
    ok, _ = gate(D["ppg"], D["acc"], cfg["quality"])
    pred = spectral_hr(D["ppg"], cfg["fs_ppg"], tuple(cfg["bandpass_hz"]), tuple(cfg["hr_range_bpm"]))
    assert mae(D["y"][ok], pred[ok]) < 3.0          # clean windows: within a few bpm
    assert 0.3 < ok.mean() < 1.0                    # the motion burst is rejected, the rest kept


def test_cli_writes_outputs(tmp_path):
    data = tmp_path / "PPG_FieldStudy"; write(str(data), n_subjects=2, minutes=2)
    cfg = yaml.safe_load(open("configs/hr_dalia.yaml")); cfg["data_dir"] = str(data); cfg["subjects"] = ["S1", "S2"]
    cpath = tmp_path / "cfg.yaml"; yaml.safe_dump(cfg, open(cpath, "w"))
    out = tmp_path / "results"
    r = subprocess.run([sys.executable, "-m", "heart_rate.run", "--config", str(cpath), "--method", "spectral", "--out", str(out)],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    df = pd.read_csv(out / "ppg_dalia_spectral_predictions.csv")
    assert {"subject", "activity", "y", "pred", "accepted", "acc_rms_g"} <= set(df.columns)
    assert (out / "ppg_dalia_spectral_summary.md").exists()
