from typing import Dict, Any
from core.models import Incident, Severity, IncidentStatus
from .base import BaseChatAdapter

# Discord Embed Color mapping
SEVERITY_COLORS = {
    Severity.P0_CRITICAL: 0xED4245,  # Discord Red
    Severity.P1_MAJOR:    0xE67E22,  # Discord Orange
    Severity.P2_MODERATE: 0xFEE75C,  # Discord Yellow
    Severity.P3_LOW:      0x57F287   # Discord Green
}

class DiscordAdapter(BaseChatAdapter):
    """
    Renders rich Discord Embeds and Action Rows for SwitchGuard War Rooms.
    """

    def format_incident_card(self, incident: Incident) -> Dict[str, Any]:
        color = SEVERITY_COLORS.get(incident.severity, 0x5865F2)
        embed = {
            "title": f"🚨 [{incident.severity.value}] {incident.title}",
            "description": f"Autonomous Incident War Room opened for `{incident.service}`.",
            "color": color,
            "fields": [
                {"name": "Incident ID", "value": f"`{incident.incident_id}`", "inline": True},
                {"name": "Status", "value": f"`{incident.status.value.upper()}`", "inline": True},
                {"name": "User Impact", "value": f"{incident.blast_radius.affected_users_pct}%", "inline": True},
                {"name": "Est. Financial Risk", "value": f"${incident.blast_radius.financial_impact_estimate_usd:,.2f} USD", "inline": True},
                {"name": "Dependencies", "value": ", ".join(incident.blast_radius.degraded_dependencies) or "None", "inline": True}
            ],
            "footer": {"text": "SwitchGuard Autonomous SRE • Powered by Switch"}
        }
        return {"embeds": [embed]}

    def format_approval_request(self, incident: Incident, patch_summary: str) -> Dict[str, Any]:
        embed = {
            "title": f"⚠️ Human Approval Required: {incident.incident_id}",
            "description": f"An autonomous remediation patch has passed all regression tests.\n\n**Summary:**\n{patch_summary}",
            "color": 0xFEE75C,
            "footer": {"text": "Respond 'Approve' or click the button below to proceed."}
        }
        components = [
            {
                "type": 1,  # Action Row
                "components": [
                    {"type": 2, "style": 3, "label": "Approve & Deploy", "custom_id": f"approve_{incident.incident_id}"},
                    {"type": 2, "style": 4, "label": "Reject Patch", "custom_id": f"reject_{incident.incident_id}"}
                ]
            }
        ]
        return {"embeds": [embed], "components": components}
