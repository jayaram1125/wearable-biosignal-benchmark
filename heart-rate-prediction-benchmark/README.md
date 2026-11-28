
## Results · PPG-DaLiA · 15 subjects · 64,697 windows (8 s / 2 s)

Gate: accelerometer RMS ≤ 0.25 g (gravity removed) plus flatline and amplitude checks, set from the
dataset's motion scale, not from error. Coverage is the fraction of windows the gate accepts.
MAE in bpm against the ECG-derived label. Full tables, per-activity and per-subject, in `results/`.

| Method | Protocol | MAE all | MAE accepted | Coverage |
|---|---|---:|---:|---:|
| Spectral peak (no learning) | leave-one-subject-out | 17.77 | 14.58 | 0.78 |
| BeliefPPG, pretrained package | reproduction check; DaLiA is in its training data | 4.26 | 4.16 | 0.78 |

Published BeliefPPG figure on PPG-DaLiA: 4.26 bpm. Reproduced to within 0.01 bpm (Experiment 0 of the
architecture document: calibrate the framework against published numbers before comparing anything new).

Gate sweep, spectral method (`results/ppg_dalia_spectral_gate_sweep.md`): MAE on accepted windows
ranges from 5.9 bpm at 34 % coverage to 17.8 bpm at 99 % coverage. The trade-off is reported, not hidden.

Two observations the design predicted:
- Cycling and table soccer have low wrist acceleration but corrupted PPG; the accelerometer gate passes
  them and the spectral error stays above 24 bpm. Motion gating alone is insufficient; PPG-based quality
  features are required.
- The plain spectral estimator is biased low (sub-harmonic and motion peaks); this is what the processing
  candidates and learned models are for.

Not yet run: KID-PPG (PyPI release has an unsatisfiable dependency pin; see issues), PaPaGei linear
probe, processing candidates SP2–SP7, IEEE SPC 2015, WildPPG. Nothing here is tuned. No comparison to
any commercial device is made or implied.

## Results · PPG-DaLiA · 15 subjects · 64,697 windows (8 s / 2 s)

Gate: accelerometer RMS ≤ 0.25 g (gravity removed) plus flatline and amplitude checks, set from the
dataset's motion scale, not from error. Coverage is the fraction of windows the gate accepts.
MAE in bpm against the ECG-derived label. Full tables, per-activity and per-subject, in `results/`.

| Method | Protocol | MAE all | MAE accepted | Coverage |
|---|---|---:|---:|---:|
| Spectral peak (no learning) | leave-one-subject-out | 17.77 | 14.58 | 0.78 |
| BeliefPPG, pretrained package | reproduction check; DaLiA is in its training data | 4.26 | 4.16 | 0.78 |

Published BeliefPPG figure on PPG-DaLiA: 4.26 bpm. Reproduced to within 0.01 bpm (Experiment 0 of the
architecture document: calibrate the framework against published numbers before comparing anything new).

Gate sweep, spectral method (`results/ppg_dalia_spectral_gate_sweep.md`): MAE on accepted windows
ranges from 5.9 bpm at 34 % coverage to 17.8 bpm at 99 % coverage. The trade-off is reported, not hidden.

Two observations the design predicted:
- Cycling and table soccer have low wrist acceleration but corrupted PPG; the accelerometer gate passes
  them and the spectral error stays above 24 bpm. Motion gating alone is insufficient; PPG-based quality
  features are required.
- The plain spectral estimator is biased low (sub-harmonic and motion peaks); this is what the processing
  candidates and learned models are for.

Not yet run: KID-PPG (PyPI release has an unsatisfiable dependency pin; see issues), PaPaGei linear
probe, processing candidates SP2–SP7, IEEE SPC 2015, WildPPG. Nothing here is tuned. No comparison to
any commercial device is made or implied.
