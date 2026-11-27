# SteadyEdge

Research-first backtesting and experiment framework for **US and Indian equities**.
It replays strategies on historical daily data with realistic costs, tests how to split
money between a **stable long-term sleeve** and an **active trading sleeve**, and keeps an
honest record of every experiment so results can't be cherry-picked.

> ## ⚠️ Disclaimer: not financial advice
> This project is for education and research. Nothing here is a recommendation to buy or
> sell any security. Backtests are simulations on past data; they routinely look better
> than live trading and **do not guarantee future results**. You can lose money, including
> all of it. The authors are not registered investment advisers (SEC) or research analysts
> (SEBI). Fee, tax, and regulatory figures in this repo are assumptions that change over
> time; verify them yourself. Use at your own risk.

## What's in Phase 1

| Piece | Where | What it does |
|---|---|---|
| Engine | `steadyedge/engine.py` | Daily simulation. Signals decided at close *t* execute at the **open of t+1**. Long-only, no leverage, whole or fractional shares, absolute-loss kill switch. |
| Costs | `steadyedge/costs.py` | US (zero-commission broker + spread/slippage + SEC/FINRA fees) and India delivery (STT, exchange, SEBI, stamp duty, GST, DP charge, slippage). |
| Strategies | `steadyedge/strategies.py` | Baselines: buy-and-hold, trend filter, cross-sectional momentum, RSI mean reversion. |
| Sleeves | `steadyedge/portfolio.py` | Combines stable + active sleeves in one account; allocation rules: fixed split, volatility target, drawdown throttle. Walk-forward parameter selection. |
| Metrics | `steadyedge/metrics.py` | CAGR, vol, Sharpe, Sortino, max drawdown, worst 12 months, turnover, cost drag, alpha/beta, **Probabilistic and Deflated Sharpe**. |
| Experiments | `steadyedge/experiment.py` | One YAML = one experiment family. Every variant is appended to `results/runs.jsonl` with git commit and data fingerprint. Writes `results/<name>/report.md`. |
| Guards | `tests/` | Lookahead detector run on every strategy, holdout lock, walk-forward isolation, cost arithmetic, engine timing. |

## Quick start

```bash
pip install -e ".[data,dev]"
pytest -q                                              # proofs the machinery works
python -m steadyedge run --config configs/synthetic_demo.yaml   # offline code check (random data)
python -m steadyedge download --config configs/us_sleeves.yaml   # free daily data via yfinance
python -m steadyedge run --config configs/us_sleeves.yaml
python -m steadyedge download --config configs/india_sleeves.yaml
python -m steadyedge run --config configs/india_sleeves.yaml
```

The **holdout** (from 2025-01-01 by default) is sealed. `--final-holdout` opens it, and the
code refuses to open the same holdout for a different candidate.

## Rules this repo lives by

1. Only out-of-sample (walk-forward) results are reported.
2. Every trial is logged, including failures; Deflated Sharpe uses the count.
3. A model is promoted only through the gate in `docs/PROMOTION_GATE.md`.
4. Every decision and its reason goes in `docs/DECISIONS.md`.

## Docs

- `docs/DECISIONS.md`: decision log
- `docs/PROMOTION_GATE.md`: what a model must pass before paper or real trading
- `docs/BROKERS_AND_RULES.md`: broker options, US day-trading rules, India NRI rules (not legal or tax advice)
- `docs/ROADMAP.md`: what's next

License: MIT.
