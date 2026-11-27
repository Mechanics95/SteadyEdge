# Experiment report: india_trend_v2

> Research output, not financial advice. Backtests are simulations on past data and do not guarantee future results.

- Run: `20261127T061302Z-59895b` · commit `9985416` · data `c5a4260c0a08`
- Out-of-sample window: 2025-01-01 to 2026-11-27 (walk-forward; holdout OPENED from 2025-01-01)
- Capital Rs 44,000, kill switch at Rs 22000 loss, whole shares, costs: india model
- Trials counted for this family so far: 102

## Results (out-of-sample only)

| variant | cagr | vol | sharpe | max_drawdown | worst_12m | annual_turnover | cost_drag_pct_of_capital_per_year | excess_cagr | dsr | dsr_vs_index | final_equity | killed_on |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| benchmark_buy_hold | 0.0493 | 0.1266 | 0.444 | -0.1479 | -0.1103 | 0.53 | 0.0012 | 0.0 | 0.186 | None | 48153.6 | None |
| stable_only | 0.0085 | 0.1382 | 0.13 | -0.2251 | -0.2031 | 6.93 | 0.0171 | -0.0408 | 0.093 | 0.025 | 44708.4 | None |
| active_only | -0.111 | 0.1706 | -0.604 | -0.2744 | -0.1949 | 10.52 | 0.0251 | -0.1603 | 0.01 | 0.001 | 35301.2 | None |
| blend_fixed_90 | -0.0096 | 0.1301 | -0.01 | -0.2126 | -0.1847 | 6.98 | 0.0252 | -0.0589 | 0.066 | 0.013 | 43208.0 | None |
| blend_fixed_80 | -0.0256 | 0.1262 | -0.142 | -0.2018 | -0.1716 | 7.36 | 0.028 | -0.0749 | 0.046 | 0.006 | 41914.4 | None |
| blend_fixed_70 | -0.0395 | 0.1229 | -0.267 | -0.1821 | -0.1492 | 7.7 | 0.0292 | -0.0888 | 0.032 | 0.003 | 40801.2 | None |
| blend_fixed_60 | -0.0504 | 0.129 | -0.336 | -0.1614 | -0.1235 | 8.39 | 0.0312 | -0.0997 | 0.026 | 0.002 | 39938.8 | None |
| blend_fixed_50 | -0.0608 | 0.1309 | -0.414 | -0.1616 | -0.1036 | 8.69 | 0.0315 | -0.1101 | 0.02 | 0.001 | 39124.8 | None |
| blend_vol_target | -0.0504 | 0.129 | -0.336 | -0.1614 | -0.1235 | 8.39 | 0.0312 | -0.0997 | 0.026 | 0.002 | 39938.8 | None |
| blend_drawdown_throttle | -0.039 | 0.1283 | -0.246 | -0.2047 | -0.1756 | 7.39 | 0.0267 | -0.0883 | 0.034 | 0.004 | 40840.8 | None |

## Walk-forward choices for the active sleeve

| train | test | chosen params | train Sharpe |
|---|---|---|---|
| 2009-01-11..2014-01-11 | 2014-01-11..2015-01-11 | `{'lookback': 126, 'top_n': 3}` | 1.621 |
| 2010-01-11..2015-01-11 | 2015-01-11..2016-01-11 | `{'lookback': 126, 'top_n': 4}` | 1.696 |
| 2011-01-11..2016-01-11 | 2016-01-11..2017-01-11 | `{'lookback': 252, 'top_n': 2}` | 1.337 |
| 2012-01-11..2017-01-11 | 2017-01-11..2018-01-11 | `{'lookback': 252, 'top_n': 2}` | 1.302 |
| 2013-01-11..2018-01-11 | 2018-01-11..2019-01-11 | `{'lookback': 126, 'top_n': 4}` | 1.636 |
| 2014-01-11..2019-01-11 | 2019-01-11..2020-01-11 | `{'lookback': 252, 'top_n': 4}` | 1.51 |
| 2015-01-11..2020-01-11 | 2020-01-11..2021-01-11 | `{'lookback': 252, 'top_n': 4}` | 1.392 |
| 2016-01-11..2021-01-11 | 2021-01-11..2022-01-11 | `{'lookback': 252, 'top_n': 4}` | 0.959 |
| 2017-01-11..2022-01-11 | 2022-01-11..2023-01-11 | `{'lookback': 252, 'top_n': 4}` | 1.29 |
| 2018-01-11..2023-01-11 | 2023-01-11..2024-01-11 | `{'lookback': 252, 'top_n': 4}` | 0.709 |
| 2019-01-11..2024-01-11 | 2024-01-11..2025-01-11 | `{'lookback': 252, 'top_n': 4}` | 0.844 |
| 2020-01-11..2025-01-11 | 2025-01-11..2026-01-11 | `{'lookback': 126, 'top_n': 2}` | 0.777 |
| 2021-01-11..2026-01-11 | 2026-01-11..2026-11-27 | `{'lookback': 252, 'top_n': 4}` | 1.312 |

## Data fixes applied

- GOLDBEES.NS 2019-12-19: one-day price-unit jump down by a factor of 100 (missing split adjustment or bad print); earlier prices rescaled to match
- GOLDBEES.NS 2019-12-23: one-day price-unit jump up by a factor of 100 (missing split adjustment or bad print); earlier prices rescaled to match
- NIFTYBEES.NS 2019-12-19: one-day price-unit jump down by a factor of 10 (missing split adjustment or bad print); earlier prices rescaled to match
- NIFTYBEES.NS 2019-12-23: one-day price-unit jump up by a factor of 10 (missing split adjustment or bad print); earlier prices rescaled to match

## How to read this

- `dsr` (Deflated Sharpe Ratio) is the probability the Sharpe is real after accounting for how many variants were tried. `dsr_vs_index` asks the same of the edge over the index; the promotion gate needs `dsr_vs_index` > 0.95.
- `cost_drag_pct_of_capital_per_year` is fees and slippage as a share of starting capital.
- `excess_cagr` is versus simply holding the benchmark (benchmark has no kill switch).
- `killed_on`: date the $-loss kill switch fired and the variant went to cash for good.
