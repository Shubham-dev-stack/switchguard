import pytest
import sys
from cli import main

def test_cli_triage(capsys, monkeypatch):
    test_args = ["cli.py", "triage", "--service", "checkout", "--error", "ZeroDivisionError", "--error-rate", "100"]
    monkeypatch.setattr(sys, "argv", test_args)
    ret = main()
    assert ret == 0
    captured = capsys.readouterr()
    assert "=== SwitchGuard Triage Result ===" in captured.out
    assert "Assigned:     P0" in captured.out

def test_cli_probe(capsys, monkeypatch):
    test_args = ["cli.py", "probe", "--service", "billing-api"]
    monkeypatch.setattr(sys, "argv", test_args)
    ret = main()
    assert ret == 0
    captured = capsys.readouterr()
    assert "=== Service Health: billing-api ===" in captured.out
    assert "Status:   HEALTHY" in captured.out

def test_cli_postmortem(capsys, monkeypatch):
    test_args = ["cli.py", "postmortem", "--incident-id", "INC-TEST-1", "--service", "checkout-service"]
    monkeypatch.setattr(sys, "argv", test_args)
    ret = main()
    assert ret == 0
    captured = capsys.readouterr()
    assert "# 📑 Postmortem: [P0] Autonomous Incident Remediation for checkout-service" in captured.out

def test_cli_simulate(capsys, monkeypatch):
    test_args = ["cli.py", "simulate"]
    monkeypatch.setattr(sys, "argv", test_args)
    ret = main()
    assert ret == 0
    captured = capsys.readouterr()
    assert "SwitchGuard Autonomous Incident Simulation" in captured.out

def test_cli_metrics(capsys, monkeypatch):
    test_args = ["cli.py", "metrics"]
    monkeypatch.setattr(sys, "argv", test_args)
    ret = main()
    assert ret == 0
    captured = capsys.readouterr()
    assert "switchguard_incidents_total" in captured.out

def test_cli_audit_verify(capsys, monkeypatch):
    test_args = ["cli.py", "audit-verify"]
    monkeypatch.setattr(sys, "argv", test_args)
    ret = main()
    assert ret == 0
    captured = capsys.readouterr()
    assert "VALID (SHA-256 intact)" in captured.out

def test_cli_dashboard_args(monkeypatch):
    import cli
    monkeypatch.setattr("dashboard.server.start_server", lambda port, open_browser: None)
    monkeypatch.setattr(sys, "argv", ["cli.py", "dashboard", "--no-browser", "--port", "9999"])
    ret = cli.main()
    assert ret == 0
