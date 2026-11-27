"""Performance, risk, and overfitting metrics."""
from __future__ import annotations

import math

import numpy as np
import pandas as pd
from scipy import stats

TRADING_DAYS = 252
EULER_GAMMA = 0.5772156649015329


def cagr(equity: pd.Series) -> float:
    years = len(equity) / TRADING_DAYS
    if years <= 0 or equity.iloc[0] <= 0 or equity.iloc[-1] <= 0:
        return float("nan") if equity.iloc[-1] > 0 else -1.0
    return (equity.iloc[-1] / equity.iloc[0]) ** (1 / years) - 1


def sharpe(returns: pd.Series, rf_daily: float = 0.0) -> float:
    r = returns - rf_daily
    sd = r.std(ddof=1)
    return float(r.mean() / sd * math.sqrt(TRADING_DAYS)) if sd > 0 else 0.0


def sortino(returns: pd.Series, rf_daily: float = 0.0) -> float:
    r = returns - rf_daily
    downside = np.sqrt((np.minimum(r, 0) ** 2).mean())
    return float(r.mean() / downside * math.sqrt(TRADING_DAYS)) if downside > 0 else 0.0


def drawdown(equity: pd.Series) -> pd.Series:
    return equity / equity.cummax() - 1


def max_drawdown(equity: pd.Series) -> float:
    return float(drawdown(equity).min())


def longest_underwater_days(equity: pd.Series) -> int:
    under = (drawdown(equity) < 0).to_numpy()
    best = cur = 0
    for u in under:
        cur = cur + 1 if u else 0
        best = max(best, cur)
    return int(best)


def worst_rolling_return(equity: pd.Series, window: int = TRADING_DAYS) -> float:
    if len(equity) <= window:
        return float(equity.iloc[-1] / equity.iloc[0] - 1)
    return float((equity / equity.shift(window) - 1).min())


def probabilistic_sharpe(returns: pd.Series, sr_benchmark: float = 0.0) -> float:
    """PSR (Bailey & Lopez de Prado 2012). Sharpe values here are per-period."""
    r = returns.dropna()
    n = len(r)
    if n < 3 or r.std(ddof=1) == 0:
        return float("nan")
    sr = r.mean() / r.std(ddof=1)
    skew = stats.skew(r)
    kurt = stats.kurtosis(r, fisher=False)
    denom = math.sqrt(max(1 - skew * sr + (kurt - 1) / 4 * sr ** 2, 1e-12))
    return float(stats.norm.cdf((sr - sr_benchmark) * math.sqrt(n - 1) / denom))


def deflated_sharpe(returns: pd.Series, n_trials: int, trial_sharpe_var: float) -> float:
    """DSR (Bailey & Lopez de Prado 2014): PSR against the Sharpe you would
    expect from the best of n_trials pure-luck strategies.

    trial_sharpe_var: variance of the per-period Sharpe ratios across all
    trials run so far (annualised Sharpe / sqrt(252), squared).
    """
    if n_trials <= 1 or trial_sharpe_var <= 0:
        return probabilistic_sharpe(returns, 0.0)
    z1 = stats.norm.ppf(1 - 1 / n_trials)
    z2 = stats.norm.ppf(1 - 1 / (n_trials * math.e))
    sr0 = math.sqrt(trial_sharpe_var) * ((1 - EULER_GAMMA) * z1 + EULER_GAMMA * z2)
    return probabilistic_sharpe(returns, sr0)


def summarize(result, benchmark_returns: pd.Series | None = None) -> dict:
    eq, r = result.equity, result.returns
    years = len(eq) / TRADING_DAYS
    out = {
        "start": str(eq.index[0].date()),
        "end": str(eq.index[-1].date()),
        "years": round(years, 2),
        "final_equity": round(float(eq.iloc[-1]), 2),
        "total_return": round(float(eq.iloc[-1] / eq.iloc[0] - 1), 4),
        "cagr": round(cagr(eq), 4),
        "vol": round(float(r.std(ddof=1) * math.sqrt(TRADING_DAYS)), 4),
        "sharpe": round(sharpe(r), 3),
        "sortino": round(sortino(r), 3),
        "max_drawdown": round(max_drawdown(eq), 4),
        "longest_underwater_days": longest_underwater_days(eq),
        "worst_12m": round(worst_rolling_return(eq), 4),
        "annual_turnover": round(float(result.turnover.sum() / max(years, 1e-9)), 2),
        "total_costs": round(float(result.costs.sum()), 2),
        "cost_drag_pct_of_capital_per_year": round(
            float(result.costs.sum() / result.meta["initial_capital"] / max(years, 1e-9)), 4),
        "n_trades": int(len(result.trades)),
        "psr": round(probabilistic_sharpe(r), 3),
        "killed_on": str(result.killed_on.date()) if result.killed_on is not None else None,
    }
    if out["max_drawdown"] < 0:
        out["calmar"] = round(out["cagr"] / abs(out["max_drawdown"]), 3)
    if benchmark_returns is not None:
        b = benchmark_returns.reindex(r.index).fillna(0.0)
        if b.var() > 0:
            beta = float(np.cov(r, b)[0, 1] / b.var())
            alpha = float((r.mean() - beta * b.mean()) * TRADING_DAYS)
            out["beta"] = round(beta, 3)
            out["alpha_annual"] = round(alpha, 4)
            beq = (1 + b).cumprod()
            out["benchmark_cagr"] = round(cagr(beq), 4)
            out["benchmark_max_drawdown"] = round(max_drawdown(beq), 4)
            out["excess_cagr"] = round(out["cagr"] - out["benchmark_cagr"], 4)
    return out
