import pytest
from core.models import Incident, Severity, IncidentStatus, BlastRadius
from postmortem.generator import PostmortemGenerator

def test_postmortem_report_generation():
    incident = Incident(
        incident_id="INC-502",
        title="ZeroDivisionError on 100% Promo Checkout",
        service="checkout-service",
        severity=Severity.P0_CRITICAL,
        blast_radius=BlastRadius(
            affected_users_pct=100.0,
            financial_impact_estimate_usd=45000.0,
            degraded_dependencies=["checkout-service", "payment-gateway"]
        ),
        patch_diff="""--- checkout.py
+++ checkout.py
@@ -24,1 +24,4 @@
-    savings_ratio = round(subtotal / net_total, 2)
+    if net_total == 0.0:
+        savings_ratio = 1.0
+    else:
+        savings_ratio = round(subtotal / net_total, 2)"""
    )
    incident.add_timeline_event("switchguard-sentinel", "ALERT_TRIGGERED", "Received 500 error spike from Sentry")
    incident.add_timeline_event("switch-buddy-admin", "PATCH_APPLIED", "Added zero division guard in checkout.py")
    incident.transition_to(IncidentStatus.RESOLVED, actor="switch-buddy-admin", reason="All 3 pytest suites green")

    report = PostmortemGenerator.generate_report(incident)
    assert "# 📑 Postmortem: [P0] ZeroDivisionError on 100% Promo Checkout" in report
    assert "INC-502" in report
    assert "checkout-service" in report
    assert "Root Cause Analysis (5 Whys)" in report
    assert "savings_ratio = 1.0" in report
    assert "Action Items & Lessons Learned" in report
