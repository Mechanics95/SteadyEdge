# Brokers and rules (US on H-1B, India as an Indian citizen)

**Not legal, tax, or immigration advice.** Rules change; confirm with your broker, a tax
professional, and (for visa questions) an immigration attorney.

## US account (you are on an H-1B visa)

- **Investing is generally fine on H-1B.** Buying and holding stocks/ETFs is usually treated as
  passive investment. **Very frequent trading that looks like running a business** is a grey area
  that some immigration attorneys warn about. Ask one before running an active day-trading bot.
- **Pattern Day Trader rule:** in a *margin* account under $25,000, more than 3 day trades
  (buy and sell the same stock the same day) in 5 business days gets the account restricted.
  FINRA has been working on changing this rule; check its current status with your broker.
  A *cash* account avoids PDT but you must wait for sales to settle (T+1) before reusing the money.
- **With $500 there is no legal cap on how much you can trade**, but the PDT rule and settlement
  effectively limit day trading. Our active sleeve trades monthly, so PDT is not an issue.
- **Brokers:** Robinhood (fractional shares, $0 commission; no official stock-trading API, so it
  can't be automated cleanly). **Alpaca** (API-first, free paper trading, fractional shares) or
  **Interactive Brokers** (API, global markets) fit an automated Phase 2. Fidelity/Schwab are fine
  for manual investing.
- **Tax:** as a US tax resident, short-term gains are taxed as ordinary income; the wash-sale rule
  applies. Gains may also need reporting in India depending on your Indian residency status.

## India account

- **Residency matters more than citizenship.** An Indian citizen living abroad for most of the
  year is usually an **NRI** under FEMA, even on a work visa. NRIs must trade through **NRE/NRO
  bank accounts with NRI demat and trading accounts** (often PIS-linked for repatriable money),
  not a regular resident account.
- **NRIs generally cannot do intraday equity trading or short selling.** Delivery trades only.
  That is why the India cost model assumes delivery (CNC) trades.
- **NRI brokerage is usually higher than the Rs 0 resident delivery rate**, and there may be extra
  account charges. With a Rs 44,000 account, a fixed per-order fee can wipe out an active strategy.
  Put your actual broker fee in `configs/india_sleeves.yaml` under `cost_overrides`.
- **Limits:** an individual NRI can hold up to 5% of a listed company's paid-up capital; not a
  constraint at this size.
- **Tax (India, current rules, verify):** listed equity STCG 20%, LTCG 12.5% above Rs 1.25 lakh a
  year. For NRIs, tax is often deducted at source by the broker. The India–US tax treaty may give
  credits.
