from typing import Dict, Any, List
from core.models import Severity

class PrometheusExporter:
    """
    Exposes incident statistics, MTTA/MTTR, and suppression metrics in standard Prometheus text format.
    """

    def __init__(self):
        self._incidents_total: Dict[str, int] = {
            "P0": 0, "P1": 0, "P2": 0, "P3": 0
        }
        self._suppressed_alerts = 0
        self._approved_patches = 0
        self._mttr_samples: List[float] = []

    def record_incident(self, severity: Severity) -> None:
        self._incidents_total[severity.value] += 1

    def record_suppressed(self, count: int = 1) -> None:
        self._suppressed_alerts += count

    def record_patch_approved(self) -> None:
        self._approved_patches += 1

    def record_mttr(self, mttr_seconds: float) -> None:
        self._mttr_samples.append(mttr_seconds)

    def render_prometheus_text(self) -> str:
        lines = [
            "# HELP switchguard_incidents_total Total number of triggered incidents by severity",
            "# TYPE switchguard_incidents_total counter"
        ]
        for sev, count in self._incidents_total.items():
            lines.append(f'switchguard_incidents_total{{severity="{sev}"}} {count}')

        lines.extend([
            "# HELP switchguard_suppressed_alerts_total Total number of duplicate alerts suppressed by deduplicator",
            "# TYPE switchguard_suppressed_alerts_total counter",
            f"switchguard_suppressed_alerts_total {self._suppressed_alerts}",
            "# HELP switchguard_approved_patches_total Total number of autonomous patches approved by human operators",
            "# TYPE switchguard_approved_patches_total counter",
            f"switchguard_approved_patches_total {self._approved_patches}"
        ])

        avg_mttr = (sum(self._mttr_samples) / len(self._mttr_samples)) if self._mttr_samples else 0.0
        lines.extend([
            "# HELP switchguard_mttr_average_seconds Average Mean Time to Resolution in seconds",
            "# TYPE switchguard_mttr_average_seconds gauge",
            f"switchguard_mttr_average_seconds {round(avg_mttr, 2)}"
        ])

        return "\n".join(lines) + "\n"
