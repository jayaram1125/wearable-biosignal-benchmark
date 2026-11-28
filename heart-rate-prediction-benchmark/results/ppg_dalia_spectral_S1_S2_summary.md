# ppg_dalia · spectral · leave-one-subject-out

Run 2026-11-28T03:42:25Z · commit `8ce87b872f43` · subjects 2 · windows 8702
Preliminary, untuned. Protocol as in the PPG Heart-Rate Technical Architecture v0.2. MAE in bpm.

## Overall
|         |    n |   coverage |   mae_all |   mae_accepted |   me_accepted |   sd_accepted |
|:--------|-----:|-----------:|----------:|---------------:|--------------:|--------------:|
| overall | 8702 |      0.764 |    12.825 |          9.834 |        -5.717 |        16.468 |

## By activity
| activity     |    n |   coverage |   mae_all |   mae_accepted |   me_accepted |   sd_accepted |
|:-------------|-----:|-----------:|----------:|---------------:|--------------:|--------------:|
| cycling      |  399 |      0.383 |    24.583 |         27.449 |       -24.269 |        30.651 |
| driving      |  904 |      0.959 |     8.112 |          7.855 |        -4.267 |        12.559 |
| lunch        | 1788 |      0.987 |     8.299 |          8.133 |        -3.273 |        12.948 |
| sitting      |  649 |      0.954 |     3.834 |          3.421 |        -1.488 |         7.314 |
| stairs       |  276 |      0.007 |    38.109 |         36.9   |       -36.9   |        39.688 |
| table_soccer |  324 |      0.806 |    23.963 |         25.681 |       -22.718 |        20.346 |
| transient    | 2401 |      0.66  |    15.557 |         12.921 |        -7.494 |        20.026 |
| walking      |  722 |      0.233 |    18.075 |         14.089 |       -10.59  |        20.238 |
| working      | 1239 |      0.992 |     6.817 |          6.74  |        -3.453 |        13.176 |

## By subject
| subject   |    n |   coverage |   mae_all |   mae_accepted |   me_accepted |   sd_accepted |
|:----------|-----:|-----------:|----------:|---------------:|--------------:|--------------:|
| S1        | 4603 |      0.737 |    11.853 |          8.111 |        -4.772 |        13.412 |
| S2        | 4099 |      0.794 |    13.915 |         11.63  |        -6.702 |        19.093 |
