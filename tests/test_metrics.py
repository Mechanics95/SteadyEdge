import numpy as np
import pandas as pd
import pytest
from steadyedge.metrics import deflated_sharpe, max_drawdown, probabilistic_sharpe, sharpe


def test_max_drawdown():
    eq = pd.Series([100, 120, 90, 130, 65.0])
    assert max_drawdown(eq) == pytest.approx(65 / 130 - 1)


def test_more_trials_lowers_deflated_sharpe():
    r = pd.Series(np.random.default_rng(0).normal(0.0005, 0.01, 1500))
    v = 0.0004
    assert deflated_sharpe(r, 100, v) < deflated_sharpe(r, 5, v) <= probabilistic_sharpe(r) + 1e-9


def test_noise_is_not_significant_after_many_trials():
    rng = np.random.default_rng(1)
    trials = [pd.Series(rng.normal(0, 0.01, 1000)) for _ in range(200)]
    srs = np.array([t.mean() / t.std() for t in trials])
    best = trials[int(srs.argmax())]
    assert sharpe(best) > 0.8                       # the luckiest noise looks good...
    assert deflated_sharpe(best, 200, srs.var()) < 0.95   # ...but DSR is not fooled
