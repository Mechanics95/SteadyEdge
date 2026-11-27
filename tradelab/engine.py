"""Daily backtest engine.

Timing rule (enforced here, not left to strategies): a target weight row
dated t is decided with information up to the close of t and executed at the
OPEN of the next trading day t+1. Equity is marked at each close.

Supports whole-share accounts (India, most brokers) and fractional shares
(Robinhood-style US accounts), a cash floor (no leverage, no shorting), and
an absolute loss kill switch.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd


@dataclass
class BacktestResult:
    equity: pd.Series
    returns: pd.Series
    trades: pd.DataFrame
    costs: pd.Series            # cost paid per day
    turnover: pd.Series         # traded notional / equity per day
    holdings: pd.DataFrame      # shares held at each close
    killed_on: pd.Timestamp | None = None
    meta: dict = field(default_factory=dict)


def run_backtest(
    open_: pd.DataFrame,
    close: pd.DataFrame,
    target_weights: pd.DataFrame,
    cost_model,
    initial_capital: float,
    fractional: bool = False,
    max_loss: float | None = None,
) -> BacktestResult:
    """Simulate a long-only, unlevered portfolio.

    target_weights: index=dates, columns=tickers. Rows that are all-NaN mean
    "no new decision, hold". Weights are clipped at 0 and scaled down if they
    sum above 1; the remainder is held as cash.
    """
    dates = close.index
    tickers = list(close.columns)
    open_ = open_.reindex(index=dates, columns=tickers)
    close = close.reindex(index=dates, columns=tickers)
    tw = target_weights.reindex(index=dates, columns=tickers)
    mark = close.ffill()

    cash = float(initial_capital)
    shares = np.zeros(len(tickers))
    pending: np.ndarray | None = None
    killed_on = None
    stop_trading = False

    eq, cost_day, turn_day, hold_rows, trade_rows = [], [], [], [], []

    for i, d in enumerate(dates):
        day_cost = 0.0
        day_traded = 0.0
        px_open = open_.iloc[i].to_numpy(dtype=float)
        if pending is not None:
            tradable = np.isfinite(px_open) & (px_open > 0)
            mark_open = np.where(tradable, px_open, mark.iloc[i - 1].to_numpy(dtype=float) if i > 0 else px_open)
            mark_open = np.nan_to_num(mark_open)
            value = cash + float(np.dot(shares, mark_open))
            w = np.nan_to_num(np.clip(pending, 0, None))
            if w.sum() > 1:
                w = w / w.sum()
            target_sh = np.where(tradable, w * value / np.where(tradable, px_open, 1.0), shares)
            if not fractional:
                target_sh = np.where(tradable, np.floor(target_sh + 1e-9), shares)
            delta = target_sh - shares

            # Sells first, to free cash.
            for j in np.where(delta < -1e-12)[0]:
                qty = -delta[j]
                notional = qty * px_open[j]
                c = cost_model.cost("sell", notional, qty).total
                cash += notional - c
                shares[j] -= qty
                day_cost += c
                day_traded += notional
                trade_rows.append((d, tickers[j], "sell", qty, px_open[j], notional, c))

            # Buys, scaled down if cash (after costs) is short.
            buys = np.where(delta > 1e-12)[0]
            if len(buys):
                want = {j: delta[j] for j in buys}
                for _ in range(50):
                    need = sum(q * px_open[j] + cost_model.cost("buy", q * px_open[j], q).total
                               for j, q in want.items() if q > 0)
                    if need <= cash + 1e-9:
                        break
                    scale = max(cash / need, 0.0) * 0.999
                    for j in want:
                        q = want[j] * scale
                        want[j] = q if fractional else np.floor(q)
                for j, q in want.items():
                    if q <= 0:
                        continue
                    notional = q * px_open[j]
                    c = cost_model.cost("buy", notional, q).total
                    if notional + c > cash + 1e-9:
                        continue
                    cash -= notional + c
                    shares[j] += q
                    day_cost += c
                    day_traded += notional
                    trade_rows.append((d, tickers[j], "buy", q, px_open[j], notional, c))
            pending = None

        px_close = np.nan_to_num(mark.iloc[i].to_numpy(dtype=float))
        equity = cash + float(np.dot(shares, px_close))
        eq.append(equity)
        cost_day.append(day_cost)
        turn_day.append(day_traded / equity if equity > 0 else 0.0)
        hold_rows.append(shares.copy())

        if stop_trading:
            continue
        if max_loss is not None and equity <= initial_capital - max_loss:
            # Kill switch: liquidate at next open, then never trade again.
            killed_on = d
            pending = np.zeros(len(tickers))
            stop_trading = True
            continue
        row = tw.iloc[i].to_numpy(dtype=float)
        if np.isfinite(row).any():
            pending = row

    equity_s = pd.Series(eq, index=dates, name="equity")
    trades = pd.DataFrame(trade_rows, columns=["date", "ticker", "side", "shares", "price", "notional", "cost"])
    return BacktestResult(
        equity=equity_s,
        returns=equity_s.pct_change().fillna(0.0),
        trades=trades,
        costs=pd.Series(cost_day, index=dates, name="cost"),
        turnover=pd.Series(turn_day, index=dates, name="turnover"),
        holdings=pd.DataFrame(hold_rows, index=dates, columns=tickers),
        killed_on=killed_on,
        meta={"initial_capital": initial_capital, "fractional": fractional, "max_loss": max_loss},
    )
