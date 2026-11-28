# Experiment report: us_mlctx_v5

> Research output, not financial advice. Backtests are simulations on past data and do not guarantee future results.

- Run: `20261128T045525Z-ae3143` · commit `b398cf4` · data `289c362a192b`
- Out-of-sample window: 2013-01-14 to 2024-12-31 (walk-forward; holdout sealed from 2025-01-01)
- Capital $500, kill switch at $250 loss, fractional shares, costs: us model
- Trials counted for this family so far: 130

## Results (out-of-sample only)

| variant | cagr | vol | sharpe | max_drawdown | worst_12m | annual_turnover | cost_drag_pct_of_capital_per_year | excess_cagr | dsr | dsr_vs_index | final_equity | killed_on |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| benchmark_buy_hold | 0.1432 | 0.1671 | 0.885 | -0.337 | -0.1973 | 0.08 | 0.0 | 0.0 | 0.946 | None | 2476.7 | None |
| stable_only | 0.1003 | 0.1239 | 0.834 | -0.2621 | -0.2396 | 5.1 | 0.0047 | -0.0429 | 0.923 | 0.005 | 1567.05 | None |
| active_only | 0.1084 | 0.1909 | 0.635 | -0.4625 | -0.2918 | 17.33 | 0.0157 | -0.0348 | 0.776 | 0.013 | 1710.35 | None |
| blend_fixed_90 | 0.1021 | 0.1214 | 0.862 | -0.2486 | -0.2307 | 6.22 | 0.0058 | -0.0411 | 0.936 | 0.004 | 1598.8 | None |
| blend_fixed_80 | 0.1045 | 0.1211 | 0.882 | -0.2436 | -0.2239 | 7.43 | 0.007 | -0.0387 | 0.943 | 0.003 | 1640.85 | None |
| blend_fixed_70 | 0.1054 | 0.1235 | 0.874 | -0.2417 | -0.2185 | 8.62 | 0.0081 | -0.0378 | 0.94 | 0.003 | 1656.8 | None |
| blend_fixed_60 | 0.1077 | 0.1286 | 0.86 | -0.2621 | -0.2141 | 9.89 | 0.0093 | -0.0355 | 0.935 | 0.002 | 1697.15 | None |
| blend_fixed_50 | 0.1079 | 0.1354 | 0.825 | -0.295 | -0.213 | 11.12 | 0.0104 | -0.0353 | 0.919 | 0.002 | 1702.5 | None |
| blend_vol_target | 0.1038 | 0.1264 | 0.845 | -0.2621 | -0.2151 | 9.91 | 0.0091 | -0.0394 | 0.928 | 0.002 | 1628.15 | None |
| blend_drawdown_throttle | 0.1016 | 0.1201 | 0.866 | -0.2525 | -0.2347 | 8.57 | 0.0079 | -0.0416 | 0.937 | 0.003 | 1590.05 | None |

## Walk-forward choices for the active sleeve

| train | test | chosen params | train Sharpe |
|---|---|---|---|
| 2008-01-14..2013-01-14 | 2013-01-14..2014-01-14 | `{'top_n': 2}` | 0.182 |
| 2009-01-14..2014-01-14 | 2014-01-14..2015-01-14 | `{'top_n': 3}` | 0.507 |
| 2010-01-14..2015-01-14 | 2015-01-14..2016-01-14 | `{'top_n': 3}` | 0.587 |
| 2011-01-14..2016-01-14 | 2016-01-14..2017-01-14 | `{'top_n': 3}` | 0.25 |
| 2012-01-14..2017-01-14 | 2017-01-14..2018-01-14 | `{'top_n': 3}` | 0.605 |
| 2013-01-14..2018-01-14 | 2018-01-14..2019-01-14 | `{'top_n': 3}` | 0.86 |
| 2014-01-14..2019-01-14 | 2019-01-14..2020-01-14 | `{'top_n': 2}` | 0.47 |
| 2015-01-14..2020-01-14 | 2020-01-14..2021-01-14 | `{'top_n': 2}` | 0.818 |
| 2016-01-14..2021-01-14 | 2021-01-14..2022-01-14 | `{'top_n': 2}` | 0.615 |
| 2017-01-14..2022-01-14 | 2022-01-14..2023-01-14 | `{'top_n': 2}` | 0.891 |
| 2018-01-14..2023-01-14 | 2023-01-14..2024-01-14 | `{'top_n': 2}` | 0.612 |
| 2019-01-14..2024-01-14 | 2024-01-14..2024-12-31 | `{'top_n': 2}` | 0.775 |

## Data fixes applied

- none

## How to read this

- `dsr` (Deflated Sharpe Ratio) is the probability the Sharpe is real after accounting for how many variants were tried. `dsr_vs_index` asks the same of the edge over the index; the promotion gate needs `dsr_vs_index` > 0.95.
- `cost_drag_pct_of_capital_per_year` is fees and slippage as a share of starting capital.
- `excess_cagr` is versus simply holding the benchmark (benchmark has no kill switch).
- `killed_on`: date the $-loss kill switch fired and the variant went to cash for good.
