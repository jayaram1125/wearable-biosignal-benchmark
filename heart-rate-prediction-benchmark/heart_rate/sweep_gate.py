"""Coverage versus accuracy at a range of accelerometer thresholds, computed from a saved
predictions file. Shows the trade-off the gate makes instead of hiding it behind one number.
    python -m heart_rate.sweep_gate results/ppg_dalia_spectral_S1_S2_predictions.csv"""
import sys
import numpy as np, pandas as pd
from common.metrics import mae

d = pd.read_csv(sys.argv[1])
base = (d.flat_fraction <= 0.2) & (d.amp_ratio.between(0.1, 5.0))
rows = []
for thr in [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.75, 1.0, 1.5]:
    ok = base & (d.acc_rms_g <= thr)
    rows.append({"acc_rms_max_g": thr, "coverage": round(ok.mean(), 3), "mae_accepted": round(mae(d.y[ok], d.pred[ok]), 2)})
t = pd.DataFrame(rows)
print(t.to_markdown(index=False))
open(sys.argv[1].replace("_predictions.csv", "_gate_sweep.md"), "w").write(t.to_markdown(index=False) + "\n")