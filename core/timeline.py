from typing import List
from .models import Incident, IncidentStatus, Severity

class StatusBoardRenderer:
    """
    Renders structured Markdown status boards formatted for Discord and Slack.
    """

    @classmethod
    def render_board(cls, incident: Incident) -> str:
        status_icons = {
            IncidentStatus.TRIGGERED: "🔴 Triggered",
            IncidentStatus.ACKNOWLEDGED: "🟡 Acknowledged",
            IncidentStatus.INVESTIGATING: "🔍 Investigating",
            IncidentStatus.ROOT_CAUSE_IDENTIFIED: "🎯 Root Cause Identified",
            IncidentStatus.PATCHING: "🛠️ Patching in Progress",
            IncidentStatus.AWAITING_APPROVAL: "⚠️ Awaiting Human Signoff",
            IncidentStatus.RESOLVED: "🟢 Resolved",
            IncidentStatus.CLOSED: "⚪ Closed"
        }

        icon_str = status_icons.get(incident.status, incident.status.value)
        timeline_rows = []
        for entry in incident.timeline[-5:]:  # Show recent 5 events
            t_str = entry.timestamp.strftime("%H:%M:%S UTC")
            timeline_rows.append(f"- `[{t_str}]` **{entry.actor}**: {entry.action} — _{entry.details}_")

        timeline_section = "\n".join(timeline_rows) if timeline_rows else "- _No activity recorded yet._"

        diff_preview = ""
        if incident.patch_diff:
            diff_preview = f"\n\n**Proposed Patch Diff:**\n```diff\n{incident.patch_diff}\n```"

        board = f"""### 🛡️ SwitchGuard War Room: `{incident.incident_id}`
> **Service:** `{incident.service}` | **Severity:** `{incident.severity.value}` | **Status:** {icon_str}

**Blast Radius & Telemetry:**
- Affected Users: `{incident.blast_radius.affected_users_pct}%`
- Financial Impact Risk: `${incident.blast_radius.financial_impact_estimate_usd:,.2f} USD`
- Degraded Dependencies: {', '.join(f'`{d}`' for d in incident.blast_radius.degraded_dependencies) or 'None'}

**Incident Timeline:**
{timeline_section}{diff_preview}
"""
        return board.strip()
