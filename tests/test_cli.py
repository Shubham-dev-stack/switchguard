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
