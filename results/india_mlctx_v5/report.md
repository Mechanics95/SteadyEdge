# Experiment report: india_mlctx_v5

> Research output, not financial advice. Backtests are simulations on past data and do not guarantee future results.

- Run: `20261128T091918Z-1d6b05` · commit `470c8c4` · data `787fcca657a3`
- Out-of-sample window: 2014-01-11 to 2024-12-31 (walk-forward; holdout sealed from 2025-01-01)
- Capital Rs 44,000, kill switch at Rs 22000 loss, whole shares, costs: india model
- Trials counted for this family so far: 130

## Results (out-of-sample only)

| variant | cagr | vol | sharpe | max_drawdown | worst_12m | annual_turnover | cost_drag_pct_of_capital_per_year | excess_cagr | dsr | dsr_vs_index | final_equity | killed_on |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| benchmark_buy_hold | 0.1423 | 0.1479 | 0.974 | -0.3631 | -0.2873 | 0.09 | 0.0002 | 0.0 | 0.439 | None | 183348.0 | None |
| stable_only | 0.1335 | 0.131 | 1.022 | -0.2146 | -0.146 | 5.69 | 0.0242 | -0.0088 | 0.5 | 0.0 | 168731.2 | None |
| active_only | 0.1108 | 0.2075 | 0.61 | -0.3809 | -0.2743 | 13.5 | 0.0618 | -0.0315 | 0.088 | 0.0 | 135863.2 | None |
| blend_fixed_90 | 0.1275 | 0.126 | 1.015 | -0.2074 | -0.1382 | 6.08 | 0.0309 | -0.0148 | 0.491 | 0.0 | 159394.4 | None |
| blend_fixed_80 | 0.1261 | 0.1258 | 1.007 | -0.2243 | -0.1326 | 7.04 | 0.0371 | -0.0162 | 0.48 | 0.0 | 157313.2 | None |
| blend_fixed_70 | 0.1302 | 0.1277 | 1.023 | -0.2131 | -0.128 | 7.96 | 0.0426 | -0.0121 | 0.501 | 0.0 | 163565.6 | None |
| blend_fixed_60 | 0.1281 | 0.1329 | 0.973 | -0.2343 | -0.1424 | 8.72 | 0.046 | -0.0142 | 0.437 | 0.0 | 160388.8 | None |
| blend_fixed_50 | 0.1246 | 0.1406 | 0.906 | -0.2501 | -0.1579 | 9.56 | 0.0495 | -0.0177 | 0.353 | 0.0 | 155188.0 | None |
| blend_vol_target | 0.1242 | 0.1313 | 0.958 | -0.2343 | -0.1424 | 8.7 | 0.0452 | -0.0181 | 0.418 | 0.0 | 154589.6 | None |
| blend_drawdown_throttle | 0.1225 | 0.1263 | 0.978 | -0.2443 | -0.1439 | 8.04 | 0.0418 | -0.0198 | 0.443 | 0.0 | 152020.0 | None |

## Walk-forward choices for the active sleeve

| train | test | chosen params | train Sharpe |
|---|---|---|---|
| 2009-01-11..2014-01-11 | 2014-01-11..2015-01-11 | `{'top_n': 3}` | 0.515 |
| 2010-01-11..2015-01-11 | 2015-01-11..2016-01-11 | `{'top_n': 3}` | 0.792 |
| 2011-01-11..2016-01-11 | 2016-01-11..2017-01-11 | `{'top_n': 3}` | 0.57 |
| 2012-01-11..2017-01-11 | 2017-01-11..2018-01-11 | `{'top_n': 3}` | 0.85 |
| 2013-01-11..2018-01-11 | 2018-01-11..2019-01-11 | `{'top_n': 3}` | 0.646 |
| 2014-01-11..2019-01-11 | 2019-01-11..2020-01-11 | `{'top_n': 3}` | 0.61 |
| 2015-01-11..2020-01-11 | 2020-01-11..2021-01-11 | `{'top_n': 3}` | 0.439 |
| 2016-01-11..2021-01-11 | 2021-01-11..2022-01-11 | `{'top_n': 3}` | 0.739 |
| 2017-01-11..2022-01-11 | 2022-01-11..2023-01-11 | `{'top_n': 3}` | 0.805 |
| 2018-01-11..2023-01-11 | 2023-01-11..2024-01-11 | `{'top_n': 3}` | 0.455 |
| 2019-01-11..2024-01-11 | 2024-01-11..2024-12-31 | `{'top_n': 3}` | 0.625 |

## Data fixes applied

- GOLDBEES.NS 2019-12-19: one-day price-unit jump down by a factor of 100 (missing split adjustment or bad print); earlier prices rescaled to match
- GOLDBEES.NS 2019-12-23: one-day price-unit jump up by a factor of 100 (missing split adjustment or bad print); earlier prices rescaled to match
- NIFTYBEES.NS 2019-12-19: one-day price-unit jump down by a factor of 10 (missing split adjustment or bad print); earlier prices rescaled to match
- NIFTYBEES.NS 2019-12-23: one-day price-unit jump up by a factor of 10 (missing split adjustment or bad print); earlier prices rescaled to match

## How to read this

- `dsr` (Deflated Sharpe Ratio) is the probability the Sharpe is real after accounting for how many variants were tried. `dsr_vs_index` asks the same of the edge over the index; the promotion gate needs `dsr_vs_index` > 0.95.
- `cost_drag_pct_of_capital_per_year` is fees and slippage as a share of starting capital.
- `excess_cagr` is versus simply holding the benchmark (benchmark has no kill switch).
- `killed_on`: date the $-loss kill switch fired and the variant went to cash for good.
