# Experiment report: us_trend_v2

> Research output, not financial advice. Backtests are simulations on past data and do not guarantee future results.

- Run: `20261128T092131Z-7eec40` · commit `470c8c4` · data `6743928d2148`
- Out-of-sample window: 2013-01-14 to 2024-12-31 (walk-forward; holdout sealed from 2025-01-01)
- Capital $500, kill switch at $250 loss, fractional shares, costs: us model
- Trials counted for this family so far: 130

## Results (out-of-sample only)

| variant | cagr | vol | sharpe | max_drawdown | worst_12m | annual_turnover | cost_drag_pct_of_capital_per_year | excess_cagr | dsr | dsr_vs_index | final_equity | killed_on |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| benchmark_buy_hold | 0.1433 | 0.1672 | 0.885 | -0.3372 | -0.1973 | 0.08 | 0.0 | 0.0 | 0.946 | None | 2478.45 | None |
| stable_only | 0.1004 | 0.124 | 0.834 | -0.2623 | -0.2398 | 5.11 | 0.0047 | -0.0429 | 0.923 | 0.005 | 1568.35 | None |
| active_only | 0.1032 | 0.1727 | 0.655 | -0.2921 | -0.166 | 8.17 | 0.0078 | -0.0401 | 0.798 | 0.004 | 1617.0 | None |
| blend_fixed_90 | 0.1014 | 0.1218 | 0.855 | -0.2459 | -0.2203 | 5.51 | 0.0051 | -0.0419 | 0.933 | 0.004 | 1586.1 | None |
| blend_fixed_80 | 0.1023 | 0.1214 | 0.863 | -0.2293 | -0.2004 | 5.89 | 0.0055 | -0.041 | 0.937 | 0.003 | 1601.35 | None |
| blend_fixed_70 | 0.103 | 0.1228 | 0.86 | -0.2125 | -0.1803 | 6.26 | 0.0059 | -0.0403 | 0.935 | 0.002 | 1613.85 | None |
| blend_fixed_60 | 0.1035 | 0.126 | 0.845 | -0.1956 | -0.1599 | 6.62 | 0.0063 | -0.0398 | 0.929 | 0.002 | 1623.4 | None |
| blend_fixed_50 | 0.1039 | 0.1309 | 0.821 | -0.2009 | -0.1392 | 6.96 | 0.0066 | -0.0394 | 0.918 | 0.001 | 1630.1 | None |
| blend_vol_target | 0.1019 | 0.1261 | 0.833 | -0.1956 | -0.1599 | 6.65 | 0.0063 | -0.0414 | 0.923 | 0.001 | 1594.0 | None |
| blend_drawdown_throttle | 0.1009 | 0.1225 | 0.846 | -0.2125 | -0.1803 | 6.26 | 0.0059 | -0.0424 | 0.929 | 0.002 | 1577.85 | None |

## Walk-forward choices for the active sleeve

| train | test | chosen params | train Sharpe |
|---|---|---|---|
| 2008-01-14..2013-01-14 | 2013-01-14..2014-01-14 | `{'lookback': 252, 'top_n': 4}` | 0.448 |
| 2009-01-14..2014-01-14 | 2014-01-14..2015-01-14 | `{'lookback': 126, 'top_n': 4}` | 0.957 |
| 2010-01-14..2015-01-14 | 2015-01-14..2016-01-14 | `{'lookback': 126, 'top_n': 4}` | 0.845 |
| 2011-01-14..2016-01-14 | 2016-01-14..2017-01-14 | `{'lookback': 126, 'top_n': 4}` | 0.732 |
| 2012-01-14..2017-01-14 | 2017-01-14..2018-01-14 | `{'lookback': 252, 'top_n': 4}` | 0.813 |
| 2013-01-14..2018-01-14 | 2018-01-14..2019-01-14 | `{'lookback': 126, 'top_n': 4}` | 1.06 |
| 2014-01-14..2019-01-14 | 2019-01-14..2020-01-14 | `{'lookback': 126, 'top_n': 2}` | 0.698 |
| 2015-01-14..2020-01-14 | 2020-01-14..2021-01-14 | `{'lookback': 126, 'top_n': 2}` | 0.803 |
| 2016-01-14..2021-01-14 | 2021-01-14..2022-01-14 | `{'lookback': 126, 'top_n': 2}` | 0.775 |
| 2017-01-14..2022-01-14 | 2022-01-14..2023-01-14 | `{'lookback': 252, 'top_n': 4}` | 0.802 |
| 2018-01-14..2023-01-14 | 2023-01-14..2024-01-14 | `{'lookback': 252, 'top_n': 4}` | 0.605 |
| 2019-01-14..2024-01-14 | 2024-01-14..2024-12-31 | `{'lookback': 252, 'top_n': 4}` | 0.804 |

## Data fixes applied

- none

## How to read this

- `dsr` (Deflated Sharpe Ratio) is the probability the Sharpe is real after accounting for how many variants were tried. `dsr_vs_index` asks the same of the edge over the index; the promotion gate needs `dsr_vs_index` > 0.95.
- `cost_drag_pct_of_capital_per_year` is fees and slippage as a share of starting capital.
- `excess_cagr` is versus simply holding the benchmark (benchmark has no kill switch).
- `killed_on`: date the $-loss kill switch fired and the variant went to cash for good.
