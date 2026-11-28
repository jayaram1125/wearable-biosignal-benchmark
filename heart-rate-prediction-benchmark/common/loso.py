"""Leave-one-subject-out evaluation. No subject ever contributes to both sides of a fold."""
from __future__ import annotations
import numpy as np


def loso(X: np.ndarray, y: np.ndarray, groups: np.ndarray, fit, predict) -> np.ndarray:
    preds = np.full(len(y), np.nan)
    for s in np.unique(groups):
        tr, te = groups != s, groups == s
        if tr.sum() == 0:
            continue
        model = fit(X[tr], y[tr])
        preds[te] = predict(model, X[te])
    return preds


def ridge_fit(alpha: float = 1.0):
    from sklearn.linear_model import Ridge
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    def fit(X, y):
        return make_pipeline(StandardScaler(), Ridge(alpha=alpha)).fit(X, y)
    return fit


def ridge_predict(model, X):
    return model.predict(X)


def mean_fit(X, y):
    return float(np.mean(y))


def mean_predict(model, X):
    return np.full(len(X), model)
