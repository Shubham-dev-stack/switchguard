import pytest
import time
from core.models import Alert
from ingestion.parsers import SentryWebhookParser, DatadogWebhookParser, PrometheusAlertmanagerParser
from ingestion.deduplicator import AlertDeduplicator

def test_sentry_webhook_parser():
    payload = {
        "id": "1002",
        "url": "https://sentry.io/organizations/acme/issues/1002/",
        "data": {
            "issue": {
                "project": {"slug": "checkout-service"},
                "metadata": {"type": "ZeroDivisionError", "value": "float division by zero"}
            },
            "event": {
                "event_id": "a1b2c3d4",
                "entries": [
                    {
                        "type": "exception",
                        "data": {
                            "values": [
                                {
                                    "stacktrace": {
                                        "frames": [
                                            {"filename": "checkout.py", "lineno": 24, "function": "calculate_order_total"}
                                        ]
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }
    }
    alert = SentryWebhookParser.parse(payload)
    assert alert.alert_id == "SENTRY-a1b2c3d4"
    assert alert.service == "checkout-service"
    assert alert.error_type == "ZeroDivisionError"
    assert "float division by zero" in alert.message
    assert alert.stack_trace == "checkout.py:24 in calculate_order_total"

def test_datadog_webhook_parser():
    payload = {
        "id": "99210",
        "event_title": "High P99 Latency Spike",
        "body": "Average latency > 2500ms on /process",
        "tags": "env:production,service:payment-gateway,tier:1",
        "priority": "high"
    }
    alert = DatadogWebhookParser.parse(payload)
    assert alert.alert_id == "DD-99210"
    assert alert.service == "payment-gateway"
    assert alert.source == "datadog"

def test_prometheus_alertmanager_parser():
    payload = {
        "alerts": [
            {
                "labels": {"job": "database-primary", "alertname": "PostgresDeadlockDetected", "instance": "db-01"},
                "annotations": {"summary": "Transaction lock wait exceeded 30s"}
            }
        ]
    }
    alert = PrometheusAlertmanagerParser.parse(payload)
    assert alert.service == "database-primary"
    assert alert.error_type == "PostgresDeadlockDetected"
    assert "lock wait exceeded" in alert.message

def test_alert_storm_deduplicator():
    dedup = AlertDeduplicator(window_seconds=10.0)
    alert = Alert(
        alert_id="ALT-1",
        source="sentry",
        service="checkout-service",
        error_type="ZeroDivisionError",
        message="float division by zero"
    )

    # First occurrence triggers new incident
    is_new, count = dedup.process(alert)
    assert is_new is True
    assert count == 1

    # Rapid succession alerts suppressed
    for _ in range(4):
        is_new, count = dedup.process(alert)
        assert is_new is False

    assert count == 5
    stats = dedup.get_storm_stats()
    assert stats["tracked_fingerprints"] == 1
    assert stats["total_suppressed_alerts"] == 4
