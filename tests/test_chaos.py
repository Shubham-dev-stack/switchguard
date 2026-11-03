import pytest
from chaos.injector import ChaosInjector, SyntheticFaultError
from chaos.fuzzer import BoundaryFuzzer
import sys
import os

# Import demo checkout function
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "demo-service"))
from checkout import calculate_order_total

def test_chaos_injector_clean():
    injector = ChaosInjector(failure_rate=0.0, latency_seconds=0.0)
    res = injector.wrap(lambda x: x * 2, 21)
    assert res == 42

def test_chaos_injector_forced_fault():
    injector = ChaosInjector(failure_rate=1.0)
    with pytest.raises(SyntheticFaultError):
        injector.wrap(lambda: "ok")

def test_boundary_fuzzer_on_fixed_checkout():
    fuzz_results = BoundaryFuzzer.fuzz_checkout_discounts(calculate_order_total)
    assert len(fuzz_results) == 8
    
    # 100% discount should pass safely with savings_ratio = 1.0
    r_100 = next(r for r in fuzz_results if r["discount_pct"] == 100.0)
    assert r_100["passed"] is True
    assert r_100["result"]["savings_ratio"] == 1.0
