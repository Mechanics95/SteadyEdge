# Decision log

Newest last. Each entry: date, decision, why, and what would change it.

| # | Date | Decision | Why | Revisit if |
|---|---|---|---|---|
| 1 | 2026-11-27 | Phase 1 is research only: no broker connection, no live orders. | A backtest must earn trust before money moves. | Never skipped; Phase 2 starts only via the promotion gate. |
| 2 | 2026-11-27 | Public GitHub repo, MIT license, prominent not-financial-advice disclaimer. | Max wants it public for portfolio and content. Disclaimer limits misreading results as advice. | Legal review suggests stronger wording. |
| 3 | 2026-11-27 | Python with pandas/numpy/scipy only in the core; yfinance optional for downloads. | Small dependency footprint, easy for others to run. | We need speed (polars) or ML (scikit-learn, LightGBM) in Phase 1b. |
| 4 | 2026-11-27 | Free daily data from yfinance (US and `.NS` India tickers), cached as CSV. | Max approved free data. | Data quality issues block a result; then propose paid data with prices first. |
| 5 | 2026-11-27 | Own small engine instead of backtrader/vectorbt. Signal at close t, fill at open t+1, enforced in the engine. | Makes timing and costs auditable and testable; avoids silent same-bar fills. | Engine speed becomes a bottleneck. |
| 6 | 2026-11-27 | Capital: $500 US (fractional shares) and Rs 44,000 India (whole shares). | Max's stated amounts. Rs figure assumes Rs 88/USD and must be updated to the real rate. | Max changes capital. |
| 7 | 2026-11-27 | Kill switch at $250 loss per market (Rs 22,000 India). | Max's total tolerance is a $500 loss; splitting it keeps either market from using all of it. | Max sets a different limit. |
| 8 | 2026-11-27 | Stable sleeve = broad index ETF held (SPY; NIFTYBEES). Active sleeve = monthly momentum (ETFs in US; large caps in India). | Index holding is the honest benchmark: any active idea must beat it after costs. Momentum is the most documented baseline. | Baselines established; then ML models compete for the active sleeve. |
| 9 | 2026-11-27 | Allocation rules tested: fixed 90/10 to 50/50, volatility target, drawdown throttle, all charged real switching costs. | Answers Max's "balance between volatile and stable" with evidence. | — |
| 10 | 2026-11-27 | Holdout from 2025-01-01 sealed; opening is logged and allowed once per holdout. | Prevents tuning on the test set. | After a holdout is spent, choose a new forward period (paper trading). |
| 11 | 2026-11-27 | Every variant appended to results/runs.jsonl; Deflated Sharpe uses the cumulative trial count. | Many tries make luck look like skill; DSR corrects for it. | — |
| 12 | 2026-11-27 | India costs default to delivery (CNC) trades, not intraday. | Intraday equity is generally not available to NRIs; delivery is also cheaper on STT for holding periods > 1 day. | Max confirms resident status and wants intraday research. |
| 13 | 2026-11-27 | India universe uses today's large caps: survivorship-biased, flagged in config and reports. US active sleeve uses ETFs to avoid that bias. | No free point-in-time Nifty membership with delisted prices. | We source historical constituents. |
| 14 | 2026-11-27 | Real-data runs execute in GitHub Actions (or on Max's machine), not in the build sandbox. | The sandbox used for building cannot reach Yahoo/NSE. | — |
| 15 | 2026-11-27 | "Learn from mistakes every day" = daily walk-forward refit plus a daily trade journal in paper trading (Phase 2), not online learning in backtests. | Daily refits on live data are measurable; continual self-modification in a backtest is a leak risk. | — |
