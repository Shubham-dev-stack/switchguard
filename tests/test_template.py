import os
import yaml
import pytest

def test_switchguard_template_schema():
    template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "switchguard.template.yaml")
    assert os.path.exists(template_path)

    with open(template_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    assert data["version"] == 1
    assert "params" in data
    assert "agents" in data
    assert "room" in data
    assert "kickoff" in data

    # Verify params
    params = data["params"]
    assert "incident_id" in params
    assert "service_name" in params
    assert "directory" in params
    assert "bridge" in params

    # Verify all 3 agents
    agents = data["agents"]
    assert len(agents) == 3
    agent_names = [a["name"] for a in agents]
    assert "switchguard-commander" in agent_names
    assert "switchguard-investigator" in agent_names
    assert "switchguard-fixer" in agent_names

    for a in agents:
        assert "directory" in a
        assert "provider" in a
        assert "location" in a
        assert "instructions" in a

    # Verify room and kickoff
    room = data["room"]
    assert len(room["agents"]) == 3
    assert "@switchguard-commander" in data["kickoff"]
