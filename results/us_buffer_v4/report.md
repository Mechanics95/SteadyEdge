# Experiment report: us_buffer_v4

> Research output, not financial advice. Backtests are simulations on past data and do not guarantee future results.

- Run: `20261128T045449Z-3ce290` · commit `b398cf4` · data `5de1f6fb7000`
- Out-of-sample window: 2013-01-14 to 2024-12-31 (walk-forward; holdout sealed from 2025-01-01)
- Capital $500, kill switch at $250 loss, fractional shares, costs: us model
- Trials counted for this family so far: 118

## Results (out-of-sample only)

| variant | cagr | vol | sharpe | max_drawdown | worst_12m | annual_turnover | cost_drag_pct_of_capital_per_year | excess_cagr | dsr | dsr_vs_index | final_equity | killed_on |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| benchmark_buy_hold | 0.1432 | 0.1671 | 0.885 | -0.337 | -0.1973 | 0.08 | 0.0 | 0.0 | 0.95 | None | 2476.7 | None |
| stable_only | 0.1003 | 0.1239 | 0.834 | -0.2621 | -0.2396 | 5.1 | 0.0047 | -0.0429 | 0.928 | 0.006 | 1567.0 | None |
| active_only | 0.0901 | 0.1729 | 0.586 | -0.3368 | -0.205 | 5.03 | 0.0045 | -0.0531 | 0.737 | 0.001 | 1402.1 | None |
| blend_fixed_90 | 0.0977 | 0.1169 | 0.856 | -0.2478 | -0.2202 | 4.81 | 0.0044 | -0.0455 | 0.938 | 0.004 | 1523.7 | None |
| blend_fixed_80 | 0.0993 | 0.1209 | 0.844 | -0.2367 | -0.2067 | 5.07 | 0.0047 | -0.0439 | 0.933 | 0.003 | 1550.05 | None |
| blend_fixed_70 | 0.0984 | 0.1222 | 0.829 | -0.2289 | -0.1953 | 5.04 | 0.0047 | -0.0448 | 0.927 | 0.002 | 1535.25 | None |
| blend_fixed_60 | 0.0974 | 0.125 | 0.807 | -0.2192 | -0.1811 | 5.06 | 0.0047 | -0.0458 | 0.916 | 0.001 | 1519.2 | None |
| blend_fixed_50 | 0.0959 | 0.13 | 0.77 | -0.2216 | -0.1686 | 5.05 | 0.0046 | -0.0473 | 0.895 | 0.0 | 1493.55 | None |
| blend_vol_target | 0.0955 | 0.1254 | 0.791 | -0.2212 | -0.1829 | 5.1 | 0.0047 | -0.0477 | 0.907 | 0.001 | 1488.2 | None |
| blend_drawdown_throttle | 0.0939 | 0.1225 | 0.794 | -0.2426 | -0.2039 | 5.38 | 0.0049 | -0.0493 | 0.909 | 0.001 | 1461.1 | None |

## Walk-forward choices for the active sleeve

| train | test | chosen params | train Sharpe |
|---|---|---|---|
| 2008-01-14..2013-01-14 | 2013-01-14..2014-01-14 | `{'lookback': 252, 'top_n': 3}` | 0.383 |
| 2009-01-14..2014-01-14 | 2014-01-14..2015-01-14 | `{'lookback': 126, 'top_n': 4}` | 0.964 |
| 2010-01-14..2015-01-14 | 2015-01-14..2016-01-14 | `{'lookback': 126, 'top_n': 4}` | 0.869 |
| 2011-01-14..2016-01-14 | 2016-01-14..2017-01-14 | `{'lookback': 126, 'top_n': 4}` | 0.666 |
| 2012-01-14..2017-01-14 | 2017-01-14..2018-01-14 | `{'lookback': 252, 'top_n': 4}` | 0.83 |
| 2013-01-14..2018-01-14 | 2018-01-14..2019-01-14 | `{'lookback': 252, 'top_n': 4}` | 1.072 |
| 2014-01-14..2019-01-14 | 2019-01-14..2020-01-14 | `{'lookback': 126, 'top_n': 3}` | 0.608 |
| 2015-01-14..2020-01-14 | 2020-01-14..2021-01-14 | `{'lookback': 126, 'top_n': 3}` | 0.811 |
| 2016-01-14..2021-01-14 | 2021-01-14..2022-01-14 | `{'lookback': 126, 'top_n': 4}` | 0.766 |
| 2017-01-14..2022-01-14 | 2022-01-14..2023-01-14 | `{'lookback': 252, 'top_n': 4}` | 0.82 |
| 2018-01-14..2023-01-14 | 2023-01-14..2024-01-14 | `{'lookback': 252, 'top_n': 2}` | 0.581 |
| 2019-01-14..2024-01-14 | 2024-01-14..2024-12-31 | `{'lookback': 252, 'top_n': 2}` | 0.705 |

## Data fixes applied

- none

## How to read this

- `dsr` (Deflated Sharpe Ratio) is the probability the Sharpe is real after accounting for how many variants were tried. `dsr_vs_index` asks the same of the edge over the index; the promotion gate needs `dsr_vs_index` > 0.95.
- `cost_drag_pct_of_capital_per_year` is fees and slippage as a share of starting capital.
- `excess_cagr` is versus simply holding the benchmark (benchmark has no kill switch).
- `killed_on`: date the $-loss kill switch fired and the variant went to cash for good.
