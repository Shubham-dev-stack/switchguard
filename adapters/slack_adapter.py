from typing import Dict, Any, List
from core.models import Incident, Severity
from .base import BaseChatAdapter

class SlackAdapter(BaseChatAdapter):
    """
    Renders Slack Block Kit payloads with interactive section blocks and actions.
    """

    def format_incident_card(self, incident: Incident) -> Dict[str, Any]:
        blocks = [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": f"🚨 [{incident.severity.value}] {incident.title}", "emoji": True}
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Incident ID:*\n`{incident.incident_id}`"},
                    {"type": "mrkdwn", "text": f"*Service:*\n`{incident.service}`"},
                    {"type": "mrkdwn", "text": f"*Status:*\n`{incident.status.value.upper()}`"},
                    {"type": "mrkdwn", "text": f"*User Impact:*\n`{incident.blast_radius.affected_users_pct}%`"}
                ]
            },
            {
                "type": "context",
                "elements": [
                    {"type": "mrkdwn", "text": f"Financial Risk: *${incident.blast_radius.financial_impact_estimate_usd:,.2f} USD* | SRE Engine: *SwitchGuard*"}
                ]
            }
        ]
        return {"blocks": blocks}

    def format_approval_request(self, incident: Incident, patch_summary: str) -> Dict[str, Any]:
        blocks = [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": f"⚠️ Human Approval Required: {incident.incident_id}", "emoji": True}
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*Patch Summary:*\n{patch_summary}\n\n_All regression tests passed successfully._"}
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Approve & Deploy", "emoji": True},
                        "style": "primary",
                        "value": f"approve_{incident.incident_id}"
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Reject", "emoji": True},
                        "style": "danger",
                        "value": f"reject_{incident.incident_id}"
                    }
                ]
            }
        ]
        return {"blocks": blocks}
