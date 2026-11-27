import numpy as np
import pandas as pd
import pytest
from steadyedge.costs import IndiaDeliveryCosts, ZeroCosts
from steadyedge.engine import run_backtest


def _bars(n=10, open_px=None, close_px=None):
    idx = pd.bdate_range("2024-01-01", periods=n)
    o = pd.DataFrame({"X": open_px or [100.0 + i for i in range(n)]}, index=idx)
    c = pd.DataFrame({"X": close_px or [100.5 + i for i in range(n)]}, index=idx)
    return o, c


def test_signal_executes_next_open_not_same_day():
    o, c = _bars()
    w = pd.DataFrame(np.nan, index=c.index, columns=["X"])
    w.iloc[2] = 1.0
    r = run_backtest(o, c, w, ZeroCosts(), 1000, fractional=True)
    assert r.holdings["X"].iloc[2] == 0           # decided at close of day 2: not yet held
    assert r.holdings["X"].iloc[3] > 0            # bought on day 3
    t = r.trades.iloc[0]
    assert t["date"] == c.index[3] and t["price"] == o["X"].iloc[3]   # at day-3 OPEN


def test_whole_shares_and_no_negative_cash():
    o, c = _bars(open_px=[300.0] * 10, close_px=[300.0] * 10)
    w = pd.DataFrame(np.nan, index=c.index, columns=["X"])
    w.iloc[0] = 1.0
    r = run_backtest(o, c, w, IndiaDeliveryCosts(), 1000, fractional=False)
    assert r.holdings["X"].iloc[1] == 3           # floor(1000/300) after costs still affordable
    cash = r.equity.iloc[1] - 3 * 300
    assert cash >= 0


def test_unaffordable_share_means_no_position():
    o, c = _bars(open_px=[5000.0] * 10, close_px=[5000.0] * 10)
    w = pd.DataFrame(np.nan, index=c.index, columns=["X"])
    w.iloc[0] = 1.0
    r = run_backtest(o, c, w, ZeroCosts(), 1000, fractional=False)
    assert r.holdings["X"].sum() == 0 and r.equity.iloc[-1] == 1000


def test_weights_above_one_are_scaled_no_leverage():
    idx = pd.bdate_range("2024-01-01", periods=5)
    o = pd.DataFrame({"A": 10.0, "B": 10.0}, index=idx)
    c = o.copy()
    w = pd.DataFrame(np.nan, index=idx, columns=["A", "B"])
    w.iloc[0] = [1.0, 1.0]
    r = run_backtest(o, c, w, ZeroCosts(), 1000, fractional=True)
    assert (r.holdings.iloc[1] * 10).sum() == pytest.approx(1000)


def test_kill_switch_liquidates_and_stops():
    n = 12
    px = [100, 100, 90, 80, 70, 60, 55, 50, 60, 70, 80, 90]
    o, c = _bars(n, open_px=[float(p) for p in px], close_px=[float(p) for p in px])
    w = pd.DataFrame(1.0, index=c.index, columns=["X"])     # wants to be invested every day
    r = run_backtest(o, c, w, ZeroCosts(), 1000, fractional=True, max_loss=250)
    assert r.killed_on is not None
    k = c.index.get_loc(r.killed_on)
    assert (r.holdings["X"].iloc[k + 1:] == 0).all()          # flat after the next open
    assert r.equity.iloc[-1] == pytest.approx(r.equity.iloc[k + 1])  # no re-entry on the rebound


def test_costs_reduce_equity():
    o, c = _bars(open_px=[100.0] * 10, close_px=[100.0] * 10)
    w = pd.DataFrame(np.nan, index=c.index, columns=["X"])
    w.iloc[0], w.iloc[3] = 1.0, 0.0
    r = run_backtest(o, c, w, IndiaDeliveryCosts(), 100_000, fractional=False)
    assert r.equity.iloc[-1] < 100_000 and r.costs.sum() > 0
