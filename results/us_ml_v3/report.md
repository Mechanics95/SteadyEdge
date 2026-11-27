# Experiment report: us_ml_v3

> Research output, not financial advice. Backtests are simulations on past data and do not guarantee future results.

- Run: `20261127T055116Z-643e33` · commit `a443e01` · data `e04d675f5749`
- Out-of-sample window: 2013-01-14 to 2024-12-31 (walk-forward; holdout sealed from 2025-01-01)
- Capital $500, kill switch at $250 loss, fractional shares, costs: us model
- Trials counted for this family so far: 54

## Results (out-of-sample only)

| variant | cagr | vol | sharpe | max_drawdown | worst_12m | annual_turnover | cost_drag_pct_of_capital_per_year | excess_cagr | dsr | dsr_vs_index | final_equity | killed_on |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| benchmark_buy_hold | 0.1433 | 0.1672 | 0.885 | -0.3372 | -0.1973 | 0.08 | 0.0 | 0.0 | 0.965 | None | 2478.45 | None |
| stable_only | 0.1004 | 0.124 | 0.834 | -0.2623 | -0.2398 | 5.11 | 0.0047 | -0.0429 | 0.949 | 0.009 | 1568.35 | None |
| active_only | 0.078 | 0.1728 | 0.522 | -0.3689 | -0.2661 | 16.86 | 0.0139 | -0.0653 | 0.724 | 0.0 | 1227.25 | None |
| blend_fixed_90 | 0.0991 | 0.1213 | 0.84 | -0.2594 | -0.2374 | 6.37 | 0.0059 | -0.0442 | 0.951 | 0.006 | 1546.65 | None |
| blend_fixed_80 | 0.0976 | 0.1205 | 0.834 | -0.2571 | -0.2354 | 7.63 | 0.007 | -0.0457 | 0.949 | 0.003 | 1522.25 | None |
| blend_fixed_70 | 0.096 | 0.1217 | 0.815 | -0.2571 | -0.2337 | 8.87 | 0.0081 | -0.0473 | 0.943 | 0.002 | 1495.25 | None |
| blend_fixed_60 | 0.0942 | 0.1247 | 0.784 | -0.258 | -0.2324 | 10.09 | 0.0091 | -0.0491 | 0.93 | 0.001 | 1465.8 | None |
| blend_fixed_50 | 0.0922 | 0.1295 | 0.746 | -0.2611 | -0.2314 | 11.3 | 0.0101 | -0.0511 | 0.912 | 0.0 | 1434.05 | None |
| blend_vol_target | 0.0913 | 0.1243 | 0.765 | -0.258 | -0.2324 | 10.1 | 0.009 | -0.052 | 0.921 | 0.0 | 1420.3 | None |
| blend_drawdown_throttle | 0.0924 | 0.121 | 0.792 | -0.2631 | -0.2414 | 8.71 | 0.0078 | -0.0509 | 0.933 | 0.001 | 1438.25 | None |

## Walk-forward choices for the active sleeve

| train | test | chosen params | train Sharpe |
|---|---|---|---|
| 2008-01-14..2013-01-14 | 2013-01-14..2014-01-14 | `{'top_n': 3}` | 0.119 |
| 2009-01-14..2014-01-14 | 2014-01-14..2015-01-14 | `{'top_n': 3}` | 0.403 |
| 2010-01-14..2015-01-14 | 2015-01-14..2016-01-14 | `{'top_n': 3}` | 0.598 |
| 2011-01-14..2016-01-14 | 2016-01-14..2017-01-14 | `{'top_n': 3}` | 0.424 |
| 2012-01-14..2017-01-14 | 2017-01-14..2018-01-14 | `{'top_n': 3}` | 0.578 |
| 2013-01-14..2018-01-14 | 2018-01-14..2019-01-14 | `{'top_n': 3}` | 0.769 |
| 2014-01-14..2019-01-14 | 2019-01-14..2020-01-14 | `{'top_n': 3}` | 0.355 |
| 2015-01-14..2020-01-14 | 2020-01-14..2021-01-14 | `{'top_n': 3}` | 0.469 |
| 2016-01-14..2021-01-14 | 2021-01-14..2022-01-14 | `{'top_n': 2}` | 0.605 |
| 2017-01-14..2022-01-14 | 2022-01-14..2023-01-14 | `{'top_n': 2}` | 0.879 |
| 2018-01-14..2023-01-14 | 2023-01-14..2024-01-14 | `{'top_n': 3}` | 0.478 |
| 2019-01-14..2024-01-14 | 2024-01-14..2024-12-31 | `{'top_n': 3}` | 0.632 |

## Data fixes applied

- none

## How to read this

- `dsr` (Deflated Sharpe Ratio) is the probability the Sharpe is real after accounting for how many variants were tried. `dsr_vs_index` asks the same of the edge over the index; the promotion gate needs `dsr_vs_index` > 0.95.
- `cost_drag_pct_of_capital_per_year` is fees and slippage as a share of starting capital.
- `excess_cagr` is versus simply holding the benchmark (benchmark has no kill switch).
- `killed_on`: date the $-loss kill switch fired and the variant went to cash for good.
