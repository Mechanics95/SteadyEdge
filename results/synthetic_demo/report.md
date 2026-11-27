# Experiment report: synthetic_demo

> Research output, not financial advice. Backtests are simulations on past data and do not guarantee future results. **This run uses SYNTHETIC random data: it tests the code, and says nothing about real markets.**

- Run: `20261127T050835Z-7df479` · commit `uncommitted` · data `d071ac2e991f`
- Out-of-sample window: 2013-01-11 to 2020-05-29 (walk-forward; holdout sealed from 2020-06-01)
- Capital $500, kill switch at $250 loss, fractional shares, costs: us model
- Trials counted for this family so far: 12

## Results (out-of-sample only)

| variant | cagr | vol | sharpe | max_drawdown | worst_12m | annual_turnover | cost_drag_pct_of_capital_per_year | excess_cagr | dsr | final_equity | killed_on |
|---|---|---|---|---|---|---|---|---|---|---|---|
| benchmark_buy_hold | 0.0376 | 0.2606 | 0.272 | -0.4236 | -0.3799 | 0.0 | 0.0 | 0.0 | 0.554 | 662.9 | None |
| stable_only | 0.0376 | 0.2606 | 0.272 | -0.4236 | -0.3799 | 0.0 | 0.0 | 0.0 | 0.554 | 662.9 | None |
| active_only | -0.054 | 0.2167 | -0.148 | -0.5095 | -0.3084 | 6.99 | 0.0031 | -0.0916 | 0.153 | 327.1 | None |
| blend_fixed_90 | 0.0302 | 0.2447 | 0.244 | -0.4029 | -0.3643 | 0.9 | 0.0005 | -0.0074 | 0.524 | 627.85 | None |
| blend_fixed_70 | 0.0146 | 0.2186 | 0.176 | -0.3914 | -0.3361 | 2.38 | 0.0013 | -0.023 | 0.448 | 558.6 | None |
| blend_fixed_50 | -0.0029 | 0.2024 | 0.087 | -0.389 | -0.3137 | 3.79 | 0.0019 | -0.0405 | 0.354 | 489.1 | None |
| blend_vol_target | 0.0061 | 0.209 | 0.134 | -0.3892 | -0.3246 | 3.09 | 0.0016 | -0.0315 | 0.403 | 523.75 | None |
| blend_drawdown_throttle | 0.0316 | 0.234 | 0.25 | -0.3949 | -0.3565 | 1.66 | 0.0009 | -0.006 | 0.53 | 634.2 | None |

## Walk-forward choices for the active sleeve

| train | test | chosen params | train Sharpe |
|---|---|---|---|
| 2009-01-11..2013-01-11 | 2013-01-11..2014-01-11 | `{'lookback': 252, 'top_n': 1}` | 0.691 |
| 2010-01-11..2014-01-11 | 2014-01-11..2015-01-11 | `{'lookback': 252, 'top_n': 1}` | 0.335 |
| 2011-01-11..2015-01-11 | 2015-01-11..2016-01-11 | `{'lookback': 252, 'top_n': 1}` | 0.405 |
| 2012-01-11..2016-01-11 | 2016-01-11..2017-01-11 | `{'lookback': 252, 'top_n': 2}` | 0.484 |
| 2013-01-11..2017-01-11 | 2017-01-11..2018-01-11 | `{'lookback': 252, 'top_n': 1}` | 0.284 |
| 2014-01-11..2018-01-11 | 2018-01-11..2019-01-11 | `{'lookback': 252, 'top_n': 1}` | 0.143 |
| 2015-01-11..2019-01-11 | 2019-01-11..2020-01-11 | `{'lookback': 126, 'top_n': 2}` | 0.093 |
| 2016-01-11..2020-01-11 | 2020-01-11..2020-05-29 | `{'lookback': 126, 'top_n': 2}` | 0.099 |

## How to read this

- `dsr` (Deflated Sharpe Ratio) is the probability the Sharpe is real after accounting for how many variants were tried. Promotion gate needs > 0.95.
- `cost_drag_pct_of_capital_per_year` is fees and slippage as a share of starting capital.
- `excess_cagr` is versus simply holding the benchmark.
