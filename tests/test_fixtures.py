import os
import json
import pytest
from ingestion.parsers import SentryWebhookParser, DatadogWebhookParser, PrometheusAlertmanagerParser

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")

def test_sentry_fixture_loading():
    path = os.path.join(FIXTURES_DIR, "sentry_p0_payload.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    alert = SentryWebhookParser.parse(data)
    assert alert.service == "checkout-service"
    assert alert.error_type == "ZeroDivisionError"
    assert alert.stack_trace == "demo-service/checkout.py:24 in calculate_order_total"

def test_datadog_fixture_loading():
    path = os.path.join(FIXTURES_DIR, "datadog_latency_payload.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    alert = DatadogWebhookParser.parse(data)
    assert alert.service == "checkout-service"
    assert alert.source == "datadog"

def test_prometheus_fixture_loading():
    path = os.path.join(FIXTURES_DIR, "prometheus_deadlock_payload.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    alert = PrometheusAlertmanagerParser.parse(data)
    assert alert.service == "billing-api"
    assert alert.error_type == "PostgresTransactionLockExhaustion"
