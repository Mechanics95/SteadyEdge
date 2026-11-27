"""Paper trading (forward test). No broker, no real orders.

Each daily run:
1. Recompute the strategy's target weights on the latest data.
2. FREEZE today's decision by appending it to paper/<market>/decisions.csv.
   Past rows are never rewritten, so later data revisions or code changes
   cannot quietly improve the track record.
3. Replay the frozen decisions through the same engine (fill at next open,
   same costs, same kill switch) from the paper start date.
4. Write the ledger, trades, positions, and a daily journal entry, and compare
   against simply holding the index over the same days.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from . import data as D
from .costs import make_cost_model
from .engine import run_backtest
from .experiment import STRATEGIES, load_config
from .portfolio import allocation_series, combine_sleeves, walk_forward
from .quality import fix_unadjusted_splits

PAPER = D.ROOT / "paper"


def target_weights(cfg: dict, open_: pd.DataFrame, close: pd.DataFrame, stable_share: float) -> pd.DataFrame:
    cost = make_cost_model(cfg["market"], cfg.get("cost_overrides"))
    act = cfg["active"]
    base = act.get("params", {})
    wf = walk_forward(lambda c, **p: STRATEGIES[act["strategy"]](c, **{**base, **p}), act["grid"],
                      open_, close, cost, cfg["capital"], cfg.get("fractional", False),
                      cfg.get("train_years", 5), cfg.get("test_years", 1))
    w_stable = STRATEGIES[cfg["stable"]["strategy"]](close, **cfg["stable"].get("params", {}))
    frac = allocation_series("fixed", close.index, stable_share=stable_share)
    return combine_sleeves(w_stable, wf["weights"], frac), wf["folds"][-1]["chosen"]


def run_paper(market: str, config_path: str, stable_share: float = 0.8, out_root: Path = PAPER,
              bars: dict | None = None) -> dict:
    cfg = load_config(config_path)
    if bars is None:
        tickers = sorted(set(cfg["universe"]) | {cfg["benchmark"]})
        bars = D.load(tickers, cfg["market"])   # full history incl. the holdout: this is live use
    open_, close, fixes = fix_unadjusted_splits(bars["open"], bars["close"])
    w, params = target_weights(cfg, open_, close, stable_share)
    today = close.index[-1]

    out = out_root / market
    out.mkdir(parents=True, exist_ok=True)
    dec_path, meta_path = out / "decisions.csv", out / "paper_meta.json"
    if meta_path.exists():
        meta = json.loads(meta_path.read_text())
    else:
        meta = {"market": market, "config": config_path, "stable_share": stable_share,
                "start": str(today.date()), "capital": cfg["capital"], "max_loss": cfg.get("max_loss"),
                "created_at": datetime.now(timezone.utc).isoformat()}
    start = pd.Timestamp(meta["start"])

    decisions = pd.read_csv(dec_path, index_col=0, parse_dates=True) if dec_path.exists() else \
        pd.DataFrame(columns=close.columns, dtype=float)
    decisions = decisions.reindex(columns=close.columns)
    if today not in decisions.index:
        row = w.loc[today]
        if decisions.empty:                       # first day: buy the full current target
            row = w.ffill().loc[today]
        decisions.loc[today] = row.to_numpy()
        decisions = decisions.sort_index()
        decisions.to_csv(dec_path)
    action = "rebalance" if decisions.loc[today].notna().any() else "hold"

    o, c = open_.loc[open_.index >= start], close.loc[close.index >= start]
    cost = make_cost_model(cfg["market"], cfg.get("cost_overrides"))
    res = run_backtest(o, c, decisions, cost, cfg["capital"], cfg.get("fractional", False), cfg.get("max_loss"))
    bench = (c[cfg["benchmark"]] / c[cfg["benchmark"]].iloc[0]) * cfg["capital"]

    ledger = pd.DataFrame({"equity": res.equity.round(2), "index_hold": bench.round(2),
                           "cost": res.costs.round(2)})
    ledger.to_csv(out / "ledger.csv")
    res.trades.to_csv(out / "trades.csv", index=False)
    last = res.holdings.iloc[-1]
    pos = pd.DataFrame({"shares": last[last > 0], "close": c.iloc[-1][last > 0]})
    pos["value"] = (pos["shares"] * pos["close"]).round(2)
    pos.to_csv(out / "positions.csv")

    eq, ix = float(res.equity.iloc[-1]), float(bench.iloc[-1])
    day_pnl = float(res.equity.iloc[-1] - res.equity.iloc[-2]) if len(res.equity) > 1 else 0.0
    summary = {"date": str(today.date()), "equity": round(eq, 2), "index_hold": round(ix, 2),
               "return_since_start": round(eq / cfg["capital"] - 1, 4),
               "index_return_since_start": round(ix / cfg["capital"] - 1, 4),
               "day_pnl": round(day_pnl, 2), "action": action, "active_params": params,
               "killed_on": str(res.killed_on.date()) if res.killed_on is not None else None,
               "data_fixes": [f for f in fixes if f.split()[1][:10] >= meta["start"]]}
    meta["last_run"] = summary
    meta_path.write_text(json.dumps(meta, indent=2, default=str))

    journal = out / "journal.md"
    if not journal.exists():
        journal.write_text(f"# Paper trading journal: {market}\n\nSimulated only, no real orders. "
                           f"Strategy: {config_path}, {int(stable_share * 100)}% stable / "
                           f"{int((1 - stable_share) * 100)}% active. Start {meta['start']}.\n\n")
    if f"## {summary['date']}" not in journal.read_text():
        tgt = decisions.loc[today].dropna()
        tgt = ", ".join(f"{k} {v:.0%}" for k, v in tgt[tgt > 0].items()) or "all cash"
        with journal.open("a") as f:
            f.write(f"## {summary['date']}\n- Equity {eq:,.2f} ({summary['return_since_start']:+.2%}) vs index "
                    f"{ix:,.2f} ({summary['index_return_since_start']:+.2%}); day P&L {day_pnl:+,.2f}\n"
                    f"- Decision: {action}" + (f" → {tgt} (fills at next open)" if action == "rebalance" else "") +
                    f"\n- Active sleeve settings in use: `{params}`\n" +
                    "".join(f"- Data fix: {x}\n" for x in summary["data_fixes"]) + "\n")
    return summary


def main() -> None:
    import argparse
    p = argparse.ArgumentParser(prog="steadyedge.paper")
    p.add_argument("--market", required=True)
    p.add_argument("--config", required=True)
    p.add_argument("--stable-share", type=float, default=0.8)
    a = p.parse_args()
    print(json.dumps(run_paper(a.market, a.config, a.stable_share), indent=2))


if __name__ == "__main__":
    main()
