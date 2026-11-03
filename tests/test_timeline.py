import pytest
from core.models import Incident, Severity, IncidentStatus, BlastRadius
from core.timeline import StatusBoardRenderer

def test_status_board_renderer_markdown():
    incident = Incident(
        incident_id="INC-900",
        title="Database Connection Pool Exhaustion",
        service="order-processing",
        severity=Severity.P0_CRITICAL,
        blast_radius=BlastRadius(
            affected_users_pct=75.0,
            financial_impact_estimate_usd=12500.0,
            degraded_dependencies=["order-processing", "database-primary"]
        )
    )
    incident.add_timeline_event("switchguard-sentinel", "TRIGGERED", "Connection timeout spike detected")
    incident.add_timeline_event("switch-buddy-admin", "INVESTIGATING", "Running pg_stat_activity query")

    board = StatusBoardRenderer.render_board(incident)
    assert "### 🛡️ SwitchGuard War Room: `INC-900`" in board
    assert "**Severity:** `P0`" in board
    assert "Affected Users: `75.0%`" in board
    assert "$12,500.00 USD" in board
    assert "switchguard-sentinel" in board
    assert "switch-buddy-admin" in board
