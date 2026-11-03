import pytest
from core.models import Alert, Severity, IncidentStatus
from core.orchestrator import IncidentOrchestrator

def test_orchestrator_e2e_lifecycle():
    orch = IncidentOrchestrator(authorized_approvers={"Shubham"})

    # Ingest Alert
    alert = Alert(
        alert_id="ALT-E2E-1",
        source="sentry",
        service="checkout-service",
        error_type="ZeroDivisionError",
        message="float division by zero on promo order"
    )
    incident = orch.ingest_alert(alert, error_rate_pct=100.0)
    assert incident is not None
    assert incident.status == IncidentStatus.TRIGGERED
    assert incident.severity == Severity.P0_CRITICAL
    assert incident.incident_id in orch.active_incidents

    # Ingest duplicate alert (should be suppressed by deduplicator)
    dup = orch.ingest_alert(alert, error_rate_pct=100.0)
    assert dup is None

    # Request human approval for patch
    patch = "+ if net_total == 0.0: savings_ratio = 1.0"
    orch.request_remediation_approval(incident.incident_id, patch_diff=patch)
    assert incident.status == IncidentStatus.AWAITING_APPROVAL

    # Approve and Resolve
    postmortem = orch.approve_and_resolve(incident.incident_id, approver="Shubham")
    assert incident.status == IncidentStatus.RESOLVED
    assert "📑 Postmortem:" in postmortem
    assert incident.incident_id in postmortem

    # Check cryptographic audit vault
    assert orch.vault.verify_integrity() is True
    assert len(orch.vault.chain) >= 3
