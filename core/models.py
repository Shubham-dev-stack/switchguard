from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

class Severity(str, Enum):
    P0_CRITICAL = "P0"  # Complete customer-facing outage or data integrity risk
    P1_MAJOR = "P1"     # Significant degradation, partial feature failure
    P2_MODERATE = "P2"  # Non-critical bug with functional workarounds
    P3_LOW = "P3"       # Minor glitch, cosmetic issue, or low-impact warning

class IncidentStatus(str, Enum):
    TRIGGERED = "triggered"
    ACKNOWLEDGED = "acknowledged"
    INVESTIGATING = "investigating"
    ROOT_CAUSE_IDENTIFIED = "root_cause_identified"
    PATCHING = "patching"
    AWAITING_APPROVAL = "awaiting_approval"
    RESOLVED = "resolved"
    CLOSED = "closed"

@dataclass
class Alert:
    alert_id: str
    source: str  # e.g., "sentry", "datadog", "pagerduty", "manual"
    service: str
    error_type: str
    message: str
    stack_trace: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass
class TimelineEntry:
    actor: str  # e.g., "switchguard-commander", "@Shubham", "switchguard-fixer"
    action: str
    details: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass
class BlastRadius:
    affected_users_pct: float = 0.0
    affected_endpoints: List[str] = field(default_factory=list)
    financial_impact_estimate_usd: float = 0.0
    degraded_dependencies: List[str] = field(default_factory=list)

@dataclass
class Incident:
    incident_id: str
    title: str
    service: str
    severity: Severity
    status: IncidentStatus = IncidentStatus.TRIGGERED
    blast_radius: BlastRadius = field(default_factory=BlastRadius)
    timeline: List[TimelineEntry] = field(default_factory=list)
    root_cause: Optional[str] = None
    patch_diff: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    resolved_at: Optional[datetime] = None

    def add_timeline_event(self, actor: str, action: str, details: str) -> None:
        self.timeline.append(TimelineEntry(actor=actor, action=action, details=details))

    def transition_to(self, new_status: IncidentStatus, actor: str, reason: str = "") -> None:
        self.status = new_status
        self.add_timeline_event(actor=actor, action=f"Status -> {new_status.value}", details=reason)
        if new_status == IncidentStatus.RESOLVED and not self.resolved_at:
            self.resolved_at = datetime.now(timezone.utc)
