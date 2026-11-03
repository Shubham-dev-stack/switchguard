import pytest
import os
from diagnostics.log_analyzer import LogAnalyzer
from diagnostics.healthcheck import ServiceHealthProbe
from diagnostics.git_blame_inspector import GitBlameInspector

def test_log_analyzer_pii_scrubbing():
    raw_log = "User test@example.com authorization failed with Bearer abc123secret and card 4111-2222-3333-4444"
    scrubbed = LogAnalyzer.redact_pii(raw_log)
    assert "[REDACTED_EMAIL]" in scrubbed
    assert "[REDACTED_TOKEN]" in scrubbed
    assert "[REDACTED_CARD_NUMBER]" in scrubbed
    assert "abc123secret" not in scrubbed

def test_stack_trace_signature_extraction():
    sample_trace = """
Traceback (most recent call last):
  File "demo-service/checkout.py", line 24, in calculate_order_total
    savings_ratio = round(subtotal / net_total, 2)
ZeroDivisionError: float division by zero
    """
    sig = LogAnalyzer.extract_error_signature(sample_trace)
    assert sig["exception_type"] == "ZeroDivisionError"
    assert "float division by zero" in sig["exception_message"]
    assert sig["failing_frame"] is not None
    assert sig["failing_frame"]["file"] == "demo-service/checkout.py"
    assert sig["failing_frame"]["line"] == 24
    assert sig["failing_frame"]["function"] == "calculate_order_total"

def test_health_probe_healthy():
    probe = ServiceHealthProbe("checkout-service")
    res = probe.probe(lambda: True)
    assert res["status"] == "HEALTHY"
    assert res["healthy"] is True
    assert res["error"] is None

def test_health_probe_failure():
    probe = ServiceHealthProbe("postgres-db")
    def failing_call():
        raise ConnectionRefusedError("Connection to 127.0.0.1:5432 refused")
    res = probe.probe(failing_call)
    assert res["status"] == "UNHEALTHY"
    assert res["healthy"] is False
    assert "refused" in res["error"]

def test_git_blame_inspector():
    cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    inspector = GitBlameInspector(cwd)
    commits = inspector.get_recent_commits("demo-service/checkout.py")
    assert isinstance(commits, list)
    if commits:
        assert "commit_hash" in commits[0]
        assert "author" in commits[0]
