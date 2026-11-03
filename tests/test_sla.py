import pytest
from datetime import datetime, timezone, timedelta
from core.models import Incident, Severity, IncidentStatus
from core.sla import SLATracker, SLA_TARGETS

def test_sla_targets_exist():
    assert Severity.P0_CRITICAL in SLA_TARGETS
    assert SLA_TARGETS[Severity.P0_CRITICAL]["ack_minutes"] == 5.0
    assert SLA_TARGETS[Severity.P0_CRITICAL]["resolve_minutes"] == 30.0

def test_sla_metric_calculation_active():
    now = datetime.now(timezone.utc)
    incident = Incident(
        incident_id="INC-801",
        title="Payment Processor Timeout",
        service="payment-gateway",
        severity=Severity.P0_CRITICAL,
        created_at=now - timedelta(minutes=10)
    )
    metrics = SLATracker.calculate_metrics(incident)
    assert metrics["severity"] == "P0"
    assert metrics["target_ack_minutes"] == 5.0
    assert metrics["target_resolve_minutes"] == 30.0
    assert metrics["elapsed_minutes"] >= 10.0
    assert metrics["is_resolved"] is False
    assert metrics["is_breached"] is False

def test_sla_metric_breached():
    now = datetime.now(timezone.utc)
    incident = Incident(
        incident_id="INC-802",
        title="Unresolved Outage Exceeded 30m MTTR",
        service="payment-gateway",
        severity=Severity.P0_CRITICAL,
        created_at=now - timedelta(minutes=45)
    )
    metrics = SLATracker.calculate_metrics(incident)
    assert metrics["is_breached"] is True
