# 📖 SwitchGuard SRE Incident Runbook

This runbook outlines operational procedures for Site Reliability Engineers responding to production incidents using SwitchGuard.

---

## 1. Triggering an Incident War Room

### Method A: Automated Ingestion
When your monitoring provider (Sentry, Datadog, Prometheus) detects an anomaly, configure its webhook target to point to SwitchGuard. SwitchGuard will automatically:
1. Deduplicate the alert to suppress notification storms.
2. Calculate Severity (P0-P3) and Blast Radius.
3. Open a dedicated War Room thread in `#incident-war-room`.

### Method B: Manual Chat Invocation
In your team's Discord or Slack channel:
```text
@switch-buddy-admin [ALERT P0] Production checkout service is failing with ZeroDivisionError on 100% discount promo orders! Please investigate checkout.py and propose a fix.
```

---

## 2. Reviewing the Status Board & Investigation

The agent will post an interactive Markdown status board:
- **Severity Badge**: Red for P0 (Outage), Orange for P1 (Degraded), Yellow for P2.
- **Blast Radius**: Estimated percentage of affected users and projected financial risk.
- **SLA Deadlines**: Real-time MTTA (Target: < 5m) and MTTR (Target: < 30m) countdown.
- **Live Timeline**: Every tool call and discovery logged with UTC timestamps.

---

## 3. Human Signoff & Deployment

When the agent completes test reproduction and patch synthesis, it will halt and request approval:

```diff
--- a/demo-service/checkout.py
+++ b/demo-service/checkout.py
@@ -21,7 +21,10 @@ def calculate_order_total(items: List[Dict[str, Any]], discount_pct: float = 0.
     discount_amount = round(subtotal * (discount_pct / 100.0), 2)
     net_total = round(subtotal - discount_amount, 2)
-    savings_ratio = round(subtotal / net_total, 2)
+    if net_total == 0.0:
+        savings_ratio = 1.0  # 100% discount means full savings
+    else:
+        savings_ratio = round(subtotal / net_total, 2)
```

**To Deploy:** Reply with `Approve` in the thread (or click the Discord/Slack button).  
**To Abort:** Reply with `Reject` or click Stop Current Work.

---

## 4. Post-Incident Review & Archival

Upon resolution:
1. SwitchGuard automatically generates an audit-ready blameless postmortem under `docs/postmortems/`.
2. All actions, diffs, and human signoffs are cryptographically sealed in the SHA-256 Audit Vault.
3. Postmortem action items are exported for Jira / Linear tracking.
