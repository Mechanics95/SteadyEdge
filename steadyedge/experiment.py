"""Experiment runner and tracker.

One YAML config = one experiment family. A run evaluates, on the same
out-of-sample window: the benchmark, the stable sleeve, the active sleeve
(walk-forward), and every allocation rule between them. Every variant is
appended to results/runs.jsonl, so the total number of things we have tried
is never forgotten; the Deflated Sharpe Ratio uses that count.
"""
from __future__ import annotations

import json
import subprocess
import uuid
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from . import data as D
from .costs import make_cost_model
from .engine import BacktestResult, run_backtest
from .metrics import TRADING_DAYS, deflated_sharpe, sharpe, summarize
from .quality import fix_unadjusted_splits
from .portfolio import allocation_series, combine_sleeves, walk_forward
from .ml import ml_rank
from .strategies import STRATEGIES

STRATEGIES["ml_rank"] = ml_rank

RESULTS = D.ROOT / "results"


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=D.ROOT,
                                       stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return "uncommitted"


def slice_result(res: BacktestResult, start) -> BacktestResult:
    m = res.equity.index >= start
    eq = res.equity[m]
    return replace(res, equity=eq, returns=eq.pct_change().fillna(0.0), costs=res.costs[m],
                   turnover=res.turnover[m], holdings=res.holdings[m],
                   trades=res.trades[res.trades["date"] >= start] if len(res.trades) else res.trades,
                   meta={**res.meta, "initial_capital": float(eq.iloc[0])})


def _weights(spec: dict, close: pd.DataFrame) -> pd.DataFrame:
    return STRATEGIES[spec["strategy"]](close, **spec.get("params", {}))


