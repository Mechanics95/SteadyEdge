# Experiment report: india_mlctx_v5

> Research output, not financial advice. Backtests are simulations on past data and do not guarantee future results.

- Run: `20261128T045404Z-9acca3` · commit `b398cf4` · data `d65568e89a5d`
- Out-of-sample window: 2014-01-11 to 2024-12-31 (walk-forward; holdout sealed from 2025-01-01)
- Capital Rs 44,000, kill switch at Rs 22000 loss, whole shares, costs: india model
- Trials counted for this family so far: 130

## Results (out-of-sample only)

| variant | cagr | vol | sharpe | max_drawdown | worst_12m | annual_turnover | cost_drag_pct_of_capital_per_year | excess_cagr | dsr | dsr_vs_index | final_equity | killed_on |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| benchmark_buy_hold | 0.1423 | 0.1479 | 0.974 | -0.3631 | -0.2873 | 0.09 | 0.0002 | 0.0 | 0.439 | None | 183348.0 | None |
| stable_only | 0.1335 | 0.131 | 1.022 | -0.2146 | -0.146 | 5.69 | 0.0242 | -0.0088 | 0.5 | 0.0 | 168731.2 | None |
| active_only | 0.1174 | 0.2068 | 0.64 | -0.3939 | -0.2743 | 13.69 | 0.0641 | -0.0249 | 0.105 | 0.0 | 144856.8 | None |
| blend_fixed_90 | 0.1271 | 0.126 | 1.013 | -0.2111 | -0.1382 | 6.09 | 0.0309 | -0.0152 | 0.488 | 0.0 | 158919.2 | None |
| blend_fixed_80 | 0.1261 | 0.1261 | 1.005 | -0.2304 | -0.1371 | 7.07 | 0.0372 | -0.0162 | 0.478 | 0.0 | 157344.0 | None |
| blend_fixed_70 | 0.1307 | 0.1276 | 1.027 | -0.2237 | -0.128 | 8.0 | 0.043 | -0.0116 | 0.506 | 0.0 | 164414.8 | None |
| blend_fixed_60 | 0.1288 | 0.1328 | 0.979 | -0.2462 | -0.1436 | 8.79 | 0.0465 | -0.0135 | 0.444 | 0.0 | 161418.4 | None |
| blend_fixed_50 | 0.128 | 0.1405 | 0.928 | -0.2634 | -0.1643 | 9.64 | 0.0505 | -0.0143 | 0.379 | 0.0 | 160195.2 | None |
| blend_vol_target | 0.1263 | 0.1314 | 0.971 | -0.2462 | -0.1436 | 8.8 | 0.0461 | -0.016 | 0.434 | 0.0 | 157656.4 | None |
| blend_drawdown_throttle | 0.1252 | 0.1267 | 0.995 | -0.2254 | -0.1506 | 8.07 | 0.0424 | -0.0171 | 0.464 | 0.0 | 156002.0 | None |

## Walk-forward choices for the active sleeve

| train | test | chosen params | train Sharpe |
|---|---|---|---|
| 2009-01-11..2014-01-11 | 2014-01-11..2015-01-11 | `{'top_n': 3}` | 0.55 |
| 2010-01-11..2015-01-11 | 2015-01-11..2016-01-11 | `{'top_n': 3}` | 0.824 |
| 2011-01-11..2016-01-11 | 2016-01-11..2017-01-11 | `{'top_n': 3}` | 0.598 |
| 2012-01-11..2017-01-11 | 2017-01-11..2018-01-11 | `{'top_n': 3}` | 0.873 |
| 2013-01-11..2018-01-11 | 2018-01-11..2019-01-11 | `{'top_n': 3}` | 0.647 |
| 2014-01-11..2019-01-11 | 2019-01-11..2020-01-11 | `{'top_n': 3}` | 0.61 |
| 2015-01-11..2020-01-11 | 2020-01-11..2021-01-11 | `{'top_n': 3}` | 0.405 |
| 2016-01-11..2021-01-11 | 2021-01-11..2022-01-11 | `{'top_n': 3}` | 0.752 |
| 2017-01-11..2022-01-11 | 2022-01-11..2023-01-11 | `{'top_n': 3}` | 0.855 |
| 2018-01-11..2023-01-11 | 2023-01-11..2024-01-11 | `{'top_n': 3}` | 0.5 |
| 2019-01-11..2024-01-11 | 2024-01-11..2024-12-31 | `{'top_n': 3}` | 0.672 |

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
