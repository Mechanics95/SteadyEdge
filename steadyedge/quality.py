"""Data quality guards for free daily data.

Yahoo sometimes misses a split or unit restructuring (for example an ETF
re-denominated 1:10). That shows up as a one-day price jump by a clean
ratio. Left in, it fakes a ~90% crash. We back-adjust earlier prices by the
ratio and log every fix so it shows in the report.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

RATIOS = [2, 3, 4, 5, 10, 20, 50, 100]


def _near_ratio(x: float, tol: float = 0.06) -> int | None:
    for k in RATIOS:
        if abs(x * k - 1) < tol:      # price fell to 1/k
            return k
        if abs(x / k - 1) < tol:      # price rose k-fold (reverse split)
            return -k
    return None


def fix_unadjusted_splits(open_: pd.DataFrame, close: pd.DataFrame, min_jump: float = 0.45):
    open_, close = open_.copy(), close.copy()
    log = []
    for t in close.columns:
        if str(t).startswith("^"):   # indexes / VIX / yields: big moves are real, no splits
            continue
        c = close[t]
        valid = c.dropna()
        r = valid / valid.shift(1)
        for d, x in r[(r < 1 - min_jump) | (r > 1 / (1 - min_jump))].items():
            k = _near_ratio(float(x))
            if k is None:
                log.append(f"{t} {d.date()}: one-day move x{x:.3f} with no clean split ratio; left as is, check manually")
                continue
            factor = 1 / k if k > 0 else abs(k)
            before = close.index < d
            close.loc[before, t] *= factor
            # The open on the jump day already trades at the new unit.
            open_.loc[before, t] *= factor
            log.append(f"{t} {d.date()}: one-day price-unit jump {'down' if k > 0 else 'up'} by a factor of {abs(k)} "
                       "(missing split adjustment or bad print); earlier prices rescaled to match")
    return open_, close, log
