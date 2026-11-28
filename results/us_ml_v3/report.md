# Experiment report: us_ml_v3

> Research output, not financial advice. Backtests are simulations on past data and do not guarantee future results.

- Run: `20261128T045506Z-474d41` · commit `b398cf4` · data `5e3dc40ad7d7`
- Out-of-sample window: 2013-01-14 to 2024-12-31 (walk-forward; holdout sealed from 2025-01-01)
- Capital $500, kill switch at $250 loss, fractional shares, costs: us model
- Trials counted for this family so far: 118

## Results (out-of-sample only)

| variant | cagr | vol | sharpe | max_drawdown | worst_12m | annual_turnover | cost_drag_pct_of_capital_per_year | excess_cagr | dsr | dsr_vs_index | final_equity | killed_on |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| benchmark_buy_hold | 0.1433 | 0.1672 | 0.885 | -0.3372 | -0.1973 | 0.08 | 0.0 | 0.0 | 0.95 | None | 2478.45 | None |
| stable_only | 0.1004 | 0.124 | 0.834 | -0.2623 | -0.2398 | 5.11 | 0.0047 | -0.0429 | 0.928 | 0.006 | 1568.35 | None |
| active_only | 0.0688 | 0.1738 | 0.47 | -0.3689 | -0.2661 | 16.97 | 0.0126 | -0.0745 | 0.595 | 0.0 | 1107.5 | None |
| blend_fixed_90 | 0.0982 | 0.1213 | 0.833 | -0.2593 | -0.2373 | 6.39 | 0.0058 | -0.0451 | 0.928 | 0.003 | 1531.3 | None |
| blend_fixed_80 | 0.0958 | 0.1206 | 0.819 | -0.2569 | -0.2351 | 7.65 | 0.0069 | -0.0475 | 0.921 | 0.002 | 1492.05 | None |
| blend_fixed_70 | 0.0932 | 0.1219 | 0.793 | -0.2569 | -0.2333 | 8.9 | 0.0079 | -0.0501 | 0.908 | 0.001 | 1450.9 | None |
| blend_fixed_60 | 0.0905 | 0.125 | 0.756 | -0.2577 | -0.2318 | 10.14 | 0.0088 | -0.0528 | 0.886 | 0.0 | 1407.95 | None |
| blend_fixed_50 | 0.0876 | 0.1299 | 0.711 | -0.2607 | -0.2307 | 11.36 | 0.0096 | -0.0557 | 0.855 | 0.0 | 1363.5 | None |
| blend_vol_target | 0.0876 | 0.1246 | 0.737 | -0.2577 | -0.2318 | 10.15 | 0.0087 | -0.0557 | 0.873 | 0.0 | 1364.25 | None |
| blend_drawdown_throttle | 0.0906 | 0.1212 | 0.776 | -0.2628 | -0.241 | 8.71 | 0.0075 | -0.0527 | 0.898 | 0.001 | 1409.05 | None |

## Walk-forward choices for the active sleeve

| train | test | chosen params | train Sharpe |
|---|---|---|---|
| 2008-01-14..2013-01-14 | 2013-01-14..2014-01-14 | `{'top_n': 3}` | 0.112 |
| 2009-01-14..2014-01-14 | 2014-01-14..2015-01-14 | `{'top_n': 3}` | 0.394 |
| 2010-01-14..2015-01-14 | 2015-01-14..2016-01-14 | `{'top_n': 3}` | 0.588 |
| 2011-01-14..2016-01-14 | 2016-01-14..2017-01-14 | `{'top_n': 2}` | 0.43 |
| 2012-01-14..2017-01-14 | 2017-01-14..2018-01-14 | `{'top_n': 3}` | 0.544 |
| 2013-01-14..2018-01-14 | 2018-01-14..2019-01-14 | `{'top_n': 3}` | 0.733 |
| 2014-01-14..2019-01-14 | 2019-01-14..2020-01-14 | `{'top_n': 3}` | 0.321 |
| 2015-01-14..2020-01-14 | 2020-01-14..2021-01-14 | `{'top_n': 3}` | 0.435 |
| 2016-01-14..2021-01-14 | 2021-01-14..2022-01-14 | `{'top_n': 3}` | 0.587 |
| 2017-01-14..2022-01-14 | 2022-01-14..2023-01-14 | `{'top_n': 2}` | 0.824 |
| 2018-01-14..2023-01-14 | 2023-01-14..2024-01-14 | `{'top_n': 3}` | 0.434 |
| 2019-01-14..2024-01-14 | 2024-01-14..2024-12-31 | `{'top_n': 2}` | 0.582 |

## Data fixes applied

- none

## How to read this

- `dsr` (Deflated Sharpe Ratio) is the probability the Sharpe is real after accounting for how many variants were tried. `dsr_vs_index` asks the same of the edge over the index; the promotion gate needs `dsr_vs_index` > 0.95.
- `cost_drag_pct_of_capital_per_year` is fees and slippage as a share of starting capital.
- `excess_cagr` is versus simply holding the benchmark (benchmark has no kill switch).
- `killed_on`: date the $-loss kill switch fired and the variant went to cash for good.
