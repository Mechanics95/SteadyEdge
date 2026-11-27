"""Baseline strategies.

Every strategy is a pure function of prices up to and including date t and
returns target weights dated t (the engine executes them at t+1's open).
tests/test_lookahead.py checks each one for leaks by truncating the data.

Rows on non-rebalance days are NaN, meaning "hold".
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def rebalance_mask(index: pd.DatetimeIndex, freq: str) -> np.ndarray:
    """True on the last trading day of each period.

    Decided from the date itself plus the calendar, never from the existence
    of a future row, so truncating data cannot change past decisions. 'D' =
    every day, 'W' = Fridays (or last day of week seen), 'M' = month end.
    """
    if freq == "D":
        return np.ones(len(index), dtype=bool)
    s = pd.Series(index, index=index)
    if freq == "W":
        key = index.to_period("W-FRI")
    elif freq == "M":
        key = index.to_period("M")
    elif freq == "Q":
        key = index.to_period("Q")
    else:
        raise ValueError(freq)
    # A row is a rebalance day if the next *calendar business day* falls in a
    # new period. This uses the calendar, not future data.
    nxt = (index + pd.offsets.BDay(1))
    if freq == "W":
        nkey = nxt.to_period("W-FRI")
    elif freq == "M":
        nkey = nxt.to_period("M")
    else:
        nkey = nxt.to_period("Q")
    return np.asarray(key != nkey)


def _on_rebalance(weights: pd.DataFrame, freq: str) -> pd.DataFrame:
    mask = rebalance_mask(weights.index, freq)
    out = weights.copy()
    out.loc[~mask] = np.nan
    return out


def buy_and_hold(close: pd.DataFrame, weights: dict | None = None, freq: str = "Q") -> pd.DataFrame:
    """Fixed weights, rebalanced each period. Default: equal weight."""
    cols = close.columns
    w = pd.Series(weights if weights else {c: 1 / len(cols) for c in cols}).reindex(cols).fillna(0)
    avail = close.notna()
    raw = avail.mul(w, axis=1)
    raw = raw.div(raw.sum(axis=1).where(lambda s: s > 0), axis=0) * w.sum()
    return _on_rebalance(raw, freq)


def trend_filter(close: pd.DataFrame, asset: str, window: int = 200, freq: str = "W",
                 off_asset: str | None = None) -> pd.DataFrame:
    """Hold `asset` while it is above its N-day average, else cash / off_asset."""
    px = close[asset]
    on = (px > px.rolling(window, min_periods=window).mean()).astype(float)
    on[px.rolling(window, min_periods=window).mean().isna()] = np.nan
    w = pd.DataFrame(0.0, index=close.index, columns=close.columns)
    w[asset] = on
    if off_asset:
        w[off_asset] = 1 - on
    w[on.isna()] = np.nan
    return _on_rebalance(w, freq)


def momentum(close: pd.DataFrame, lookback: int = 252, skip: int = 21, top_n: int = 3,
             freq: str = "M", universe: list[str] | None = None,
             abs_filter: bool = True) -> pd.DataFrame:
    """Cross-sectional momentum: hold the top_n by return from t-lookback to
    t-skip, equal weight. abs_filter drops names with negative momentum
    (their slot goes to cash)."""
    px = close[universe] if universe else close
    mom = px.shift(skip) / px.shift(lookback) - 1
    ranks = mom.rank(axis=1, ascending=False, method="first")
    pick = (ranks <= top_n) & mom.notna()
    if abs_filter:
        pick &= mom > 0
    w = pick.astype(float) / top_n
    w = w.reindex(columns=close.columns, fill_value=0.0)
    w[mom.notna().sum(axis=1) < top_n] = np.nan
    return _on_rebalance(w, freq)


def rsi(px: pd.Series, n: int = 14) -> pd.Series:
    d = px.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    return 100 - 100 / (1 + up / dn)


def rsi_reversion(close: pd.DataFrame, n: int = 2, entry: float = 10, exit_: float = 70,
                  trend_window: int = 200, universe: list[str] | None = None,
                  max_positions: int = 3) -> pd.DataFrame:
    """Short-term mean reversion: buy oversold names in an uptrend, exit on
    rebound. Decisions daily."""
    cols = universe or list(close.columns)
    w = pd.DataFrame(0.0, index=close.index, columns=close.columns)
    held = pd.DataFrame(False, index=close.index, columns=cols)
    r = pd.DataFrame({c: rsi(close[c], n) for c in cols})
    trend = close[cols] > close[cols].rolling(trend_window, min_periods=trend_window).mean()
    state = pd.Series(False, index=cols)
    for i, d in enumerate(close.index):
        ri, ti = r.iloc[i], trend.iloc[i]
        state = (state & ~(ri > exit_)) | ((ri < entry) & ti)
        state = state.fillna(False).astype(bool)
        if state.sum() > max_positions:
            keep = ri[state].nsmallest(max_positions).index
            state = state & state.index.isin(keep)
        held.iloc[i] = state.to_numpy()
    w[cols] = held.astype(float) / max_positions
    return w


STRATEGIES = {
    "buy_and_hold": buy_and_hold,
    "trend_filter": trend_filter,
    "momentum": momentum,
    "rsi_reversion": rsi_reversion,
}
