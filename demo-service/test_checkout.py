import pytest
from checkout import calculate_order_total, OrderProcessingError

def test_standard_order():
    items = [{"id": "item-1", "price": 50.0, "quantity": 2}]
    res = calculate_order_total(items, discount_pct=20.0)
    assert res["subtotal"] == 100.0
    assert res["discount_amount"] == 20.0
    assert res["net_total"] == 80.0
    assert res["savings_ratio"] == 1.25

def test_empty_order_raises():
    with pytest.raises(OrderProcessingError):
        calculate_order_total([])

def test_promotional_free_order():
    # Production incident test case: 100% discount promotion
    items = [{"id": "item-promo", "price": 25.0, "quantity": 1}]
    res = calculate_order_total(items, discount_pct=100.0)
    assert res["net_total"] == 0.0
    assert res["status"] == "settled"
