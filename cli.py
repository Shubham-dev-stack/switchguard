#!/usr/bin/env python3
"""
SwitchGuard CLI: Command-line companion for Autonomous SRE Incident Response.
"""
import argparse
import sys
from core.models import Alert, Severity, Incident, IncidentStatus
from core.classifier import SeverityClassifier
from core.sla import SLATracker
from core.timeline import StatusBoardRenderer
from postmortem.generator import PostmortemGenerator
from diagnostics.healthcheck import ServiceHealthProbe
from diagnostics.log_analyzer import LogAnalyzer
from metrics.exporter import PrometheusExporter
from governance.vault import AuditVault
from scripts.simulate_p0_outage import run_simulation

def handle_triage(args):
    alert = Alert(
        alert_id="CLI-ALERT-1",
        source="cli-manual",
        service=args.service,
        error_type=args.error,
        message=args.message or f"Incident reported on {args.service}"
    )
    severity = SeverityClassifier.classify(alert, error_rate_pct=args.error_rate)
    blast = SeverityClassifier.estimate_blast_radius(alert, error_rate_pct=args.error_rate)
    
    print(f"=== SwitchGuard Triage Result ===")
    print(f"Service:      {alert.service}")
    print(f"Assigned:     {severity.value}")
    print(f"User Impact:  {blast.affected_users_pct}%")
    print(f"Financial:    ${blast.financial_impact_estimate_usd:,.2f} USD")
    return 0

def handle_probe(args):
    probe = ServiceHealthProbe(args.service)
    res = probe.probe(lambda: True)
    print(f"=== Service Health: {args.service} ===")
    print(f"Status:   {res['status']}")
    print(f"Latency:  {res['latency_ms']} ms")
    return 0

def handle_postmortem(args):
    inc = Incident(
        incident_id=args.incident_id,
        title=f"Autonomous Incident Remediation for {args.service}",
        service=args.service,
        severity=Severity.P0_CRITICAL
    )
    inc.add_timeline_event("switchguard-sentinel", "TRIGGERED", "Anomalous failure detected")
    inc.add_timeline_event("switch-buddy-admin", "PATCHED", "Autonomous fix deployed and verified")
    inc.transition_to(IncidentStatus.RESOLVED, actor="switch-buddy-admin", reason="All tests passed")

    md = PostmortemGenerator.generate_report(inc)
    print(md)
    return 0

def handle_simulate(args):
    return run_simulation()

def handle_metrics(args):
    exporter = PrometheusExporter()
    exporter.record_incident(Severity.P0_CRITICAL)
    exporter.record_suppressed(5)
    exporter.record_patch_approved()
    exporter.record_mttr(171.0)
    print(exporter.render_prometheus_text())
    return 0

def handle_audit_verify(args):
    vault = AuditVault()
    vault.record_event("INC-CLI-1", "operator", "CHECK", "Integrity check invoked")
    valid = vault.verify_integrity()
    print(f"=== SwitchGuard Audit Vault ===")
    print(f"Total Blocks:     {len(vault.chain)}")
    print(f"Integrity Status: {'VALID (SHA-256 intact)' if valid else 'CORRUPTED'}")
    return 0 if valid else 1

def main():
    parser = argparse.ArgumentParser(description="SwitchGuard Autonomous SRE CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # triage
    p_triage = subparsers.add_parser("triage", help="Triage an alert and compute severity & blast radius")
    p_triage.add_argument("--service", required=True, help="Microservice name")
    p_triage.add_argument("--error", required=True, help="Error exception type")
    p_triage.add_argument("--message", default="", help="Error description message")
    p_triage.add_argument("--error-rate", type=float, default=100.0, help="Error rate percentage (0-100)")
    p_triage.set_defaults(func=handle_triage)

    # probe
    p_probe = subparsers.add_parser("probe", help="Perform synthetic health check probe on a microservice")
    p_probe.add_argument("--service", required=True, help="Microservice name")
    p_probe.set_defaults(func=handle_probe)

    # postmortem
    p_post = subparsers.add_parser("postmortem", help="Generate blameless postmortem report")
    p_post.add_argument("--incident-id", required=True, help="Incident tracking ID")
    p_post.add_argument("--service", default="checkout-service", help="Microservice name")
    p_post.set_defaults(func=handle_postmortem)

    # simulate
    p_sim = subparsers.add_parser("simulate", help="Run end-to-end incident war room simulation")
    p_sim.set_defaults(func=handle_simulate)

    # metrics
    p_met = subparsers.add_parser("metrics", help="Export Prometheus SRE metrics")
    p_met.set_defaults(func=handle_metrics)

    # audit-verify
    p_aud = subparsers.add_parser("audit-verify", help="Verify cryptographic integrity of audit vault")
    p_aud.set_defaults(func=handle_audit_verify)

    args = parser.parse_args()
    return args.func(args)

if __name__ == "__main__":
    sys.exit(main())
