import pytest
from core.models import Alert, Severity
from core.classifier import SeverityClassifier

def test_tier1_fatal_error_classification():
    alert = Alert(
        alert_id="ALT-001",
        source="sentry",
        service="checkout",
        error_type="ZeroDivisionError",
        message="float division by zero in checkout promo pipeline"
    )
    severity = SeverityClassifier.classify(alert, error_rate_pct=100.0)
    assert severity == Severity.P0_CRITICAL

def test_tier2_moderate_classification():
    alert = Alert(
        alert_id="ALT-002",
        source="datadog",
        service="inventory",
        error_type="TimeoutError",
        message="Failed to update stock cache"
    )
    severity = SeverityClassifier.classify(alert, error_rate_pct=15.0)
    assert severity == Severity.P2_MODERATE

def test_tier2_low_error_rate_classification():
    alert = Alert(
        alert_id="ALT-003",
        source="sentry",
        service="inventory",
        error_type="ValueError",
        message="Invalid product SKU format"
    )
    severity = SeverityClassifier.classify(alert, error_rate_pct=5.0)
    assert severity == Severity.P2_MODERATE

def test_blast_radius_estimation():
    alert = Alert(
        alert_id="ALT-004",
        source="datadog",
        service="checkout",
        error_type="ZeroDivisionError",
        message="crash on checkout"
    )
    blast = SeverityClassifier.estimate_blast_radius(alert, error_rate_pct=50.0, active_traffic_rps=100.0)
    assert blast.affected_users_pct == 50.0
    assert len(blast.affected_endpoints) == 2
    # 100 rps * 50% = 50 lost orders/sec * 60 = 3000 lost orders/min * $50 = $150,000
    assert blast.financial_impact_estimate_usd == 150000.0