def run_config(cfg: dict, use_holdout: bool = False, results_dir: Path = RESULTS) -> dict:
    name = cfg["name"]
    if cfg.get("data") == "synthetic":
        bars = D.synthetic(**cfg.get("synthetic", {}))
    else:
        tickers = sorted(set(cfg["universe"]) | {cfg["benchmark"]} | set(cfg.get("context", [])))
        bars = D.load(tickers, cfg["market"])
    bars = {k: v.loc[v.index >= pd.Timestamp(cfg.get("start", "1900-01-01"))] for k, v in bars.items()}
    bars = D.apply_holdout(bars, cfg.get("holdout_start"), use_holdout, name,
                           scope=cfg.get("family", cfg["market"]))
    open_, close = bars["open"], bars["close"]
    quality_log = []
    if cfg.get("data") != "synthetic":
        open_, close, quality_log = fix_unadjusted_splits(open_, close)
    cost = make_cost_model(cfg["market"], cfg.get("cost_overrides"))
    cap, frac, max_loss = cfg["capital"], cfg.get("fractional", False), cfg.get("max_loss")
    band = cfg.get("min_trade_frac", 0.0)

    def bt(w, kill=True):
        return run_backtest(open_, close, w, cost, cap, frac, max_loss if kill else None, band)

    # Active sleeve: walk-forward over its parameter grid.
    act = cfg["active"]
    base_params = act.get("params", {})
    wf = walk_forward(lambda c, **p: STRATEGIES[act["strategy"]](c, **{**base_params, **p}),
                      act["grid"], open_, close, cost, cap, frac,
                      cfg.get("train_years", 5), cfg.get("test_years", 1), min_trade_frac=band)
    if not wf["folds"]:
        raise ValueError("not enough history for one walk-forward fold")
    oos = pd.Timestamp(wf["oos_start"])
    if use_holdout:
        # Final exam: score ONLY the sealed period. Parameters are still picked
        # by walk-forward from earlier data, exactly as they would be live.
        oos = pd.Timestamp(cfg["holdout_start"])
        name = f"{name}_holdout"
        cfg = {**cfg, "title": cfg.get("title", name) + " (sealed 2025+ check)"}
    w_active = wf["weights"]
    w_stable = _weights(cfg["stable"], close)
    w_bench = STRATEGIES["buy_and_hold"](close, weights={cfg["benchmark"]: 1.0})

    # Signal-only run of the active sleeve over all history (no kill switch):
    # allocation rules read its past returns.
    active_alone = bt(w_active, kill=False)

    def start_at(w):
        # Every variant starts with fresh capital on the first out-of-sample
        # day, so the kill switch and all metrics refer to the same window.
        w2 = w.copy()
        w2[w2.index < oos] = np.nan
        first = int(np.argmax(w2.index >= oos))
        w2.iloc[first] = w.ffill().iloc[first].to_numpy()
        return w2

    variants = {"benchmark_buy_hold": bt(start_at(w_bench), kill=False),
                "stable_only": bt(start_at(w_stable)), "active_only": bt(start_at(w_active))}
    for a in cfg["allocations"]:
        rule = a["rule"]
        label = f"{rule}_{int(a.get('stable_share', 0.8) * 100)}" if rule == "fixed" else rule
        frac_s = allocation_series(rule, close.index, active_alone.returns, **{k: v for k, v in a.items() if k != "rule"})
        variants[f"blend_{label}"] = bt(start_at(combine_sleeves(w_stable, w_active, frac_s)))

    bench_r = slice_result(variants["benchmark_buy_hold"], oos).returns
    rows, equity = {}, {}
    for label, res in variants.items():
        s = slice_result(res, oos)
        rows[label] = summarize(s, bench_r)
        # Report as if `capital` were invested at the start of the out-of-sample window.
        rows[label]["final_equity"] = round(cap * (1 + rows[label]["total_return"]), 2)
        equity[label] = s.equity / s.equity.iloc[0] * cap

    # Trial accounting: everything ever logged for this family + this run.
    results_dir.mkdir(parents=True, exist_ok=True)
    log = results_dir / "runs.jsonl"
    past = [json.loads(l) for l in log.read_text().splitlines()] if log.exists() else []
    family = cfg.get("family", name)
    # A config already in the log is a re-run (fresh data), not a new idea:
    # it is not counted again. Rule: never edit a config after its first run;
    # a new idea gets a new name. Holdout runs are logged but not re-counted.
    seen = any(p.get("config", p["family"]) == name.removesuffix("_holdout") for p in past)
    past_sr = [p["metrics"]["sharpe"] for p in past if p["family"] == family]
    new_sr = [] if seen else [m["sharpe"] for m in rows.values()] + wf["trial_sharpes"]
    all_sr = np.array(past_sr + new_sr) / np.sqrt(TRADING_DAYS)
    adj_path = results_dir / "trial_adjustments.json"
    untracked = json.loads(adj_path.read_text()).get(family, 0) if adj_path.exists() else 0
    n_trials = len(all_sr) + untracked
    for label in rows:
        s = slice_result(variants[label], oos)
        rows[label]["dsr"] = round(deflated_sharpe(s.returns, n_trials, float(np.var(all_sr))), 3)
        # Is the EDGE over the index real? Same deflation, applied to daily
        # excess returns. This is the number the promotion gate uses.
        excess = s.returns - bench_r.reindex(s.returns.index).fillna(0.0)
        rows[label]["dsr_vs_index"] = (round(deflated_sharpe(excess, n_trials, float(np.var(all_sr))), 3)
                                       if excess.std() > 0 else None)
        rows[label]["n_trials_family"] = n_trials

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:6]
    meta = {"run_id": run_id, "family": family, "config_name": name, "git_commit": git_commit(),
            "data_fingerprint": D.fingerprint(close), "used_holdout": use_holdout,
            "oos_start": str(oos.date()), "data_end": str(close.index[-1].date()),
            "walk_forward_folds": wf["folds"], "data_fixes": quality_log, "config": cfg}
    if not seen:
        with log.open("a") as f:
            for label, m in rows.items():
                f.write(json.dumps({"run_id": run_id, "family": family, "config": name, "variant": label,
                                    "time": meta["run_id"][:16], "git_commit": meta["git_commit"],
                                    "data_fingerprint": meta["data_fingerprint"],
                                    "used_holdout": use_holdout, "metrics": m}) + "\n")
            # Walk-forward grid candidates are trials too.
            for i, sr in enumerate(wf["trial_sharpes"]):
                f.write(json.dumps({"run_id": run_id, "family": family, "config": name, "variant": f"grid_{i}",
                                    "time": meta["run_id"][:16], "used_holdout": use_holdout,
                                    "metrics": {"sharpe": round(sr, 3)}}) + "\n")

    out = results_dir / name
    out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(equity).to_csv(out / "equity.csv")
    (out / "metrics.json").write_text(json.dumps(rows, indent=2, default=str))
    trades = []
    for label in ("active_only", "stable_only"):
        t = slice_result(variants[label], oos).trades.copy()
        t.insert(0, "variant", label)
        trades.append(t)
    pd.concat(trades).to_csv(out / "trades.csv", index=False)
    (out / "run_meta.json").write_text(json.dumps(meta, indent=2, default=str))
    (out / "report.md").write_text(render_report(cfg, meta, rows))
    return {"meta": meta, "metrics": rows}


