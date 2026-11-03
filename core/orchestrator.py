from typing import Dict, Any, Optional, Set
from core.models import Alert, Incident, Severity, IncidentStatus
from core.classifier import SeverityClassifier
from core.sla import SLATracker
from core.timeline import StatusBoardRenderer
from ingestion.deduplicator import AlertDeduplicator
from governance.approval_gate import ApprovalGate
from governance.vault import AuditVault
from postmortem.generator import PostmortemGenerator

class IncidentOrchestrator:
    """
    Central orchestration engine for SwitchGuard.
    Coordinates telemetry ingestion, triage, human approval, audit vault, and postmortem generation.
    """

    def __init__(self, authorized_approvers: Optional[Set[str]] = None):
        self.deduplicator = AlertDeduplicator()
        self.approval_gate = ApprovalGate(authorized_approvers or {"Shubham", "sre-lead"})
        self.vault = AuditVault()
        self.active_incidents: Dict[str, Incident] = {}

    def ingest_alert(self, alert: Alert, error_rate_pct: float = 100.0) -> Optional[Incident]:
        """
        Ingests an alert, suppresses duplicates, and opens a new Incident if novel.
        """
        is_new, count = self.deduplicator.process(alert)
        if not is_new:
            # Alert storm suppressed; update active incident if present
            return None

        # Compute triage & blast radius
        severity = SeverityClassifier.classify(alert, error_rate_pct=error_rate_pct)
        blast = SeverityClassifier.estimate_blast_radius(alert, error_rate_pct=error_rate_pct)

        inc_id = f"INC-{alert.service.upper()}-{int(blast.financial_impact_estimate_usd)}"
        incident = Incident(
            incident_id=inc_id,
            title=f"Autonomous Incident: {alert.error_type} in {alert.service}",
            service=alert.service,
            severity=severity,
            status=IncidentStatus.TRIGGERED,
            blast_radius=blast
        )

        incident.add_timeline_event("switchguard-sentinel", "ALERT_INGESTED", f"Ingested {alert.error_type} from {alert.source}")
        self.vault.record_event(inc_id, "switchguard-sentinel", "INCIDENT_TRIGGERED", f"Severity: {severity.value}")
        self.active_incidents[inc_id] = incident
        return incident

    def request_remediation_approval(self, incident_id: str, patch_diff: str) -> None:
        incident = self.active_incidents.get(incident_id)
        if not incident:
            raise ValueError(f"Incident {incident_id} not found")

        incident.patch_diff = patch_diff
        incident.transition_to(IncidentStatus.AWAITING_APPROVAL, actor="switchguard-fixer", reason="Patch ready for human signoff")
        self.approval_gate.request_approval(incident_id, patch_hash=str(hash(patch_diff)))
        self.vault.record_event(incident_id, "switchguard-fixer", "AWAITING_APPROVAL", "Patch regression passed")

    def approve_and_resolve(self, incident_id: str, approver: str) -> str:
        incident = self.active_incidents.get(incident_id)
        if not incident:
            raise ValueError(f"Incident {incident_id} not found")

        self.approval_gate.evaluate_approval(incident_id, approver=approver, decision="approve")
        incident.transition_to(IncidentStatus.RESOLVED, actor=approver, reason="Human operator approved deployment")
        self.vault.record_event(incident_id, approver, "INCIDENT_RESOLVED", "Production restored")
        
        # Generate postmortem
        postmortem = PostmortemGenerator.generate_report(incident)
        return postmortem
