# Experiment report: india_ml_v3

> Research output, not financial advice. Backtests are simulations on past data and do not guarantee future results.

- Run: `20261127T055037Z-1f7964` · commit `a443e01` · data `bf9147a08aab`
- Out-of-sample window: 2014-01-11 to 2024-12-31 (walk-forward; holdout sealed from 2025-01-01)
- Capital Rs 44,000, kill switch at Rs 22000 loss, whole shares, costs: india model
- Trials counted for this family so far: 54

## Results (out-of-sample only)

| variant | cagr | vol | sharpe | max_drawdown | worst_12m | annual_turnover | cost_drag_pct_of_capital_per_year | excess_cagr | dsr | dsr_vs_index | final_equity | killed_on |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| benchmark_buy_hold | 0.1424 | 0.148 | 0.974 | -0.3633 | -0.2875 | 0.09 | 0.0002 | 0.0 | 0.996 | None | 183546.0 | None |
| stable_only | 0.1336 | 0.1312 | 1.022 | -0.215 | -0.1462 | 5.7 | 0.0242 | -0.0088 | 0.998 | 0.221 | 168951.2 | None |
| active_only | 0.1564 | 0.218 | 0.776 | -0.4766 | -0.4361 | 15.19 | 0.1198 | 0.014 | 0.978 | 0.512 | 209290.4 | None |
| blend_fixed_90 | 0.1243 | 0.1267 | 0.989 | -0.2452 | -0.1498 | 6.68 | 0.0471 | -0.0181 | 0.997 | 0.144 | 154743.6 | None |
| blend_fixed_80 | 0.1262 | 0.1269 | 1.0 | -0.2742 | -0.1588 | 7.86 | 0.0574 | -0.0162 | 0.997 | 0.143 | 157537.6 | None |
| blend_fixed_70 | 0.1271 | 0.1307 | 0.981 | -0.3036 | -0.2011 | 9.12 | 0.0678 | -0.0153 | 0.996 | 0.145 | 158923.6 | None |
| blend_fixed_60 | 0.1282 | 0.137 | 0.949 | -0.3295 | -0.2384 | 10.12 | 0.0753 | -0.0142 | 0.995 | 0.157 | 160556.0 | None |
| blend_fixed_50 | 0.1283 | 0.1466 | 0.897 | -0.3586 | -0.2782 | 11.15 | 0.0829 | -0.0141 | 0.992 | 0.174 | 160639.6 | None |
| blend_vol_target | 0.1254 | 0.136 | 0.937 | -0.3295 | -0.2384 | 10.07 | 0.0746 | -0.017 | 0.994 | 0.139 | 156248.4 | None |
| blend_drawdown_throttle | 0.127 | 0.1287 | 0.993 | -0.2749 | -0.1676 | 8.81 | 0.0647 | -0.0154 | 0.997 | 0.155 | 158672.8 | None |

## Walk-forward choices for the active sleeve

| train | test | chosen params | train Sharpe |
|---|---|---|---|
| 2009-01-11..2014-01-11 | 2014-01-11..2015-01-11 | `{'top_n': 2}` | 0.953 |
| 2010-01-11..2015-01-11 | 2015-01-11..2016-01-11 | `{'top_n': 3}` | 1.357 |
| 2011-01-11..2016-01-11 | 2016-01-11..2017-01-11 | `{'top_n': 3}` | 1.334 |
| 2012-01-11..2017-01-11 | 2017-01-11..2018-01-11 | `{'top_n': 3}` | 1.52 |
| 2013-01-11..2018-01-11 | 2018-01-11..2019-01-11 | `{'top_n': 3}` | 1.682 |
| 2014-01-11..2019-01-11 | 2019-01-11..2020-01-11 | `{'top_n': 3}` | 1.532 |
| 2015-01-11..2020-01-11 | 2020-01-11..2021-01-11 | `{'top_n': 3}` | 0.707 |
| 2016-01-11..2021-01-11 | 2021-01-11..2022-01-11 | `{'top_n': 2}` | 0.754 |
| 2017-01-11..2022-01-11 | 2022-01-11..2023-01-11 | `{'top_n': 3}` | 0.735 |
| 2018-01-11..2023-01-11 | 2023-01-11..2024-01-11 | `{'top_n': 2}` | 0.527 |
| 2019-01-11..2024-01-11 | 2024-01-11..2024-12-31 | `{'top_n': 2}` | 0.468 |

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
