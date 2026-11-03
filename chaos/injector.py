import time
import random
from typing import Callable, Any, Optional

class SyntheticFaultError(Exception):
    pass

class ChaosInjector:
    """
    Injects synthetic faults, network latency, and random circuit breaks into call paths.
    """

    def __init__(self, failure_rate: float = 0.0, latency_seconds: float = 0.0):
        self.failure_rate = failure_rate
        self.latency_seconds = latency_seconds

    def wrap(self, fn: Callable[..., Any], *args, **kwargs) -> Any:
        # Inject Latency
        if self.latency_seconds > 0:
            time.sleep(self.latency_seconds)

        # Inject Failure
        if self.failure_rate > 0 and random.random() < self.failure_rate:
            raise SyntheticFaultError("ChaosInjector: injected synthetic service fault")

        return fn(*args, **kwargs)
