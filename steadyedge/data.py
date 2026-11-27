"""Market data: free daily bars via yfinance, cached as CSV, plus a locked
holdout and a synthetic generator for offline tests.

yfinance is an unofficial Yahoo Finance client. It is fine for research but
has known gaps: no delisted tickers (survivorship bias), occasional bad
prints, and adjusted prices that get restated after splits and dividends.
Every load records a data fingerprint so a result can be tied to its data.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "raw"
HOLDOUT_LOG = ROOT / "results" / "holdout_log.json"


class HoldoutLocked(RuntimeError):
    pass


def download(tickers: list[str], market: str, start: str = "2005-01-01") -> None:
    import yfinance as yf  # optional dependency, only needed to fetch

    out = DATA_DIR / market
    out.mkdir(parents=True, exist_ok=True)
    for t in tickers:
        df = yf.download(t, start=start, auto_adjust=True, progress=False, actions=False)
        if df is None or df.empty:
            print(f"[warn] no data for {t}")
            continue
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df = df[["Open", "High", "Low", "Close", "Volume"]].dropna(how="all")
        df.index.name = "Date"
        df.to_csv(out / f"{t}.csv.gz")
        print(f"[ok] {t}: {len(df)} rows {df.index[0].date()}..{df.index[-1].date()}")
    (out / "_downloaded_at.txt").write_text(datetime.now(timezone.utc).isoformat())


def load(tickers: list[str], market: str) -> dict[str, pd.DataFrame]:
    frames = {}
    for t in tickers:
        p = DATA_DIR / market / f"{t}.csv.gz"
        if not p.exists():
            raise FileNotFoundError(f"{p} missing; run: python -m steadyedge download --config <cfg>")
        frames[t] = pd.read_csv(p, index_col=0, parse_dates=True)
    open_ = pd.DataFrame({t: f["Open"] for t, f in frames.items()}).sort_index()
    close = pd.DataFrame({t: f["Close"] for t, f in frames.items()}).sort_index()
    return {"open": open_, "close": close}


def fingerprint(close: pd.DataFrame) -> str:
    h = hashlib.sha256(pd.util.hash_pandas_object(close.fillna(-1), index=True).values.tobytes())
    return h.hexdigest()[:12]


def apply_holdout(bars: dict, holdout_start: str | None, use_holdout: bool, run_label: str,
                  log_path: Path = HOLDOUT_LOG) -> dict:
    """Cut data at holdout_start unless the holdout is deliberately opened.

    Opening the holdout is logged, and refused for a second run label: the
    holdout is a one-shot final exam, not a tuning set.
    """
    if not holdout_start:
        return bars
    cut = pd.Timestamp(holdout_start)
    if not use_holdout:
        return {k: v.loc[v.index < cut] for k, v in bars.items()}
    log = json.loads(log_path.read_text()) if log_path.exists() else []
    if any(e["holdout_start"] == holdout_start and e["label"] != run_label for e in log):
        raise HoldoutLocked(
            f"Holdout from {holdout_start} was already used by {[e['label'] for e in log]}. "
            "Using it again would turn it into a tuning set. Pick a new holdout period instead.")
    log.append({"label": run_label, "holdout_start": holdout_start,
                "opened_at": datetime.now(timezone.utc).isoformat()})
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(json.dumps(log, indent=2))
    return bars


def synthetic(n_assets: int = 6, years: int = 15, seed: int = 0, start: str = "2008-01-01") -> dict:
    """Random-walk prices with regime switches. For tests and offline demos
    only: results on this data say nothing about real markets."""
    rng = np.random.default_rng(seed)
    idx = pd.bdate_range(start, periods=years * 252)
    regime = np.cumsum(rng.random(len(idx)) < 1 / 250) % 2  # flips ~yearly
    mu = np.where(regime == 0, 0.0004, -0.0003)
    vol = np.where(regime == 0, 0.010, 0.020)
    common = rng.normal(mu, vol)
    cols = {}
    opens = {}
    for k in range(n_assets):
        idio = rng.normal(0.0001 * (k - n_assets / 2) / n_assets, 0.012, len(idx))
        r = 0.7 * common + idio
        close = 100 * np.exp(np.cumsum(r))
        gap = rng.normal(0, 0.003, len(idx))
        cols[f"A{k}"] = close
        opens[f"A{k}"] = np.r_[100, close[:-1]] * np.exp(gap)
    return {"open": pd.DataFrame(opens, index=idx), "close": pd.DataFrame(cols, index=idx)}
