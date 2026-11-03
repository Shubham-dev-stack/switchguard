"""
SwitchGuard Demo Service: Payment & Checkout Processing Engine
"""

from typing import List, Dict, Any, Optional

class OrderProcessingError(Exception):
    pass

def calculate_order_total(items: List[Dict[str, Any]], discount_pct: float = 0.0) -> Dict[str, Any]:
    """
    Calculates total order amount, applies promotional discount,
    and computes effective settlement metrics.
    """
    if not items:
        raise OrderProcessingError("Order must contain at least one item.")

    subtotal = sum(item["price"] * item["quantity"] for item in items)
    discount_amount = round(subtotal * (discount_pct / 100.0), 2)
    net_total = round(subtotal - discount_amount, 2)

    # BUG (INC-502): During 100% discount promo campaigns (discount_pct=100.0),
    # net_total becomes 0.0, resulting in an unhandled ZeroDivisionError in production!
    if net_total == 0:
        savings_ratio = 1.0
    else:
        savings_ratio = round(subtotal / net_total, 2)

    return {
        "subtotal": subtotal,
        "discount_amount": discount_amount,
        "net_total": net_total,
        "savings_ratio": savings_ratio,
        "currency": "USD",
        "status": "settled"
    }
