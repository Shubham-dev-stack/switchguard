import pytest
from core.models import Severity
from metrics.exporter import PrometheusExporter

def test_prometheus_exporter_rendering():
    exporter = PrometheusExporter()
    exporter.record_incident(Severity.P0_CRITICAL)
    exporter.record_incident(Severity.P0_CRITICAL)
    exporter.record_incident(Severity.P1_MAJOR)
    exporter.record_suppressed(14)
    exporter.record_patch_approved()
    exporter.record_mttr(171.0)  # 2m 51s

    output = exporter.render_prometheus_text()
    assert 'switchguard_incidents_total{severity="P0"} 2' in output
    assert 'switchguard_incidents_total{severity="P1"} 1' in output
    assert 'switchguard_suppressed_alerts_total 14' in output
    assert 'switchguard_approved_patches_total 1' in output
    assert 'switchguard_mttr_average_seconds 171.0' in output
