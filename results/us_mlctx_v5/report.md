# Experiment report: us_mlctx_v5

> Research output, not financial advice. Backtests are simulations on past data and do not guarantee future results.

- Run: `20261128T092058Z-f57cbd` · commit `470c8c4` · data `1fcd6bdd9304`
- Out-of-sample window: 2013-01-14 to 2024-12-31 (walk-forward; holdout sealed from 2025-01-01)
- Capital $500, kill switch at $250 loss, fractional shares, costs: us model
- Trials counted for this family so far: 130

## Results (out-of-sample only)

| variant | cagr | vol | sharpe | max_drawdown | worst_12m | annual_turnover | cost_drag_pct_of_capital_per_year | excess_cagr | dsr | dsr_vs_index | final_equity | killed_on |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| benchmark_buy_hold | 0.1432 | 0.1671 | 0.885 | -0.337 | -0.1973 | 0.08 | 0.0 | 0.0 | 0.946 | None | 2476.7 | None |
| stable_only | 0.1003 | 0.1239 | 0.834 | -0.2621 | -0.2396 | 5.1 | 0.0047 | -0.0429 | 0.923 | 0.005 | 1567.05 | None |
| active_only | 0.1024 | 0.1915 | 0.606 | -0.4625 | -0.3108 | 16.48 | 0.015 | -0.0408 | 0.746 | 0.008 | 1603.5 | None |
| blend_fixed_90 | 0.1013 | 0.1216 | 0.855 | -0.2506 | -0.233 | 6.14 | 0.0057 | -0.0419 | 0.932 | 0.004 | 1583.7 | None |
| blend_fixed_80 | 0.1029 | 0.1215 | 0.868 | -0.2464 | -0.2267 | 7.23 | 0.0068 | -0.0403 | 0.938 | 0.003 | 1612.55 | None |
| blend_fixed_70 | 0.1036 | 0.1238 | 0.859 | -0.2478 | -0.2248 | 8.39 | 0.0079 | -0.0396 | 0.934 | 0.002 | 1624.55 | None |
| blend_fixed_60 | 0.1049 | 0.129 | 0.838 | -0.26 | -0.2242 | 9.55 | 0.009 | -0.0383 | 0.925 | 0.002 | 1647.35 | None |
| blend_fixed_50 | 0.105 | 0.1359 | 0.803 | -0.2931 | -0.2244 | 10.68 | 0.01 | -0.0382 | 0.908 | 0.002 | 1649.65 | None |
| blend_vol_target | 0.101 | 0.1267 | 0.823 | -0.26 | -0.2242 | 9.56 | 0.0088 | -0.0422 | 0.918 | 0.001 | 1579.45 | None |
| blend_drawdown_throttle | 0.0997 | 0.1204 | 0.85 | -0.2559 | -0.2387 | 8.43 | 0.0078 | -0.0435 | 0.93 | 0.002 | 1556.75 | None |

## Walk-forward choices for the active sleeve

| train | test | chosen params | train Sharpe |
|---|---|---|---|
| 2008-01-14..2013-01-14 | 2013-01-14..2014-01-14 | `{'top_n': 2}` | 0.19 |
| 2009-01-14..2014-01-14 | 2014-01-14..2015-01-14 | `{'top_n': 3}` | 0.562 |
| 2010-01-14..2015-01-14 | 2015-01-14..2016-01-14 | `{'top_n': 3}` | 0.631 |
| 2011-01-14..2016-01-14 | 2016-01-14..2017-01-14 | `{'top_n': 3}` | 0.243 |
| 2012-01-14..2017-01-14 | 2017-01-14..2018-01-14 | `{'top_n': 3}` | 0.595 |
| 2013-01-14..2018-01-14 | 2018-01-14..2019-01-14 | `{'top_n': 3}` | 0.858 |
| 2014-01-14..2019-01-14 | 2019-01-14..2020-01-14 | `{'top_n': 3}` | 0.366 |
| 2015-01-14..2020-01-14 | 2020-01-14..2021-01-14 | `{'top_n': 2}` | 0.771 |
| 2016-01-14..2021-01-14 | 2021-01-14..2022-01-14 | `{'top_n': 2}` | 0.638 |
| 2017-01-14..2022-01-14 | 2022-01-14..2023-01-14 | `{'top_n': 2}` | 0.865 |
| 2018-01-14..2023-01-14 | 2023-01-14..2024-01-14 | `{'top_n': 2}` | 0.57 |
| 2019-01-14..2024-01-14 | 2024-01-14..2024-12-31 | `{'top_n': 2}` | 0.691 |

## Data fixes applied

- none

## How to read this

- `dsr` (Deflated Sharpe Ratio) is the probability the Sharpe is real after accounting for how many variants were tried. `dsr_vs_index` asks the same of the edge over the index; the promotion gate needs `dsr_vs_index` > 0.95.
- `cost_drag_pct_of_capital_per_year` is fees and slippage as a share of starting capital.
- `excess_cagr` is versus simply holding the benchmark (benchmark has no kill switch).
- `killed_on`: date the $-loss kill switch fired and the variant went to cash for good.
