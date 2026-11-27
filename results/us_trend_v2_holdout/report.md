# Experiment report: us_trend_v2

> Research output, not financial advice. Backtests are simulations on past data and do not guarantee future results.

- Run: `20261127T061247Z-0f5600` · commit `9985416` · data `fca7a1a82993`
- Out-of-sample window: 2025-01-01 to 2026-11-25 (walk-forward; holdout OPENED from 2025-01-01)
- Capital $500, kill switch at $250 loss, fractional shares, costs: us model
- Trials counted for this family so far: 102

## Results (out-of-sample only)

| variant | cagr | vol | sharpe | max_drawdown | worst_12m | annual_turnover | cost_drag_pct_of_capital_per_year | excess_cagr | dsr | dsr_vs_index | final_equity | killed_on |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| benchmark_buy_hold | 0.1219 | 0.1765 | 0.739 | -0.1875 | 0.0522 | 0.52 | 0.0003 | 0.0 | 0.688 | None | 621.65 | None |
| stable_only | 0.0854 | 0.1335 | 0.681 | -0.1146 | 0.0264 | 5.78 | 0.0031 | -0.0365 | 0.655 | 0.159 | 583.9 | None |
| active_only | 0.0672 | 0.1996 | 0.426 | -0.2384 | -0.0849 | 5.56 | 0.0035 | -0.0547 | 0.52 | 0.172 | 565.5 | None |
| blend_fixed_90 | 0.0852 | 0.1325 | 0.683 | -0.1191 | 0.0159 | 5.91 | 0.0032 | -0.0367 | 0.656 | 0.151 | 583.65 | None |
| blend_fixed_80 | 0.0846 | 0.1335 | 0.675 | -0.1249 | 0.0053 | 6.01 | 0.0033 | -0.0373 | 0.652 | 0.145 | 583.1 | None |
| blend_fixed_70 | 0.0838 | 0.1366 | 0.657 | -0.1308 | -0.0054 | 6.09 | 0.0034 | -0.0381 | 0.643 | 0.142 | 582.25 | None |
| blend_fixed_60 | 0.0827 | 0.1416 | 0.632 | -0.1366 | -0.0163 | 6.15 | 0.0035 | -0.0392 | 0.63 | 0.142 | 581.1 | None |
| blend_fixed_50 | 0.0812 | 0.1482 | 0.601 | -0.1424 | -0.0273 | 6.18 | 0.0036 | -0.0407 | 0.614 | 0.144 | 579.65 | None |
| blend_vol_target | 0.0827 | 0.1416 | 0.632 | -0.1366 | -0.0163 | 6.15 | 0.0035 | -0.0392 | 0.63 | 0.142 | 581.1 | None |
| blend_drawdown_throttle | 0.0805 | 0.136 | 0.638 | -0.1308 | -0.0111 | 6.31 | 0.0036 | -0.0414 | 0.633 | 0.133 | 578.95 | None |

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
| 2019-01-14..2024-01-14 | 2024-01-14..2025-01-14 | `{'lookback': 252, 'top_n': 4}` | 0.804 |
| 2020-01-14..2025-01-14 | 2025-01-14..2026-01-14 | `{'lookback': 252, 'top_n': 4}` | 0.749 |
| 2021-01-14..2026-01-14 | 2026-01-14..2026-11-25 | `{'lookback': 252, 'top_n': 2}` | 1.04 |

## Data fixes applied

- none

## How to read this

- `dsr` (Deflated Sharpe Ratio) is the probability the Sharpe is real after accounting for how many variants were tried. `dsr_vs_index` asks the same of the edge over the index; the promotion gate needs `dsr_vs_index` > 0.95.
- `cost_drag_pct_of_capital_per_year` is fees and slippage as a share of starting capital.
- `excess_cagr` is versus simply holding the benchmark (benchmark has no kill switch).
- `killed_on`: date the $-loss kill switch fired and the variant went to cash for good.
