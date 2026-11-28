# Experiment report: india_buffer_v4

> Research output, not financial advice. Backtests are simulations on past data and do not guarantee future results.

- Run: `20261128T045328Z-9ebff5` · commit `b398cf4` · data `5abe0a194f5b`
- Out-of-sample window: 2014-01-11 to 2024-12-31 (walk-forward; holdout sealed from 2025-01-01)
- Capital Rs 44,000, kill switch at Rs 22000 loss, whole shares, costs: india model
- Trials counted for this family so far: 118

## Results (out-of-sample only)

| variant | cagr | vol | sharpe | max_drawdown | worst_12m | annual_turnover | cost_drag_pct_of_capital_per_year | excess_cagr | dsr | dsr_vs_index | final_equity | killed_on |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| benchmark_buy_hold | 0.1423 | 0.1479 | 0.974 | -0.3631 | -0.2873 | 0.09 | 0.0002 | 0.0 | 0.396 | None | 183348.0 | None |
| stable_only | 0.1335 | 0.131 | 1.022 | -0.2146 | -0.146 | 5.69 | 0.0242 | -0.0088 | 0.454 | 0.0 | 168731.2 | None |
| active_only | 0.2237 | 0.2149 | 1.048 | -0.4221 | -0.2928 | 4.75 | 0.0406 | 0.0814 | 0.488 | 0.04 | 383869.2 | None |
| blend_fixed_90 | 0.1313 | 0.1238 | 1.059 | -0.2204 | -0.1397 | 5.3 | 0.0237 | -0.011 | 0.502 | 0.0 | 165308.0 | None |
| blend_fixed_80 | 0.1512 | 0.1274 | 1.17 | -0.2215 | -0.1288 | 5.42 | 0.0293 | 0.0089 | 0.641 | 0.0 | 199381.6 | None |
| blend_fixed_70 | 0.1586 | 0.1307 | 1.193 | -0.2273 | -0.13 | 5.32 | 0.0306 | 0.0163 | 0.668 | 0.001 | 213602.4 | None |
| blend_fixed_60 | 0.1661 | 0.1369 | 1.191 | -0.2436 | -0.157 | 5.25 | 0.0318 | 0.0238 | 0.666 | 0.003 | 228914.4 | None |
| blend_fixed_50 | 0.1794 | 0.1461 | 1.203 | -0.2754 | -0.1783 | 5.2 | 0.0343 | 0.0371 | 0.679 | 0.008 | 258451.6 | None |
| blend_vol_target | 0.166 | 0.1366 | 1.193 | -0.2436 | -0.157 | 5.27 | 0.032 | 0.0237 | 0.667 | 0.002 | 228562.4 | None |
| blend_drawdown_throttle | 0.1552 | 0.1306 | 1.171 | -0.2254 | -0.129 | 5.51 | 0.0307 | 0.0129 | 0.642 | 0.001 | 206993.6 | None |

## Walk-forward choices for the active sleeve

| train | test | chosen params | train Sharpe |
|---|---|---|---|
| 2009-01-11..2014-01-11 | 2014-01-11..2015-01-11 | `{'lookback': 126, 'top_n': 4}` | 1.679 |
| 2010-01-11..2015-01-11 | 2015-01-11..2016-01-11 | `{'lookback': 126, 'top_n': 4}` | 1.782 |
| 2011-01-11..2016-01-11 | 2016-01-11..2017-01-11 | `{'lookback': 252, 'top_n': 2}` | 1.703 |
| 2012-01-11..2017-01-11 | 2017-01-11..2018-01-11 | `{'lookback': 252, 'top_n': 2}` | 1.637 |
| 2013-01-11..2018-01-11 | 2018-01-11..2019-01-11 | `{'lookback': 252, 'top_n': 3}` | 1.835 |
| 2014-01-11..2019-01-11 | 2019-01-11..2020-01-11 | `{'lookback': 252, 'top_n': 3}` | 1.686 |
| 2015-01-11..2020-01-11 | 2020-01-11..2021-01-11 | `{'lookback': 252, 'top_n': 3}` | 1.362 |
| 2016-01-11..2021-01-11 | 2021-01-11..2022-01-11 | `{'lookback': 252, 'top_n': 4}` | 0.898 |
| 2017-01-11..2022-01-11 | 2022-01-11..2023-01-11 | `{'lookback': 252, 'top_n': 4}` | 1.308 |
| 2018-01-11..2023-01-11 | 2023-01-11..2024-01-11 | `{'lookback': 252, 'top_n': 4}` | 0.831 |
| 2019-01-11..2024-01-11 | 2024-01-11..2024-12-31 | `{'lookback': 252, 'top_n': 4}` | 0.976 |

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
