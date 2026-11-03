from typing import List, Dict, Any, Callable, Tuple

class BoundaryFuzzer:
    """
    Automated boundary fuzzer for order calculations and financial logic.
    Identifies uncaught zero-division, overflow, and negative value exceptions.
    """

    EXTREME_DISCOUNTS = [0.0, 50.0, 99.99, 100.0, -10.0, 150.0, 0.000001, 100.000001]

    @classmethod
    def fuzz_checkout_discounts(cls, checkout_fn: Callable[[List[Dict[str, Any]], float], Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        dummy_items = [{"id": "item-1", "price": 100.0, "quantity": 1}]

        for pct in cls.EXTREME_DISCOUNTS:
            outcome = {
                "discount_pct": pct,
                "passed": False,
                "error": None,
                "result": None
            }
            try:
                res = checkout_fn(dummy_items, pct)
                outcome["passed"] = True
                outcome["result"] = res
            except Exception as e:
                outcome["passed"] = False
                outcome["error"] = f"{type(e).__name__}: {str(e)}"
            results.append(outcome)

        return results
