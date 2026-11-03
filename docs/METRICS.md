# 📊 SwitchGuard Prometheus Metrics Reference

SwitchGuard exposes native Prometheus metrics to monitor incident response efficiency, MTTA/MTTR, and alert storm suppression in real time.

---

## 1. Metric Definitions

| Metric Name | Type | Description |
|---|---|---|
| `switchguard_incidents_total{severity="P0\|P1\|P2\|P3"}` | Counter | Total number of incidents opened, partitioned by severity. |
| `switchguard_suppressed_alerts_total` | Counter | Total number of duplicate telemetry alerts suppressed by the sliding-window deduplicator. |
| `switchguard_approved_patches_total` | Counter | Total count of autonomous patches approved by human operators in chat. |
| `switchguard_mttr_average_seconds` | Gauge | Moving average Mean Time to Resolution across resolved incidents. |

---

## 2. Scraping Metrics

To inspect metrics via CLI:
```bash
python cli.py metrics
```

Output:
```prometheus
# HELP switchguard_incidents_total Total number of triggered incidents by severity
# TYPE switchguard_incidents_total counter
switchguard_incidents_total{severity="P0"} 1
switchguard_incidents_total{severity="P1"} 0
switchguard_incidents_total{severity="P2"} 0
switchguard_incidents_total{severity="P3"} 0
# HELP switchguard_suppressed_alerts_total Total number of duplicate alerts suppressed by deduplicator
# TYPE switchguard_suppressed_alerts_total counter
switchguard_suppressed_alerts_total 5
# HELP switchguard_approved_patches_total Total number of autonomous patches approved by human operators
# TYPE switchguard_approved_patches_total counter
switchguard_approved_patches_total 1
# HELP switchguard_mttr_average_seconds Average Mean Time to Resolution in seconds
# TYPE switchguard_mttr_average_seconds gauge
switchguard_mttr_average_seconds 171.0
```

---

## 3. Grafana Dashboard Configuration

Add the following PromQL queries to your Grafana dashboard:
- **Active P0 Incidents**: `sum(switchguard_incidents_total{severity="P0"})`
- **Alert Storm Suppression Efficiency**: `rate(switchguard_suppressed_alerts_total[5m])`
- **Average MTTR Trend**: `switchguard_mttr_average_seconds / 60` (minutes)
