import pytest
from core.models import Incident, Severity, IncidentStatus, BlastRadius
from adapters.discord_adapter import DiscordAdapter, SEVERITY_COLORS
from adapters.slack_adapter import SlackAdapter

@pytest.fixture
def sample_incident():
    return Incident(
        incident_id="INC-404",
        title="Payment Service Latency Anomaly",
        service="payment-gateway",
        severity=Severity.P0_CRITICAL,
        status=IncidentStatus.INVESTIGATING,
        blast_radius=BlastRadius(
            affected_users_pct=80.0,
            financial_impact_estimate_usd=30000.0,
            degraded_dependencies=["payment-gateway", "stripe-api"]
        )
    )

def test_discord_incident_card(sample_incident):
    adapter = DiscordAdapter()
    res = adapter.format_incident_card(sample_incident)
    assert "embeds" in res
    embed = res["embeds"][0]
    assert embed["color"] == SEVERITY_COLORS[Severity.P0_CRITICAL]
    assert "[P0] Payment Service Latency Anomaly" in embed["title"]
    assert any(f["name"] == "Incident ID" and f["value"] == "`INC-404`" for f in embed["fields"])

def test_discord_approval_request(sample_incident):
    adapter = DiscordAdapter()
    res = adapter.format_approval_request(sample_incident, "Fix zero division on line 24")
    assert "embeds" in res
    assert "components" in res
    actions = res["components"][0]["components"]
    assert len(actions) == 2
    assert actions[0]["label"] == "Approve & Deploy"
    assert actions[1]["label"] == "Reject Patch"

def test_slack_incident_card(sample_incident):
    adapter = SlackAdapter()
    res = adapter.format_incident_card(sample_incident)
    assert "blocks" in res
    header = res["blocks"][0]
    assert "Payment Service Latency Anomaly" in header["text"]["text"]

def test_slack_approval_request(sample_incident):
    adapter = SlackAdapter()
    res = adapter.format_approval_request(sample_incident, "Hotfix applied to billing pool")
    assert "blocks" in res
    action_block = next(b for b in res["blocks"] if b["type"] == "actions")
    assert len(action_block["elements"]) == 2
    assert action_block["elements"][0]["style"] == "primary"
    assert action_block["elements"][1]["style"] == "danger"
