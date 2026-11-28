# Experiment report: india_ml_v3

> Research output, not financial advice. Backtests are simulations on past data and do not guarantee future results.

- Run: `20261128T045345Z-fdbdec` · commit `b398cf4` · data `7d78ebbab8a8`
- Out-of-sample window: 2014-01-11 to 2024-12-31 (walk-forward; holdout sealed from 2025-01-01)
- Capital Rs 44,000, kill switch at Rs 22000 loss, whole shares, costs: india model
- Trials counted for this family so far: 118

## Results (out-of-sample only)

| variant | cagr | vol | sharpe | max_drawdown | worst_12m | annual_turnover | cost_drag_pct_of_capital_per_year | excess_cagr | dsr | dsr_vs_index | final_equity | killed_on |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| benchmark_buy_hold | 0.1424 | 0.148 | 0.974 | -0.3633 | -0.2875 | 0.09 | 0.0002 | 0.0 | 0.396 | None | 183546.0 | None |
| stable_only | 0.1336 | 0.1312 | 1.022 | -0.215 | -0.1462 | 5.7 | 0.0242 | -0.0088 | 0.454 | 0.0 | 168951.2 | None |
| active_only | 0.1531 | 0.2198 | 0.758 | -0.4414 | -0.4072 | 14.96 | 0.1115 | 0.0107 | 0.165 | 0.001 | 202853.2 | None |
| blend_fixed_90 | 0.1243 | 0.1266 | 0.989 | -0.2392 | -0.1499 | 6.66 | 0.0464 | -0.0181 | 0.413 | 0.0 | 154734.8 | None |
| blend_fixed_80 | 0.1244 | 0.1268 | 0.988 | -0.269 | -0.1528 | 7.83 | 0.0568 | -0.018 | 0.412 | 0.0 | 154805.2 | None |
| blend_fixed_70 | 0.1268 | 0.1308 | 0.979 | -0.2854 | -0.1789 | 8.97 | 0.0653 | -0.0156 | 0.4 | 0.0 | 158430.8 | None |
| blend_fixed_60 | 0.1271 | 0.1372 | 0.941 | -0.3131 | -0.2182 | 9.98 | 0.0726 | -0.0153 | 0.354 | 0.0 | 158892.8 | None |
| blend_fixed_50 | 0.1274 | 0.1468 | 0.891 | -0.333 | -0.2489 | 11.01 | 0.0802 | -0.015 | 0.296 | 0.0 | 159354.8 | None |
| blend_vol_target | 0.1249 | 0.1359 | 0.935 | -0.3131 | -0.2182 | 9.91 | 0.0717 | -0.0175 | 0.347 | 0.0 | 155592.8 | None |
| blend_drawdown_throttle | 0.1195 | 0.1287 | 0.942 | -0.267 | -0.1576 | 8.87 | 0.0627 | -0.0229 | 0.354 | 0.0 | 147681.6 | None |

## Walk-forward choices for the active sleeve

| train | test | chosen params | train Sharpe |
|---|---|---|---|
| 2009-01-11..2014-01-11 | 2014-01-11..2015-01-11 | `{'top_n': 3}` | 0.956 |
| 2010-01-11..2015-01-11 | 2015-01-11..2016-01-11 | `{'top_n': 3}` | 1.362 |
| 2011-01-11..2016-01-11 | 2016-01-11..2017-01-11 | `{'top_n': 3}` | 1.294 |
| 2012-01-11..2017-01-11 | 2017-01-11..2018-01-11 | `{'top_n': 3}` | 1.484 |
| 2013-01-11..2018-01-11 | 2018-01-11..2019-01-11 | `{'top_n': 3}` | 1.61 |
| 2014-01-11..2019-01-11 | 2019-01-11..2020-01-11 | `{'top_n': 3}` | 1.387 |
| 2015-01-11..2020-01-11 | 2020-01-11..2021-01-11 | `{'top_n': 2}` | 0.747 |
| 2016-01-11..2021-01-11 | 2021-01-11..2022-01-11 | `{'top_n': 2}` | 0.79 |
| 2017-01-11..2022-01-11 | 2022-01-11..2023-01-11 | `{'top_n': 2}` | 0.723 |
| 2018-01-11..2023-01-11 | 2023-01-11..2024-01-11 | `{'top_n': 2}` | 0.564 |
| 2019-01-11..2024-01-11 | 2024-01-11..2024-12-31 | `{'top_n': 2}` | 0.469 |

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
