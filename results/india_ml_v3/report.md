# Experiment report: india_ml_v3

> Research output, not financial advice. Backtests are simulations on past data and do not guarantee future results.

- Run: `20261128T091855Z-e57844` · commit `470c8c4` · data `4c844c48ddd5`
- Out-of-sample window: 2014-01-11 to 2024-12-31 (walk-forward; holdout sealed from 2025-01-01)
- Capital Rs 44,000, kill switch at Rs 22000 loss, whole shares, costs: india model
- Trials counted for this family so far: 130

## Results (out-of-sample only)

| variant | cagr | vol | sharpe | max_drawdown | worst_12m | annual_turnover | cost_drag_pct_of_capital_per_year | excess_cagr | dsr | dsr_vs_index | final_equity | killed_on |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| benchmark_buy_hold | 0.1424 | 0.148 | 0.974 | -0.3633 | -0.2875 | 0.09 | 0.0002 | 0.0 | 0.439 | None | 183546.0 | None |
| stable_only | 0.1336 | 0.1312 | 1.022 | -0.215 | -0.1462 | 5.7 | 0.0242 | -0.0088 | 0.5 | 0.0 | 168951.2 | None |
| active_only | 0.1539 | 0.2171 | 0.769 | -0.5027 | -0.4542 | 15.24 | 0.1184 | 0.0115 | 0.207 | 0.002 | 204349.2 | None |
| blend_fixed_90 | 0.1245 | 0.1267 | 0.99 | -0.2471 | -0.1515 | 6.68 | 0.047 | -0.0179 | 0.458 | 0.0 | 154998.8 | None |
| blend_fixed_80 | 0.1258 | 0.127 | 0.997 | -0.2775 | -0.1645 | 7.88 | 0.0578 | -0.0166 | 0.467 | 0.0 | 156908.4 | None |
| blend_fixed_70 | 0.1272 | 0.1308 | 0.981 | -0.312 | -0.2069 | 9.1 | 0.068 | -0.0152 | 0.447 | 0.0 | 158980.8 | None |
| blend_fixed_60 | 0.128 | 0.1371 | 0.947 | -0.343 | -0.25 | 10.12 | 0.0758 | -0.0144 | 0.405 | 0.0 | 160173.2 | None |
| blend_fixed_50 | 0.1283 | 0.1464 | 0.898 | -0.3714 | -0.2856 | 11.19 | 0.0833 | -0.0141 | 0.345 | 0.0 | 160644.0 | None |
| blend_vol_target | 0.1248 | 0.1362 | 0.932 | -0.343 | -0.25 | 10.11 | 0.0751 | -0.0176 | 0.386 | 0.0 | 155408.0 | None |
| blend_drawdown_throttle | 0.126 | 0.1289 | 0.985 | -0.2743 | -0.1646 | 8.79 | 0.0653 | -0.0164 | 0.453 | 0.0 | 157256.0 | None |

## Walk-forward choices for the active sleeve

| train | test | chosen params | train Sharpe |
|---|---|---|---|
| 2009-01-11..2014-01-11 | 2014-01-11..2015-01-11 | `{'top_n': 2}` | 0.978 |
| 2010-01-11..2015-01-11 | 2015-01-11..2016-01-11 | `{'top_n': 3}` | 1.39 |
| 2011-01-11..2016-01-11 | 2016-01-11..2017-01-11 | `{'top_n': 3}` | 1.369 |
| 2012-01-11..2017-01-11 | 2017-01-11..2018-01-11 | `{'top_n': 3}` | 1.555 |
| 2013-01-11..2018-01-11 | 2018-01-11..2019-01-11 | `{'top_n': 3}` | 1.683 |
| 2014-01-11..2019-01-11 | 2019-01-11..2020-01-11 | `{'top_n': 3}` | 1.528 |
| 2015-01-11..2020-01-11 | 2020-01-11..2021-01-11 | `{'top_n': 3}` | 0.657 |
| 2016-01-11..2021-01-11 | 2021-01-11..2022-01-11 | `{'top_n': 3}` | 0.705 |
| 2017-01-11..2022-01-11 | 2022-01-11..2023-01-11 | `{'top_n': 3}` | 0.696 |
| 2018-01-11..2023-01-11 | 2023-01-11..2024-01-11 | `{'top_n': 2}` | 0.45 |
| 2019-01-11..2024-01-11 | 2024-01-11..2024-12-31 | `{'top_n': 2}` | 0.364 |

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
