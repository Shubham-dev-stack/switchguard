import pytest
from datetime import datetime, timezone
from core.models import Severity, IncidentStatus, Alert, BlastRadius, Incident, TimelineEntry

def test_alert_dataclass():
    alert = Alert(
        alert_id="ALT-101",
        source="sentry",
        service="checkout-service",
        error_type="ZeroDivisionError",
        message="float division by zero",
        stack_trace="checkout.py:24 in calculate_order_total",
        metadata={"environment": "production"}
    )
    assert alert.alert_id == "ALT-101"
    assert alert.service == "checkout-service"
    assert alert.error_type == "ZeroDivisionError"
    assert alert.metadata["environment"] == "production"

def test_incident_state_transitions():
    incident = Incident(
        incident_id="INC-501",
        title="ZeroDivisionError in Checkout Service",
        service="checkout-service",
        severity=Severity.P0_CRITICAL
    )
    assert incident.status == IncidentStatus.TRIGGERED
    assert incident.resolved_at is None

    # Transition to ACKNOWLEDGED
    incident.transition_to(IncidentStatus.ACKNOWLEDGED, actor="switchguard-commander", reason="P0 War Room Opened")
    assert incident.status == IncidentStatus.ACKNOWLEDGED
    assert len(incident.timeline) == 1
    assert incident.timeline[0].actor == "switchguard-commander"

    # Transition to INVESTIGATING
    incident.transition_to(IncidentStatus.INVESTIGATING, actor="switch-buddy-admin", reason="Locating source files")
    assert incident.status == IncidentStatus.INVESTIGATING
    assert len(incident.timeline) == 2

    # Transition to RESOLVED
    incident.transition_to(IncidentStatus.RESOLVED, actor="switch-buddy-admin", reason="Patch verified via pytest")
    assert incident.status == IncidentStatus.RESOLVED
    assert incident.resolved_at is not None
    assert len(incident.timeline) == 3

def test_blast_radius_dataclass():
    br = BlastRadius(
        affected_users_pct=85.0,
        affected_endpoints=["/api/v1/checkout"],
        financial_impact_estimate_usd=4250.0,
        degraded_dependencies=["checkout-service", "stripe-gateway"]
    )
    assert br.affected_users_pct == 85.0
    assert len(br.degraded_dependencies) == 2
    assert br.financial_impact_estimate_usd == 4250.0
