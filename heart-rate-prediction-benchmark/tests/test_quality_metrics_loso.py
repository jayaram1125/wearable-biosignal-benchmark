import numpy as np, pandas as pd
from common.quality import gate, acc_rms_g
from common.metrics import mae, me_sd, summarise
from common.loso import loso, ridge_fit, ridge_predict, mean_fit, mean_predict

CFG = {"acc_rms_max_g": 1.5, "flat_fraction_max": 0.2, "amp_ratio_max": 5.0, "amp_ratio_min": 0.1}


def test_gate_rejects_motion_flat_and_amplitude_outliers():
    rng = np.random.default_rng(0)
    t = np.arange(512) / 64
    clean = np.sin(2 * np.pi * 1.1 * t)
    ppg = np.stack([clean, clean, np.zeros(512), clean * 50, clean])
    acc = np.tile([0, 0, 1.0], (5, 512 // 2, 1)).transpose(0, 2, 1) + 0.01 * rng.normal(size=(5, 3, 256))
    acc[1] += 3.0 * rng.normal(size=(3, 256))      # motion burst
    ok, feats = gate(ppg, acc, CFG)
    assert ok.tolist() == [True, False, False, False, True]
    assert acc_rms_g(acc)[1] > CFG["acc_rms_max_g"]


def test_metrics_and_summarise():
    y = np.array([60, 70, 80, 90.0]); p = np.array([62, 68, np.nan, 95.0])
    assert abs(mae(y, p) - (2 + 2 + 5) / 3) < 1e-9
    m, s = me_sd(y, p); assert abs(m - 5 / 3) < 1e-9
    df = pd.DataFrame({"y": y, "pred": p, "accepted": [True, True, True, False], "activity": ["a", "a", "b", "b"]})
    out = summarise(df, "pred", by="activity")
    assert out.loc["a", "coverage"] == 1.0 and out.loc["b", "coverage"] == 0.5
    assert abs(out.loc["a", "mae_accepted"] - 2.0) < 1e-9


def test_loso_never_sees_test_subject():
    rng = np.random.default_rng(1)
    X = rng.normal(size=(60, 4)); w = np.array([1.0, -2.0, 0.5, 0.0]); y = X @ w + 50
    g = np.repeat(["S1", "S2", "S3"], 20)
    p = loso(X, y, g, ridge_fit(1e-3), ridge_predict)
    assert mae(y, p) < 0.5                         # linear target is recoverable from other subjects
    pm = loso(X, y, g, mean_fit, mean_predict)
    for s in np.unique(g):                         # mean predictor equals the mean of the OTHER subjects
        assert abs(pm[g == s][0] - y[g != s].mean()) < 1e-9
