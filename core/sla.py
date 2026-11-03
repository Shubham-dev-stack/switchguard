from datetime import datetime, timezone, timedelta
from typing import Dict, Optional, Tuple
from .models import Incident, Severity, IncidentStatus

# Standard Enterprise SRE SLA Thresholds (in minutes)
SLA_TARGETS: Dict[Severity, Dict[str, float]] = {
    Severity.P0_CRITICAL: {"ack_minutes": 5.0, "resolve_minutes": 30.0},
    Severity.P1_MAJOR:    {"ack_minutes": 15.0, "resolve_minutes": 120.0},
    Severity.P2_MODERATE: {"ack_minutes": 60.0, "resolve_minutes": 480.0},
    Severity.P3_LOW:      {"ack_minutes": 240.0, "resolve_minutes": 1440.0},
}

class SLATracker:
    """
    Computes real-time SLA metrics (MTTA, MTTR) and monitors SLA breach deadlines.
    """

    @classmethod
    def calculate_metrics(cls, incident: Incident) -> Dict[str, Any]:
        targets = SLA_TARGETS.get(incident.severity, SLA_TARGETS[Severity.P2_MODERATE])
        ack_deadline = incident.created_at + timedelta(minutes=targets["ack_minutes"])
        resolve_deadline = incident.created_at + timedelta(minutes=targets["resolve_minutes"])

        now = datetime.now(timezone.utc)
        resolved_time = incident.resolved_at or now

        total_elapsed_seconds = (resolved_time - incident.created_at).total_seconds()
        is_resolved = incident.status in (IncidentStatus.RESOLVED, IncidentStatus.CLOSED)

        breached = False
        if not is_resolved and now > resolve_deadline:
            breached = True
        elif is_resolved and incident.resolved_at and incident.resolved_at > resolve_deadline:
            breached = True

        return {
            "severity": incident.severity.value,
            "target_ack_minutes": targets["ack_minutes"],
            "target_resolve_minutes": targets["resolve_minutes"],
            "elapsed_minutes": round(total_elapsed_seconds / 60.0, 2),
            "ack_deadline_utc": ack_deadline.isoformat(),
            "resolve_deadline_utc": resolve_deadline.isoformat(),
            "is_breached": breached,
            "is_resolved": is_resolved
        }
