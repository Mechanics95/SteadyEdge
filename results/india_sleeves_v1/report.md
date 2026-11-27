# Experiment report: india_sleeves_v1

> Research output, not financial advice. Backtests are simulations on past data and do not guarantee future results.

- Run: `20261127T053512Z-6cdd7a` · commit `fdd648f` · data `363e0db6f47a`
- Out-of-sample window: 2014-01-11 to 2024-12-31 (walk-forward; holdout sealed from 2025-01-01)
- Capital Rs 44,000, kill switch at Rs 22000 loss, whole shares, costs: india model
- Trials counted for this family so far: 16

## Results (out-of-sample only)

| variant | cagr | vol | sharpe | max_drawdown | worst_12m | annual_turnover | cost_drag_pct_of_capital_per_year | excess_cagr | dsr | dsr_vs_index | final_equity | killed_on |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| benchmark_buy_hold | 0.1424 | 0.148 | 0.974 | -0.3633 | -0.2875 | 0.09 | 0.0002 | 0.0 | 0.996 | None | 183546.0 | None |
| stable_only | 0.1424 | 0.148 | 0.974 | -0.3633 | -0.2875 | 0.09 | 0.0002 | 0.0 | 0.996 | None | 183546.0 | None |
| active_only | 0.1775 | 0.2062 | 0.896 | -0.3678 | -0.241 | 7.42 | 0.0491 | 0.0351 | 0.993 | 0.681 | 254122.0 | None |
| blend_fixed_90 | 0.1413 | 0.1457 | 0.981 | -0.3577 | -0.2816 | 0.73 | 0.011 | -0.0011 | 0.996 | 0.236 | 181759.6 | None |
| blend_fixed_80 | 0.1473 | 0.1475 | 1.006 | -0.3571 | -0.2775 | 1.54 | 0.0161 | 0.0049 | 0.997 | 0.526 | 192306.4 | None |
| blend_fixed_70 | 0.1502 | 0.1508 | 1.004 | -0.3544 | -0.2693 | 2.28 | 0.0197 | 0.0078 | 0.997 | 0.55 | 197586.4 | None |
| blend_fixed_60 | 0.1561 | 0.1554 | 1.012 | -0.3535 | -0.2625 | 3.06 | 0.0244 | 0.0137 | 0.997 | 0.622 | 208736.0 | None |
| blend_fixed_50 | 0.1607 | 0.1614 | 1.005 | -0.3562 | -0.257 | 3.81 | 0.0286 | 0.0183 | 0.997 | 0.648 | 217734.0 | None |
| blend_vol_target | 0.1575 | 0.1557 | 1.018 | -0.3535 | -0.2625 | 3.07 | 0.0246 | 0.0151 | 0.997 | 0.65 | 211283.6 | None |
| blend_drawdown_throttle | 0.1463 | 0.1511 | 0.98 | -0.3573 | -0.2741 | 2.28 | 0.0198 | 0.0039 | 0.996 | 0.462 | 190462.8 | None |

## Walk-forward choices for the active sleeve

| train | test | chosen params | train Sharpe |
|---|---|---|---|
| 2009-01-11..2014-01-11 | 2014-01-11..2015-01-11 | `{'lookback': 126, 'top_n': 3}` | 1.621 |
| 2010-01-11..2015-01-11 | 2015-01-11..2016-01-11 | `{'lookback': 126, 'top_n': 4}` | 1.696 |
| 2011-01-11..2016-01-11 | 2016-01-11..2017-01-11 | `{'lookback': 252, 'top_n': 2}` | 1.337 |
| 2012-01-11..2017-01-11 | 2017-01-11..2018-01-11 | `{'lookback': 252, 'top_n': 2}` | 1.302 |
| 2013-01-11..2018-01-11 | 2018-01-11..2019-01-11 | `{'lookback': 126, 'top_n': 4}` | 1.636 |
| 2014-01-11..2019-01-11 | 2019-01-11..2020-01-11 | `{'lookback': 252, 'top_n': 4}` | 1.51 |
| 2015-01-11..2020-01-11 | 2020-01-11..2021-01-11 | `{'lookback': 252, 'top_n': 4}` | 1.392 |
| 2016-01-11..2021-01-11 | 2021-01-11..2022-01-11 | `{'lookback': 252, 'top_n': 4}` | 0.959 |
| 2017-01-11..2022-01-11 | 2022-01-11..2023-01-11 | `{'lookback': 252, 'top_n': 4}` | 1.29 |
| 2018-01-11..2023-01-11 | 2023-01-11..2024-01-11 | `{'lookback': 252, 'top_n': 4}` | 0.709 |
| 2019-01-11..2024-01-11 | 2024-01-11..2024-12-31 | `{'lookback': 252, 'top_n': 4}` | 0.844 |

## Data fixes applied

- GOLDBEES.NS 2019-12-19: unadjusted split 1:100 detected; earlier prices adjusted
- GOLDBEES.NS 2019-12-23: unadjusted reverse split 1:100 detected; earlier prices adjusted
- NIFTYBEES.NS 2019-12-19: unadjusted split 1:10 detected; earlier prices adjusted
- NIFTYBEES.NS 2019-12-23: unadjusted reverse split 1:10 detected; earlier prices adjusted

## How to read this

- `dsr` (Deflated Sharpe Ratio) is the probability the Sharpe is real after accounting for how many variants were tried. `dsr_vs_index` asks the same of the edge over the index; the promotion gate needs `dsr_vs_index` > 0.95.
- `cost_drag_pct_of_capital_per_year` is fees and slippage as a share of starting capital.
- `excess_cagr` is versus simply holding the benchmark (benchmark has no kill switch).
- `killed_on`: date the $-loss kill switch fired and the variant went to cash for good.
