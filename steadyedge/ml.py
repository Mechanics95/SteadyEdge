"""ML active sleeve: cross-sectional ranking with gradient-boosted trees.

At each month end t the model predicts which assets will do best over the
next `horizon` trading days, and the sleeve holds the top_n.

Leak guards (all date-based, so tests/test_lookahead.py can verify them):
- Features at t use prices up to and including t only.
- The model is retrained once per calendar year, on the first rebalance day
  of that year, using only rows whose LABEL window ended before t
  (row date <= t - horizon - embargo). That is the purge + embargo.
- Labels are cross-sectional ranks, so the model learns "which asset beats
  the others", not the market's level.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .strategies import _on_rebalance, rebalance_mask, rsi

FEATURES = ["r5", "r21", "r63", "r126", "r252", "vol21", "vol63", "dist200", "rsi14", "mom_12_1"]


def make_features(close: pd.DataFrame) -> dict[str, pd.DataFrame]:
    ret = close.pct_change(fill_method=None)
    f = {
        "r5": close.pct_change(5, fill_method=None),
        "r21": close.pct_change(21, fill_method=None),
        "r63": close.pct_change(63, fill_method=None),
        "r126": close.pct_change(126, fill_method=None),
        "r252": close.pct_change(252, fill_method=None),
        "vol21": ret.rolling(21).std(),
        "vol63": ret.rolling(63).std(),
        "dist200": close / close.rolling(200).mean() - 1,
        "rsi14": pd.DataFrame({c: rsi(close[c], 14) for c in close.columns}),
        "mom_12_1": close.shift(21) / close.shift(252) - 1,
    }
    # Cross-sectional ranks make features comparable across assets and years.
    return {k: v.rank(axis=1, pct=True) for k, v in f.items()}


def make_context(close: pd.DataFrame, assets: list[str], market: str | None,
                 context: list[str]) -> dict[str, pd.DataFrame]:
    """Market-wide signals, the same value for every asset on a date. Trees
    can combine them with asset features ("momentum works less when VIX is
    high"). Built from prices up to t only."""
    out = {}

    def bcast(s: pd.Series) -> pd.DataFrame:
        return pd.DataFrame({a: s for a in assets}, index=close.index)

    if market:
        m = close[market]
        out["mkt_r63"] = bcast(m.pct_change(63, fill_method=None))
        out["mkt_dist200"] = bcast(m / m.rolling(200).mean() - 1)
        out["mkt_vol21"] = bcast(m.pct_change(fill_method=None).rolling(21).std())
    for c in context:
        if c not in close:
            continue
        x = close[c].ffill()
        key = c.strip("^").lower()
        if key in ("vix", "indiavix"):
            out[f"{key}_level"] = bcast(x)
            out[f"{key}_vs_1y"] = bcast(x / x.rolling(252).mean() - 1)
        else:  # interest-rate series quoted in percent
            out[f"{key}_level"] = bcast(x)
            out[f"{key}_chg63"] = bcast(x - x.shift(63))
    return out


def _stack(feats: dict, dates) -> pd.DataFrame:
    cols = {k: v.loc[dates].stack(future_stack=True) for k, v in feats.items()}
    return pd.DataFrame(cols)


def ml_rank(close: pd.DataFrame, top_n: int = 3, horizon: int = 21, embargo: int = 5,
            train_years: int = 5, freq: str = "M", universe: list[str] | None = None,
            min_train_rows: int = 500, seed: int = 0, max_iter: int = 150,
            market: str | None = None, context: list[str] | None = None) -> pd.DataFrame:
    from sklearn.ensemble import HistGradientBoostingRegressor

    px = close[universe] if universe else close
    feats = make_features(px)
    if market or context:
        feats.update(make_context(close, list(px.columns), market, context or []))
    fwd = px.shift(-horizon) / px - 1                     # label: used ONLY for rows purged below
    label = fwd.rank(axis=1, pct=True)
    idx = px.index
    mask = rebalance_mask(idx, freq)
    w = pd.DataFrame(np.nan, index=idx, columns=close.columns)

    model, model_year = None, None
    for i in np.where(mask)[0]:
        t = idx[i]
        if model_year != t.year:
            last_ok = i - horizon - embargo               # label window of this row ends before t
            if last_ok > 0:
                lo = idx.searchsorted(t - pd.DateOffset(years=train_years))
                train_dates = idx[lo:last_ok + 1:5]       # every 5th day: less overlap, faster
                X = _stack(feats, train_dates)
                y = label.loc[train_dates].stack(future_stack=True).reindex(X.index)
                ok = X.notna().all(axis=1) & y.notna()
                if ok.sum() >= min_train_rows:
                    model = HistGradientBoostingRegressor(max_iter=max_iter, learning_rate=0.05,
                                                          max_depth=3, random_state=seed)
                    model.fit(X[ok].to_numpy(), y[ok].to_numpy())
                    model_year = t.year
        if model is None:
            continue
        xt = pd.DataFrame({k: v.loc[t] for k, v in feats.items()})
        ok = xt.notna().all(axis=1)
        if ok.sum() < top_n:
            continue
        pred = pd.Series(model.predict(xt[ok].to_numpy()), index=xt.index[ok])
        row = pd.Series(0.0, index=close.columns)
        row[pred.nlargest(top_n).index] = 1.0 / top_n
        w.loc[t] = row.to_numpy()
    return _on_rebalance(w, freq)
