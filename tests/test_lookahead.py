"""Leak detector: a causal strategy's decision on day t must not change when
we delete all data after t. Run against every strategy, and against a
deliberately cheating strategy to prove the detector works."""
import numpy as np
import pandas as pd
import pytest
from tradelab.data import synthetic
from tradelab.strategies import buy_and_hold, momentum, rsi_reversion, trend_filter

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
