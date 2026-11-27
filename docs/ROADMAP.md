# Roadmap

- [x] **1a. Foundation**: engine, US/India costs, baselines, sleeves, allocation rules, walk-forward, trial log, leak tests.
- [ ] **1a. First real-data results**: run `us_sleeves_v1` and `india_sleeves_v1` on free data (GitHub Actions).
- [ ] **1b. More baselines**: trend-filtered stable sleeve, RSI reversion and breakout active sleeves, regime breakdown by year.
- [ ] **1b. After-tax line**: STCG/LTCG for India, short/long term for US.
- [ ] **1c. ML active sleeve**: feature pipeline, purged/embargoed CV, LightGBM ranking, compared to momentum.
- [ ] **1d. Agentic research (optional)**: LLM agents tested only after their training cutoff or forward.
- [ ] **Gate**: `docs/PROMOTION_GATE.md`.
- [ ] **Phase 2**: paper trading with daily refit and trade journal (Alpaca paper for US; India manual or broker API).
