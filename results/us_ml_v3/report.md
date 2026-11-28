# Experiment report: us_ml_v3

> Research output, not financial advice. Backtests are simulations on past data and do not guarantee future results.

- Run: `20261128T092035Z-09eb01` · commit `470c8c4` · data `1cc5dd2d351d`
- Out-of-sample window: 2013-01-14 to 2024-12-31 (walk-forward; holdout sealed from 2025-01-01)
- Capital $500, kill switch at $250 loss, fractional shares, costs: us model
- Trials counted for this family so far: 130

## Results (out-of-sample only)

| variant | cagr | vol | sharpe | max_drawdown | worst_12m | annual_turnover | cost_drag_pct_of_capital_per_year | excess_cagr | dsr | dsr_vs_index | final_equity | killed_on |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| benchmark_buy_hold | 0.1433 | 0.1672 | 0.885 | -0.3372 | -0.1973 | 0.08 | 0.0 | 0.0 | 0.946 | None | 2478.45 | None |
| stable_only | 0.1004 | 0.124 | 0.834 | -0.2623 | -0.2398 | 5.11 | 0.0047 | -0.0429 | 0.923 | 0.005 | 1568.35 | None |
| active_only | 0.0816 | 0.1743 | 0.538 | -0.3689 | -0.2661 | 17.3 | 0.0136 | -0.0617 | 0.668 | 0.0 | 1277.55 | None |
| blend_fixed_90 | 0.0995 | 0.1215 | 0.842 | -0.2564 | -0.234 | 6.42 | 0.0059 | -0.0438 | 0.927 | 0.003 | 1552.9 | None |
| blend_fixed_80 | 0.0984 | 0.1209 | 0.837 | -0.2513 | -0.2286 | 7.72 | 0.007 | -0.0449 | 0.925 | 0.002 | 1534.55 | None |
| blend_fixed_70 | 0.0971 | 0.1222 | 0.82 | -0.2484 | -0.2235 | 9.01 | 0.0081 | -0.0462 | 0.916 | 0.001 | 1513.35 | None |
| blend_fixed_60 | 0.0956 | 0.1255 | 0.791 | -0.2471 | -0.2187 | 10.28 | 0.0091 | -0.0477 | 0.901 | 0.0 | 1489.45 | None |
| blend_fixed_50 | 0.094 | 0.1304 | 0.754 | -0.248 | -0.2142 | 11.54 | 0.0101 | -0.0493 | 0.878 | 0.0 | 1463.0 | None |
| blend_vol_target | 0.0928 | 0.125 | 0.773 | -0.2471 | -0.2187 | 10.26 | 0.009 | -0.0505 | 0.89 | 0.0 | 1444.7 | None |
| blend_drawdown_throttle | 0.0932 | 0.1214 | 0.795 | -0.2527 | -0.2282 | 8.96 | 0.0079 | -0.0501 | 0.903 | 0.001 | 1450.8 | None |

## Walk-forward choices for the active sleeve

| train | test | chosen params | train Sharpe |
|---|---|---|---|
| 2008-01-14..2013-01-14 | 2013-01-14..2014-01-14 | `{'top_n': 3}` | 0.091 |
| 2009-01-14..2014-01-14 | 2014-01-14..2015-01-14 | `{'top_n': 3}` | 0.357 |
| 2010-01-14..2015-01-14 | 2015-01-14..2016-01-14 | `{'top_n': 3}` | 0.517 |
| 2011-01-14..2016-01-14 | 2016-01-14..2017-01-14 | `{'top_n': 3}` | 0.302 |
| 2012-01-14..2017-01-14 | 2017-01-14..2018-01-14 | `{'top_n': 3}` | 0.457 |
| 2013-01-14..2018-01-14 | 2018-01-14..2019-01-14 | `{'top_n': 3}` | 0.701 |
| 2014-01-14..2019-01-14 | 2019-01-14..2020-01-14 | `{'top_n': 3}` | 0.302 |
| 2015-01-14..2020-01-14 | 2020-01-14..2021-01-14 | `{'top_n': 3}` | 0.46 |
| 2016-01-14..2021-01-14 | 2021-01-14..2022-01-14 | `{'top_n': 3}` | 0.612 |
| 2017-01-14..2022-01-14 | 2022-01-14..2023-01-14 | `{'top_n': 2}` | 0.831 |
| 2018-01-14..2023-01-14 | 2023-01-14..2024-01-14 | `{'top_n': 2}` | 0.458 |
| 2019-01-14..2024-01-14 | 2024-01-14..2024-12-31 | `{'top_n': 2}` | 0.617 |

## Data fixes applied

- none

## How to read this

- `dsr` (Deflated Sharpe Ratio) is the probability the Sharpe is real after accounting for how many variants were tried. `dsr_vs_index` asks the same of the edge over the index; the promotion gate needs `dsr_vs_index` > 0.95.
- `cost_drag_pct_of_capital_per_year` is fees and slippage as a share of starting capital.
- `excess_cagr` is versus simply holding the benchmark (benchmark has no kill switch).
- `killed_on`: date the $-loss kill switch fired and the variant went to cash for good.
