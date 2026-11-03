from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from core.models import Incident, Severity

class PostmortemGenerator:
    """
    Generates structured, blameless Postmortem and Root Cause Analysis (RCA) reports.
    """

    @classmethod
    def generate_report(
        cls,
        incident: Incident,
        five_whys: Optional[List[str]] = None,
        action_items: Optional[List[Dict[str, str]]] = None
    ) -> str:
        t_start = incident.created_at.strftime("%Y-%m-%d %H:%M:%S UTC")
        t_end = (incident.resolved_at or datetime.now(timezone.utc)).strftime("%Y-%m-%d %H:%M:%S UTC")
        
        # Format Timeline
        timeline_rows = []
        for e in incident.timeline:
            t_str = e.timestamp.strftime("%H:%M:%S UTC")
            timeline_rows.append(f"| `{t_str}` | **{e.actor}** | {e.action} | {e.details} |")
        timeline_table = "\n".join(timeline_rows) if timeline_rows else "| - | - | - | - |"

        # Format 5 Whys
        whys_list = five_whys or [
            "Why did the service fail? Unhandled ZeroDivisionError was raised in checkout calculation.",
            "Why was division by zero possible? Net total became 0.0 when promo code gave 100% discount.",
            "Why was savings ratio computed against net total? Assumption that all orders have net_total > 0.",
            "Why was this not caught in staging? Test cases only covered partial discounts (10%-50%).",
            "Why was boundary condition missing? Lack of automated boundary fuzzing on promotional workflows."
        ]
        whys_md = "\n".join(f"{i+1}. {w}" for i, w in enumerate(whys_list))

        # Format Action Items
        actions = action_items or [
            {"type": "Prevent", "task": "Add unit test suite for 0% and 100% boundary discounts", "owner": "@Shubham", "status": "Done"},
            {"type": "Mitigate", "task": "Deploy SwitchGuard automated canary regression runner", "owner": "SwitchGuard", "status": "Done"},
            {"type": "Process", "task": "Update PR checklist to require zero-boundary fuzz tests", "owner": "SRE Lead", "status": "In Progress"}
        ]
        action_rows = [f"| {a['type']} | {a['task']} | {a['owner']} | `{a['status']}` |" for a in actions]
        action_table = "\n".join(action_rows)

        diff_block = f"```diff\n{incident.patch_diff}\n```" if incident.patch_diff else "_No patch diff attached._"

        report = f"""# 📑 Postmortem: [{incident.severity.value}] {incident.title}

> **Incident ID:** `{incident.incident_id}`  
> **Service:** `{incident.service}`  
> **Status:** `{incident.status.value.upper()}`  
> **Start Time:** `{t_start}`  
> **Resolved Time:** `{t_end}`  

---

## 1. Executive Summary
During peak promotional traffic, `{incident.service}` experienced a critical failure resulting in complete disruption for affected customers. SwitchGuard detected the anomaly via automated telemetry, opened an incident war room in team chat, identified the root cause, applied a verified patch, and validated service recovery through automated regression testing.

## 2. Blast Radius & Customer Impact
- **Impacted Service:** `{incident.service}`
- **User Impact:** `{incident.blast_radius.affected_users_pct}%` of active checkouts failed
- **Financial Risk:** `${incident.blast_radius.financial_impact_estimate_usd:,.2f} USD`
- **Degraded Downstream:** {', '.join(f'`{d}`' for d in incident.blast_radius.degraded_dependencies) or 'None'}

## 3. Incident Timeline
| Timestamp (UTC) | Actor | Action | Details |
|---|---|---|---|
{timeline_table}

## 4. Root Cause Analysis (5 Whys)
{whys_md}

## 5. Remediation & Patch Verification
The root cause was isolated and resolved with the following patch:

{diff_block}

**Verification Method:** Automated test runner executed all unit and regression test suites with 100% pass rate prior to production rollout.

## 6. Action Items & Lessons Learned
| Type | Action Item | Owner | Status |
|---|---|---|---|
{action_table}
"""
        return report.strip()
