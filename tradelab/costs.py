"""Transaction cost models for US and Indian equities.

Every rate here is a configurable assumption, not a quote. Brokers and
regulators change fees; check them against your broker's current contract
note before trusting a backtest. Values below were set on 2026-11-27 from
publicly documented schedules and are logged in docs/DECISIONS.md.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CostBreakdown:
    total: float = 0.0
    parts: dict = field(default_factory=dict)

    def add(self, name: str, amount: float) -> None:
        self.parts[name] = self.parts.get(name, 0.0) + amount
        self.total += amount


@dataclass
class USCosts:
    """Zero-commission US broker (for example Robinhood) plus market frictions."""

    commission_per_order: float = 0.0
    slippage_bps: float = 5.0          # half-spread + impact, per side, liquid large caps / ETFs
    sec_fee_rate: float = 27.80e-6     # on sell notional; SEC resets this rate periodically
    finra_taf_per_share: float = 0.000166
    finra_taf_max: float = 8.30

    def cost(self, side: str, notional: float, shares: float) -> CostBreakdown:
        c = CostBreakdown()
        if notional <= 0:
            return c
        c.add("commission", self.commission_per_order)
        c.add("slippage", notional * self.slippage_bps / 1e4)
        if side == "sell":
            c.add("sec_fee", notional * self.sec_fee_rate)
            c.add("finra_taf", min(abs(shares) * self.finra_taf_per_share, self.finra_taf_max))
        return c


@dataclass
class IndiaDeliveryCosts:
    """NSE equity delivery (CNC) trade charges, in INR.

    Delivery, not intraday: intraday has different STT and is generally not
    available to NRIs trading under PIS (see docs/BROKERS_AND_RULES.md).
    """

    brokerage_per_order: float = 0.0     # many discount brokers charge 0 for delivery
    stt_rate: float = 0.001              # 0.1% on buy and on sell
    exchange_txn_rate: float = 0.0000297 # NSE transaction charge
    sebi_rate: float = 0.000001          # Rs 10 per crore
    stamp_duty_buy_rate: float = 0.00015 # 0.015% on buy side only
    gst_rate: float = 0.18               # on brokerage + exchange + SEBI charges
    dp_charge_per_sell: float = 15.93    # per scrip per sell day, incl. GST (broker dependent)
    slippage_bps: float = 10.0

    def cost(self, side: str, notional: float, shares: float) -> CostBreakdown:
        c = CostBreakdown()
        if notional <= 0:
            return c
        brokerage = self.brokerage_per_order
        exch = notional * self.exchange_txn_rate
        sebi = notional * self.sebi_rate
        c.add("brokerage", brokerage)
        c.add("stt", notional * self.stt_rate)
        c.add("exchange_txn", exch)
        c.add("sebi", sebi)
        c.add("gst", (brokerage + exch + sebi) * self.gst_rate)
        if side == "buy":
            c.add("stamp_duty", notional * self.stamp_duty_buy_rate)
        else:
            c.add("dp_charge", self.dp_charge_per_sell)
        c.add("slippage", notional * self.slippage_bps / 1e4)
        return c


@dataclass
class ZeroCosts:
    def cost(self, side: str, notional: float, shares: float) -> CostBreakdown:
        return CostBreakdown()


def make_cost_model(market: str, overrides: dict | None = None):
    overrides = overrides or {}
    if market == "us":
        return USCosts(**overrides)
    if market == "india":
        return IndiaDeliveryCosts(**overrides)
    if market == "none":
        return ZeroCosts()
    raise ValueError(f"unknown market {market!r}")
