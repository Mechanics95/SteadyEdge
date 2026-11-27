# Experiment report: us_sleeves_v1

> Research output, not financial advice. Backtests are simulations on past data and do not guarantee future results.

- Run: `20261127T053452Z-71c345` · commit `fdd648f` · data `2b8e21624a2b`
- Out-of-sample window: 2013-01-14 to 2024-12-31 (walk-forward; holdout sealed from 2025-01-01)
- Capital $500, kill switch at $250 loss, fractional shares, costs: us model
- Trials counted for this family so far: 16

## Results (out-of-sample only)

| variant | cagr | vol | sharpe | max_drawdown | worst_12m | annual_turnover | cost_drag_pct_of_capital_per_year | excess_cagr | dsr | dsr_vs_index | final_equity | killed_on |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| benchmark_buy_hold | 0.1433 | 0.1672 | 0.885 | -0.3372 | -0.1973 | 0.08 | 0.0 | 0.0 | 0.981 | None | 2478.45 | None |
| stable_only | 0.1433 | 0.1672 | 0.885 | -0.3372 | -0.1973 | 0.08 | 0.0 | 0.0 | 0.981 | None | 2478.45 | None |
| active_only | 0.1032 | 0.1727 | 0.655 | -0.2921 | -0.166 | 8.17 | 0.0078 | -0.0401 | 0.906 | 0.016 | 1617.0 | None |
| blend_fixed_90 | 0.1396 | 0.1651 | 0.875 | -0.3327 | -0.1828 | 0.91 | 0.001 | -0.0037 | 0.98 | 0.014 | 2384.15 | None |
| blend_fixed_80 | 0.1358 | 0.1636 | 0.861 | -0.3282 | -0.1805 | 1.74 | 0.0019 | -0.0075 | 0.977 | 0.014 | 2291.35 | None |
| blend_fixed_70 | 0.132 | 0.1626 | 0.844 | -0.3237 | -0.1783 | 2.56 | 0.0028 | -0.0113 | 0.974 | 0.015 | 2200.3 | None |
| blend_fixed_60 | 0.1281 | 0.1623 | 0.824 | -0.3192 | -0.1761 | 3.37 | 0.0036 | -0.0152 | 0.97 | 0.015 | 2111.05 | None |
| blend_fixed_50 | 0.1241 | 0.1626 | 0.801 | -0.3147 | -0.1742 | 4.18 | 0.0044 | -0.0192 | 0.964 | 0.015 | 2023.65 | None |
| blend_vol_target | 0.1293 | 0.1628 | 0.829 | -0.3192 | -0.1761 | 3.39 | 0.0037 | -0.014 | 0.971 | 0.016 | 2138.8 | None |
| blend_drawdown_throttle | 0.1319 | 0.1625 | 0.844 | -0.3237 | -0.1783 | 2.58 | 0.0028 | -0.0114 | 0.974 | 0.014 | 2198.2 | None |

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
