"""Leak detector: a causal strategy's decision on day t must not change when
we delete all data after t. Run against every strategy, and against a
deliberately cheating strategy to prove the detector works."""
import numpy as np
import pandas as pd
import pytest
from steadyedge.data import synthetic
from steadyedge.strategies import buy_and_hold, momentum, rsi_reversion, trend_filter

CLOSE = synthetic(n_assets=5, years=4, seed=3)["close"]
CUTS = [300, 517, 700, 901]

CASES = {
    "buy_and_hold": lambda c: buy_and_hold(c),
    "trend_filter": lambda c: trend_filter(c, "A0", 100, off_asset="A1"),
    "momentum": lambda c: momentum(c, lookback=126, skip=21, top_n=2),
    "momentum_weekly": lambda c: momentum(c, lookback=63, skip=5, top_n=2, freq="W"),
    "rsi_reversion": lambda c: rsi_reversion(c, trend_window=100),
}


def leaks(fn, close, cuts=CUTS) -> bool:
    full = fn(close)
    for k in cuts:
        part = fn(close.iloc[: k + 1])
        a, b = full.iloc[: k + 1], part
        same = ((a == b) | (a.isna() & b.isna())).all().all()
        if not same:
            return True
    return False


@pytest.mark.parametrize("name", list(CASES))
def test_strategy_has_no_lookahead(name):
    assert not leaks(CASES[name], CLOSE), f"{name} uses future data"


def test_detector_catches_a_cheater():
    def cheater(c):  # peeks at tomorrow's close
        return (c.shift(-1) > c).astype(float) / c.shape[1]
    assert leaks(cheater, CLOSE)


def test_ml_rank_has_no_lookahead():
    from steadyedge.ml import ml_rank
    close = synthetic(n_assets=6, years=8, seed=4)["close"]
    fn = lambda c: ml_rank(c, top_n=2, train_years=3, min_train_rows=200, max_iter=30)
    w = fn(close)
    assert w.notna().any(axis=1).sum() > 24          # it actually trades
    assert not leaks(fn, close, cuts=[1300, 1650, 1900])


def test_momentum_buffered_has_no_lookahead_and_trades_less():
    from steadyedge.strategies import momentum_buffered
    from steadyedge.costs import ZeroCosts
    from steadyedge.engine import run_backtest
    b = synthetic(n_assets=8, years=6, seed=9)
    c = b["close"]
    fn = lambda x: momentum_buffered(x, lookback=126, skip=21, top_n=2, buffer=2)
    assert not leaks(fn, c, cuts=[400, 777, 1200])
    plain = run_backtest(b["open"], c, momentum(c, lookback=126, skip=21, top_n=2), ZeroCosts(), 1000, True)
    buf = run_backtest(b["open"], c, fn(c), ZeroCosts(), 1000, True)
    assert buf.turnover.sum() < plain.turnover.sum()


def test_ml_with_context_has_no_lookahead():
    from steadyedge.ml import ml_rank
    b = synthetic(n_assets=6, years=8, seed=4)
    close = b["close"].copy()
    close["^VIX"] = 20 + (close["A0"].pct_change().rolling(21).std().fillna(0.01) * 1000)
    fn = lambda c: ml_rank(c, top_n=2, train_years=3, min_train_rows=200, max_iter=30,
                           universe=["A1", "A2", "A3", "A4", "A5"], market="A0", context=["^VIX"])
    w = fn(close)
    assert w["^VIX"].fillna(0).eq(0).all()             # context is never traded
    assert w.notna().any(axis=1).sum() > 24
    assert not leaks(fn, close, cuts=[1300, 1900])
