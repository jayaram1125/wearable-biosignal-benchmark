# ppg_dalia · beliefppg · leave-one-subject-out

Run 2026-11-28T04:18:47Z · commit `0a8d45681144` · subjects 2 · windows 8702
Preliminary, untuned. Protocol as in the PPG Heart-Rate Technical Architecture v0.2. MAE in bpm.

## Overall
|         |    n |   coverage |   mae_all |   mae_accepted |   me_accepted |   sd_accepted |
|:--------|-----:|-----------:|----------:|---------------:|--------------:|--------------:|
| overall | 8702 |      0.764 |     4.082 |          4.098 |         1.106 |         5.348 |

## By activity
| activity     |    n |   coverage |   mae_all |   mae_accepted |   me_accepted |   sd_accepted |
|:-------------|-----:|-----------:|----------:|---------------:|--------------:|--------------:|
| cycling      |  399 |      0.383 |     4.595 |          5.165 |        -0.976 |         6.454 |
| driving      |  904 |      0.959 |     3.69  |          3.684 |         1.144 |         4.604 |
| lunch        | 1788 |      0.987 |     3.821 |          3.789 |         1.466 |         4.689 |
| sitting      |  649 |      0.954 |     3.306 |          3.277 |         1.264 |         4.384 |
| stairs       |  276 |      0.007 |     5.967 |          0.958 |         0.958 |         1.064 |
| table_soccer |  324 |      0.806 |     5.676 |          5.662 |         0.839 |         7.006 |
| transient    | 2401 |      0.66  |     4.361 |          4.711 |         0.761 |         6.144 |
| walking      |  722 |      0.233 |     3.792 |          5.744 |         4.067 |         8.165 |
| working      | 1239 |      0.992 |     3.779 |          3.778 |         0.836 |         4.82  |

## By subject
| subject   |    n |   coverage |   mae_all |   mae_accepted |   me_accepted |   sd_accepted |
|:----------|-----:|-----------:|----------:|---------------:|--------------:|--------------:|
| S1        | 4603 |      0.737 |     4.1   |          4.039 |         1.12  |         5.283 |
| S2        | 4099 |      0.794 |     4.061 |          4.16  |         1.092 |         5.416 |
