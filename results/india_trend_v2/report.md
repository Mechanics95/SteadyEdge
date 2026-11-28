# Experiment report: india_trend_v2

> Research output, not financial advice. Backtests are simulations on past data and do not guarantee future results.

- Run: `20261128T045434Z-fc1a7b` · commit `b398cf4` · data `09cc34472fad`
- Out-of-sample window: 2014-01-11 to 2024-12-31 (walk-forward; holdout sealed from 2025-01-01)
- Capital Rs 44,000, kill switch at Rs 22000 loss, whole shares, costs: india model
- Trials counted for this family so far: 130

## Results (out-of-sample only)

| variant | cagr | vol | sharpe | max_drawdown | worst_12m | annual_turnover | cost_drag_pct_of_capital_per_year | excess_cagr | dsr | dsr_vs_index | final_equity | killed_on |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| benchmark_buy_hold | 0.1424 | 0.148 | 0.974 | -0.3633 | -0.2875 | 0.09 | 0.0002 | 0.0 | 0.439 | None | 183546.0 | None |
| stable_only | 0.1336 | 0.1312 | 1.022 | -0.215 | -0.1462 | 5.7 | 0.0242 | -0.0088 | 0.5 | 0.0 | 168951.2 | None |
| active_only | 0.1775 | 0.2062 | 0.896 | -0.3678 | -0.241 | 7.42 | 0.0491 | 0.0351 | 0.344 | 0.007 | 254122.0 | None |
| blend_fixed_90 | 0.1292 | 0.1273 | 1.019 | -0.2291 | -0.1504 | 5.94 | 0.041 | -0.0132 | 0.496 | 0.0 | 162126.8 | None |
| blend_fixed_80 | 0.136 | 0.1274 | 1.065 | -0.2398 | -0.1481 | 6.29 | 0.0483 | -0.0064 | 0.555 | 0.0 | 172915.6 | None |
| blend_fixed_70 | 0.1398 | 0.1303 | 1.07 | -0.2527 | -0.1455 | 6.59 | 0.052 | -0.0026 | 0.561 | 0.0 | 179128.4 | None |
| blend_fixed_60 | 0.145 | 0.1361 | 1.064 | -0.2652 | -0.1439 | 6.93 | 0.0572 | 0.0026 | 0.553 | 0.0 | 188144.0 | None |
| blend_fixed_50 | 0.1491 | 0.1441 | 1.037 | -0.2796 | -0.16 | 7.18 | 0.0599 | 0.0067 | 0.519 | 0.001 | 195434.8 | None |
| blend_vol_target | 0.1455 | 0.1361 | 1.066 | -0.2652 | -0.1439 | 6.95 | 0.0574 | 0.0031 | 0.556 | 0.0 | 188997.6 | None |
| blend_drawdown_throttle | 0.1333 | 0.1304 | 1.025 | -0.2629 | -0.1593 | 6.8 | 0.0513 | -0.0091 | 0.504 | 0.0 | 168418.8 | None |

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
| 2019-01-11..2024-01-11 | 2024-01-11..2024-12-31 | `{'lookback': 252, 'top_n': 4}` | 0.844 |

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
