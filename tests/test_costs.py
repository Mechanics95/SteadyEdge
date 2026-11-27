import pytest
from tradelab.costs import IndiaDeliveryCosts, USCosts


def test_india_delivery_buy_10k():
    c = IndiaDeliveryCosts().cost("buy", 10_000, 10)
    assert c.parts["stt"] == pytest.approx(10.0)
    assert c.parts["stamp_duty"] == pytest.approx(1.5)
    assert c.parts["exchange_txn"] == pytest.approx(0.297)
    assert c.parts["gst"] == pytest.approx(0.18 * (0.297 + 0.01))
    assert "dp_charge" not in c.parts
    assert c.total == pytest.approx(10 + 1.5 + 0.297 + 0.01 + 0.18 * 0.307 + 10)


def test_india_sell_has_dp_charge_no_stamp():
    c = IndiaDeliveryCosts().cost("sell", 10_000, 10)
    assert c.parts["dp_charge"] == pytest.approx(15.93)
    assert "stamp_duty" not in c.parts


def test_india_round_trip_is_expensive_for_small_accounts():
    # A Rs 5,000 round trip costs more than 0.6% - matters for a small account.
    m = IndiaDeliveryCosts()
    rt = m.cost("buy", 5000, 1).total + m.cost("sell", 5000, 1).total
    assert rt / 5000 > 0.006


def test_us_sell_fees_only_on_sell():
    m = USCosts()
    assert "sec_fee" not in m.cost("buy", 1000, 2).parts
    s = m.cost("sell", 1000, 2)
    assert s.parts["sec_fee"] == pytest.approx(1000 * 27.80e-6)
    assert s.parts["finra_taf"] == pytest.approx(2 * 0.000166)


def test_zero_notional_costs_nothing():
    assert IndiaDeliveryCosts().cost("sell", 0, 0).total == 0
