import time
from typing import Dict, Any, Callable, Optional

class ServiceHealthProbe:
    """
    Synthetically probes microservice dependencies and evaluates circuit breaker threshold.
    """

    def __init__(self, service_name: str, timeout_seconds: float = 2.0):
        self.service_name = service_name
        self.timeout_seconds = timeout_seconds

    def probe(self, health_fn: Callable[[], bool]) -> Dict[str, Any]:
        start = time.perf_counter()
        healthy = False
        error_msg = None

        try:
            healthy = bool(health_fn())
        except Exception as e:
            healthy = False
            error_msg = str(e)
        finally:
            elapsed_ms = (time.perf_counter() - start) * 1000.0

        status = "HEALTHY" if healthy else "UNHEALTHY"
        if healthy and elapsed_ms > (self.timeout_seconds * 1000.0 * 0.75):
            status = "DEGRADED"

        return {
            "service": self.service_name,
            "status": status,
            "latency_ms": round(elapsed_ms, 2),
            "healthy": healthy,
            "error": error_msg
        }
