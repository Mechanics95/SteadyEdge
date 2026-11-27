# Promotion gate

A model moves from backtest to paper trading only if **all** hold, per market:

1. Beats its benchmark (buy-and-hold index ETF) on walk-forward out-of-sample results **after costs**.
2. Deflated Sharpe Ratio of the **excess return over the index** (`dsr_vs_index`) > 0.95, using the family's full trial count.
3. Out-of-sample max drawdown no worse than 25%, and the kill switch never fires.
4. Survives regimes: positive excess return in at least 60% of test years, including one bear year.
5. Robust: neighbouring parameter values also beat the benchmark.
6. Passes the sealed holdout, opened once.

Paper trading to real money: at least 3 months (target 6) of paper results consistent with
the backtest (return within the backtest's 90% range, no rule breaks). Then start with a
fraction of the planned capital.

Even a model that passes everything can lose money live. The gate lowers the odds of
fooling ourselves; it does not remove market risk.
