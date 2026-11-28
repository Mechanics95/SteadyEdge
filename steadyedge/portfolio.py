"""Combine a stable sleeve and an active sleeve, and walk-forward selection.

Sleeves are combined at the weight level and run through the engine as one
account, so the costs of moving money between sleeves are charged for real.
Allocation rules only use sleeve returns observed up to the decision date.
"""
from __future__ import annotations

import itertools
import math

import numpy as np
import pandas as pd

from .engine import run_backtest
from .metrics import TRADING_DAYS, sharpe
from .strategies import rebalance_mask


def allocation_series(rule: str, index: pd.DatetimeIndex, active_returns: pd.Series | None = None,
                      stable_share: float = 0.8, target_vol: float = 0.15, max_active: float = 0.5,
                      dd_limit: float = -0.15, freq: str = "M") -> pd.Series:
    """Fraction of capital in the STABLE sleeve on each decision date (NaN = keep)."""
    mask = rebalance_mask(index, freq)
    if rule == "fixed":
        a = pd.Series(stable_share, index=index)
    elif rule == "vol_target":
        vol = active_returns.rolling(63, min_periods=42).std() * math.sqrt(TRADING_DAYS)
        active = (target_vol / vol).clip(upper=max_active).fillna(1 - stable_share)
        a = 1 - active
    elif rule == "drawdown_throttle":
        eq = (1 + active_returns).cumprod()
        dd = eq / eq.cummax() - 1
        base_active = 1 - stable_share
        active = pd.Series(np.where(dd < dd_limit, base_active / 2, base_active), index=index)
        a = 1 - active
    else:
        raise ValueError(rule)
    a = a.reindex(index)
    a[~mask] = np.nan
    return a


def combine_sleeves(w_stable: pd.DataFrame, w_active: pd.DataFrame, stable_frac: pd.Series) -> pd.DataFrame:
    cols = w_stable.columns.union(w_active.columns)
    ws = w_stable.reindex(columns=cols).ffill()
    wa = w_active.reindex(columns=cols).ffill()
    a = stable_frac.ffill()
    decide = w_stable.notna().any(axis=1) | w_active.notna().any(axis=1) | stable_frac.notna()
    ready = ws.notna().any(axis=1) & wa.notna().any(axis=1) & a.notna()
    combo = ws.fillna(0).mul(a, axis=0) + wa.fillna(0).mul(1 - a, axis=0)
    combo[~(decide & ready)] = np.nan
    return combo


def grid(param_grid: dict) -> list[dict]:
    keys = list(param_grid)
    return [dict(zip(keys, vals)) for vals in itertools.product(*param_grid.values())]


def walk_forward(make_weights, param_grid: dict, open_: pd.DataFrame, close: pd.DataFrame,
                 cost_model, capital: float, fractional: bool, train_years: int = 5,
                 test_years: int = 1, warmup_days: int = 260, min_trade_frac: float = 0.0) -> dict:
    """Rolling walk-forward. For each test window, pick the params with the
    best Sharpe on the preceding train window only, then trade the test
    window with them. Returns stitched out-of-sample weights plus the log of
    choices. Every param combination evaluated counts as a trial."""
    combos = grid(param_grid)
    all_w = {i: make_weights(close, **p) for i, p in enumerate(combos)}
    # Each combo's full-history run; slicing a run by date is safe because the
    # strategies are causal (verified by tests/test_lookahead.py).
    runs = {i: run_backtest(open_, close, w, cost_model, capital, fractional,
                            min_trade_frac=min_trade_frac).returns
            for i, w in all_w.items()}
    idx = close.index
    start = idx[0] + pd.Timedelta(days=int(warmup_days * 365 / 252))
    folds, stitched = [], pd.DataFrame(np.nan, index=idx, columns=close.columns)
    t0 = start
    while True:
        train_end = t0 + pd.DateOffset(years=train_years)
        test_end = train_end + pd.DateOffset(years=test_years)
        if train_end >= idx[-1]:
            break
        tr = (idx >= t0) & (idx < train_end)
        te = (idx >= train_end) & (idx < test_end)
        scores = {i: sharpe(r[tr]) for i, r in runs.items()}
        best = max(scores, key=scores.get)
        w = all_w[best]
        stitched.loc[te] = w.loc[te].to_numpy()
        # Force a rebalance on the first test day so the new params take over.
        first = np.argmax(te)
        filled = w.ffill().iloc[first]
        if filled.notna().any():
            stitched.iloc[first] = filled.to_numpy()
        folds.append({"train": f"{t0.date()}..{train_end.date()}",
                      "test": f"{train_end.date()}..{min(test_end, idx[-1]).date()}",
                      "chosen": combos[best], "train_sharpe": round(scores[best], 3)})
        t0 = t0 + pd.DateOffset(years=test_years)
    trial_sharpes = [sharpe(r) for r in runs.values()]
    return {"weights": stitched, "folds": folds, "n_trials": len(combos),
            "trial_sharpes": trial_sharpes, "oos_start": folds[0]["test"].split("..")[0] if folds else None}
