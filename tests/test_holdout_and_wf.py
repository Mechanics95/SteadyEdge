import pandas as pd
import pytest
from steadyedge.costs import ZeroCosts
from steadyedge.data import HoldoutLocked, apply_holdout, synthetic
from steadyedge.portfolio import walk_forward
from steadyedge.strategies import momentum


def test_holdout_is_cut_by_default(tmp_path):
    bars = synthetic(years=5)
    out = apply_holdout(bars, "2011-01-01", False, "a", tmp_path / "h.json")
    assert out["close"].index.max() < pd.Timestamp("2011-01-01")


def test_holdout_can_only_be_opened_once(tmp_path):
    bars, log = synthetic(years=5), tmp_path / "h.json"
    apply_holdout(bars, "2011-01-01", True, "final_candidate", log)
    apply_holdout(bars, "2011-01-01", True, "final_candidate", log)   # same candidate re-run: ok
    with pytest.raises(HoldoutLocked):
        apply_holdout(bars, "2011-01-01", True, "tweaked_candidate", log)


def test_walk_forward_choice_ignores_future():
    b = synthetic(n_assets=5, years=10, seed=11)
    o, c = b["open"], b["close"]
    args = dict(param_grid={"lookback": [63, 252], "top_n": [1, 2]}, cost_model=ZeroCosts(),
                capital=1000, fractional=True, train_years=3, test_years=1)
    mk = lambda cl, **p: momentum(cl, skip=5, **p)
    wf1 = walk_forward(mk, open_=o, close=c, **args)
    # Scramble everything after the first fold's training window.
    cut = pd.Timestamp(wf1["folds"][0]["test"].split("..")[0])
    c2, o2 = c.copy(), o.copy()
    c2.loc[c2.index >= cut] = c2.loc[c2.index >= cut].iloc[::-1].to_numpy()
    o2.loc[o2.index >= cut] = o2.loc[o2.index >= cut].iloc[::-1].to_numpy()
    wf2 = walk_forward(mk, open_=o2, close=c2, **args)
    assert wf1["folds"][0]["chosen"] == wf2["folds"][0]["chosen"]
    assert wf1["n_trials"] == 4


def test_unadjusted_split_is_repaired():
    from steadyedge.quality import fix_unadjusted_splits
    b = synthetic(n_assets=2, years=2, seed=5)
    o, c = b["open"].copy(), b["close"].copy()
    k = 300
    c.iloc[k:, 0] /= 10
    o.iloc[k:, 0] /= 10
    o2, c2, log = fix_unadjusted_splits(o, c)
    assert len(log) == 1 and "factor of 10" in log[0]
    assert abs(c2.iloc[k, 0] / c2.iloc[k - 1, 0] - b["close"].iloc[k, 0] / b["close"].iloc[k - 1, 0]) < 1e-9


def test_holdout_lock_is_per_market(tmp_path):
    bars, log = synthetic(years=5), tmp_path / "h.json"
    apply_holdout(bars, "2011-01-01", True, "us_v2", log, scope="us")
    apply_holdout(bars, "2011-01-01", True, "india_v2", log, scope="india")   # other market: ok
    with pytest.raises(HoldoutLocked):
        apply_holdout(bars, "2011-01-01", True, "us_v3", log, scope="us")