def render_report(cfg: dict, meta: dict, rows: dict) -> str:
    cur = "$" if cfg["market"] == "us" else ("Rs " if cfg["market"] == "india" else "")
    cols = ["cagr", "vol", "sharpe", "max_drawdown", "worst_12m", "annual_turnover",
            "cost_drag_pct_of_capital_per_year", "excess_cagr", "dsr", "dsr_vs_index", "final_equity", "killed_on"]
    hdr = "| variant | " + " | ".join(cols) + " |\n|" + "---|" * (len(cols) + 1) + "\n"
    body = "".join("| " + k + " | " + " | ".join(str(v.get(c, "")) for c in cols) + " |\n" for k, v in rows.items())
    synth = cfg.get("data") == "synthetic"
    lines = [
        f"# Experiment report: {cfg['name']}",
        "",
        "> Research output, not financial advice. Backtests are simulations on past data and do not "
        "guarantee future results." + (" **This run uses SYNTHETIC random data: it tests the code, "
                                        "and says nothing about real markets.**" if synth else ""),
        "",
        f"- Run: `{meta['run_id']}` · commit `{meta['git_commit']}` · data `{meta['data_fingerprint']}`",
        f"- Out-of-sample window: {meta['oos_start']} to {meta['data_end']} (walk-forward; holdout "
        f"{'OPENED' if meta['used_holdout'] else 'sealed'} from {cfg.get('holdout_start')})",
        f"- Capital {cur}{cfg['capital']:,}, kill switch at {cur}{cfg.get('max_loss')} loss, "
        f"{'fractional' if cfg.get('fractional') else 'whole'} shares, costs: {cfg['market']} model",
        f"- Trials counted for this family so far: {next(iter(rows.values()))['n_trials_family']}",
        "",
        "## Results (out-of-sample only)",
        "",
        hdr + body,
        "## Walk-forward choices for the active sleeve",
        "",
        "| train | test | chosen params | train Sharpe |\n|---|---|---|---|",
        *[f"| {f['train']} | {f['test']} | `{f['chosen']}` | {f['train_sharpe']} |" for f in meta["walk_forward_folds"]],
        "",
        "## Data fixes applied",
        "",
        *([f"- {q}" for q in meta["data_fixes"]] or ["- none"]),
        "",
        "## How to read this",
        "",
        "- `dsr` (Deflated Sharpe Ratio) is the probability the Sharpe is real after accounting for "
        "how many variants were tried. `dsr_vs_index` asks the same of the edge over the index; "
        "the promotion gate needs `dsr_vs_index` > 0.95.",
        "- `cost_drag_pct_of_capital_per_year` is fees and slippage as a share of starting capital.",
        "- `excess_cagr` is versus simply holding the benchmark (benchmark has no kill switch).",
        "- `killed_on`: date the $-loss kill switch fired and the variant went to cash for good.",
    ]
    return "\n".join(lines) + "\n"


def load_config(path: str) -> dict:
    return yaml.safe_load(Path(path).read_text())
