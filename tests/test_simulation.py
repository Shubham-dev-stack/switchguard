import pytest
from scripts.simulate_p0_outage import run_simulation
from scripts.verify_cluster_health import verify_cluster

def test_incident_simulation_run(capsys):
    ret = run_simulation()
    assert ret == 0
    captured = capsys.readouterr()
    assert "SwitchGuard Autonomous Incident Simulation" in captured.out
    assert "Service Restored!" in captured.out

def test_cluster_health_verification(capsys):
    ret = verify_cluster()
    assert ret == 0
    captured = capsys.readouterr()
    assert "checkout-service" in captured.out
    assert "payment-gateway" in captured.out
