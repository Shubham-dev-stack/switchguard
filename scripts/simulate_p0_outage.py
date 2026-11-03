#!/usr/bin/env python3
"""
SwitchGuard Incident Simulator:
Runs an end-to-end dry run of a P0 production outage and autonomous remediation.
"""
import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Add root directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.models import Alert
from core.orchestrator import IncidentOrchestrator
from core.timeline import StatusBoardRenderer

def run_simulation():
    print("==================================================================")
    print("🛡️ SwitchGuard Autonomous Incident Simulation: P0 Checkout Outage")
    print("==================================================================\n")

    orchestrator = IncidentOrchestrator(authorized_approvers={"Shubham"})

    # 1. Ingest simulated Sentry alert
    alert = Alert(
        alert_id="SENTRY-SIM-502",
        source="sentry",
        service="checkout-service",
        error_type="ZeroDivisionError",
        message="float division by zero in calculate_order_total"
    )
    print(">> [1/4] Ingesting Telemetry Alert from Sentry...")
    incident = orchestrator.ingest_alert(alert, error_rate_pct=100.0)
    assert incident is not None
    print(f"   Severity Assigned: {incident.severity.value}")
    print(f"   Est. Financial Risk: ${incident.blast_radius.financial_impact_estimate_usd:,.2f} USD\n")

    # 2. Render Status Board
    print(">> [2/4] Rendering Chat War Room Status Card:")
    card = StatusBoardRenderer.render_board(incident)
    print(card)
    print()

    # 3. Propose autonomous patch
    patch_diff = """--- checkout.py
+++ checkout.py
@@ -24,1 +24,4 @@
-    savings_ratio = round(subtotal / net_total, 2)
+    if net_total == 0.0:
+        savings_ratio = 1.0
+    else:
+        savings_ratio = round(subtotal / net_total, 2)"""
    print(">> [3/4] Agent Synthesized Patch & Requesting Human Signoff...")
    orchestrator.request_remediation_approval(incident.incident_id, patch_diff=patch_diff)

    # 4. Human Approval
    print(">> [4/4] Operator @Shubham granted signoff. Deploying and generating postmortem...")
    postmortem = orchestrator.approve_and_resolve(incident.incident_id, approver="Shubham")
    print("\n✅ Service Restored! Blameless Postmortem Generated:")
    print("------------------------------------------------------------------")
    print(postmortem[:300] + "...\n[Report truncated for CLI output]")
    return 0

if __name__ == "__main__":
    sys.exit(run_simulation())
