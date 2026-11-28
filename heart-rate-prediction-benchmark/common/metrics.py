"""Metrics reported in every results table."""
from __future__ import annotations
import numpy as np
import pandas as pd


def mae(y, p):
    y, p = np.asarray(y, float), np.asarray(p, float)
    m = ~np.isnan(p)
    return float(np.abs(y[m] - p[m]).mean()) if m.any() else float("nan")


def me_sd(y, p):
    y, p = np.asarray(y, float), np.asarray(p, float)
    m = ~np.isnan(p)
    e = p[m] - y[m]
    return (float(e.mean()), float(e.std(ddof=1))) if m.sum() > 1 else (float("nan"), float("nan"))


def summarise(df: pd.DataFrame, pred_col: str, by: str | None = None) -> pd.DataFrame:
    """df needs columns y, accepted, and pred_col. Reports MAE on all windows, MAE on
    accepted windows, coverage and n, overall or grouped by `by`."""
    def one(g):
        acc = g[g.accepted]
        me, sd = me_sd(acc.y, acc[pred_col])
        return pd.Series({
            "n": len(g), "coverage": float(g.accepted.mean()) if len(g) else float("nan"),
            "mae_all": mae(g.y, g[pred_col]), "mae_accepted": mae(acc.y, acc[pred_col]),
            "me_accepted": me, "sd_accepted": sd,
        })
    if by is None:
        return one(df).to_frame("overall").T
    return df.groupby(by, sort=True).apply(one, include_groups=False)
